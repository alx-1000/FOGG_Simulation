import copy
import random
from dataclasses import dataclass

from src.board import print_board
from src.piece import pieces_F, pieces_G
from src.score import calculate_score, calculate_x_lines, calculate_y_lines, calculate_z_lines


@dataclass(frozen=True)
class Action:
    """An AI-safe description of one decision; it never holds a Piece object."""

    kind: str
    x: int | None = None
    y: int | None = None
    piece_index: int | None = None
    direction1: str | None = None
    direction2: str | None = None
    down_direction: str | None = None


class Game:
    def __init__(self):
        self.phase = 1
        self.current_player = "F"
        self.score_F = 0
        self.score_G = 0
        self.game_over = False
        self.phase_end_used = {"F": False, "G": False}

        # A game must own its pieces: directions are mutated when a piece is placed.
        self.hand = {"F": copy.deepcopy(pieces_F), "G": copy.deepcopy(pieces_G)}
        self.last_action = None
        self.history = []
        self.phase_end_rule = "by_player"  # "by_player" or "fixed"
        self.board = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def clone(self):
        return copy.deepcopy(self)

    def change_turn(self):
        self.current_player = "G" if self.current_player == "F" else "F"

    def can_put_piece(self, x, y, piece):
        z = self.phase - 1
        return (
            0 <= x < 3
            and 0 <= y < 3
            and self.board[z][y][x] is None
            and piece in self.hand[self.current_player]
        )

    def put_piece(self, x, y, piece, direction1, direction2, down_direction=None):
        if not self.can_put_piece(x, y, piece):
            return False

        z = self.phase - 1
        piece.direction1 = direction1
        piece.direction2 = direction2
        piece.down_direction = down_direction
        self.board[z][y][x] = piece
        self.hand[self.current_player].remove(piece)
        self.change_turn()
        return True

    def can_hang_piece(self, x, y, piece, direction1, direction2):
        if self.phase < 2 or not self.can_put_piece(x, y, piece):
            return False
        directions = {direction1, direction2}
        if x in (0, 2) and y in (0, 2):
            return directions in ({"X", "Z"}, {"Y", "Z"})
        if x in (0, 2):
            return directions == {"X", "Z"}
        if y in (0, 2):
            return directions == {"Y", "Z"}
        return False

    def print_board(self):
        print_board(self.board)

    def end_phase_by_player(self):
        if not self.can_end_phase():
            return False
        self.phase_end_used[self.current_player] = True
        self.end_phase()
        self.change_turn()
        return True

    def end_phase(self):
        x_lines = calculate_x_lines(self.board, self.phase)
        y_lines = calculate_y_lines(self.board, self.phase)
        z_lines = calculate_z_lines(self.board, self.phase)
        score_F, score_G = calculate_score(x_lines, y_lines, z_lines)
        self.score_F += score_F
        self.score_G += score_G
        if self.phase < 3:
            self.phase += 1
        else:
            self.phase = 4
            self.game_over = True

    def can_end_phase(self):
        return (
            not self.game_over
            and self.phase < 3
            and not self.phase_end_used[self.current_player]
        )

    def is_phase_full(self):
        z = self.phase - 1
        return all(self.board[z][y][x] is not None for y in range(3) for x in range(3))

    def empty_cells_in_phase(self):
        z = self.phase - 1
        return sum(self.board[z][y][x] is None for y in range(3) for x in range(3))

    def get_legal_moves(self):
        """Legacy Piece-based placement API. AI code should use get_legal_actions."""
        moves = []
        directions = ("X", "Y", "Z")
        for y in range(3):
            for x in range(3):
                for piece in self.hand[self.current_player]:
                    if self.can_put_piece(x, y, piece):
                        for direction1 in directions:
                            for direction2 in directions:
                                if direction1 != direction2:
                                    moves.append((x, y, piece, direction1, direction2, None))
                    for direction1 in directions:
                        for direction2 in directions:
                            if direction1 == direction2:
                                continue
                            if self.can_hang_piece(x, y, piece, direction1, direction2):
                                if "X" in (direction1, direction2):
                                    moves.append((x, y, piece, direction1, direction2, "X"))
                                if "Y" in (direction1, direction2):
                                    moves.append((x, y, piece, direction1, direction2, "Y"))
        return moves

    def get_legal_actions(self):
        """Return every player-selectable action for the current settled state."""
        if self.game_over or self.is_phase_full():
            return []

        actions = []
        directions = ("X", "Y", "Z")
        for y in range(3):
            for x in range(3):
                for piece_index, piece in enumerate(self.hand[self.current_player]):
                    if self.can_put_piece(x, y, piece):
                        for direction1 in directions:
                            for direction2 in directions:
                                if direction1 != direction2:
                                    actions.append(Action("put", x, y, piece_index, direction1, direction2))
                    for direction1 in directions:
                        for direction2 in directions:
                            if direction1 == direction2 or not self.can_hang_piece(x, y, piece, direction1, direction2):
                                continue
                            if "X" in (direction1, direction2):
                                actions.append(Action("put", x, y, piece_index, direction1, direction2, "X"))
                            if "Y" in (direction1, direction2):
                                actions.append(Action("put", x, y, piece_index, direction1, direction2, "Y"))

        if self.phase_end_rule == "by_player" and self.can_end_phase():
            actions.append(Action("end_phase"))
        if not actions:
            actions.append(Action("pass"))
        return actions

    def apply_action(self, action):
        """Apply an Action from get_legal_actions and return its event record."""
        legal_actions = self.get_legal_actions()
        if action not in legal_actions:
            raise ValueError(f"Illegal action: {action}")

        player = self.current_player
        if action.kind == "put":
            piece = self.hand[player][action.piece_index]
            self.put_piece(action.x, action.y, piece, action.direction1, action.direction2, action.down_direction)
            event = {
                "type": "put", "player": player, "phase": self.phase,
                "x": action.x, "y": action.y, "piece": piece,
                "direction1": action.direction1, "direction2": action.direction2,
                "down_direction": action.down_direction,
            }
        elif action.kind == "end_phase":
            self.end_phase_by_player()
            event = self._phase_end_event(player, "by_player")
        elif action.kind == "pass":
            self.change_turn()
            event = self._event("pass", player)
        else:
            raise ValueError(f"Unknown action kind: {action.kind}")

        self.last_action = action
        self.history.append(event)
        return event

    def advance_forced_actions(self):
        """Resolve full layers, mandatory phase ends, passes, and terminal conditions."""
        events = []
        while not self.game_over:
            player = self.current_player
            if self.phase == 3 and not self.hand["F"] and not self.hand["G"]:
                self.end_phase()
                event = self._event("game_end", player, reason="hands_empty")
            elif (
                self.phase_end_rule == "fixed"
                and self.phase < 3
                and self.empty_cells_in_phase() == 1
                and self.can_end_phase()
            ):
                self.end_phase_by_player()
                event = self._phase_end_event(player, "fixed")
            elif self.is_phase_full():
                if self.phase == 3:
                    self.end_phase()
                    event = self._event("game_end", player, reason="board_full")
                elif self.can_end_phase():
                    self.end_phase_by_player()
                    event = self._phase_end_event(player, "board_full")
                else:
                    self.change_turn()
                    event = self._event("pass", player, reason="board_full")
            else:
                legal = self.get_legal_actions()
                if legal != [Action("pass")]:
                    break
                self.change_turn()
                event = self._event("pass", player, reason="no_legal_move")
            self.history.append(event)
            events.append(event)
        return events

    def _event(self, event_type, player, **extra):
        return {
            "type": event_type,
            "player": player,
            "phase": self.phase,
            "score_F": self.score_F,
            "score_G": self.score_G,
            "F_hand": len(self.hand["F"]),
            "G_hand": len(self.hand["G"]),
            **extra,
        }

    def _phase_end_event(self, player, reason):
        ended_phase = self.phase - 1
        z = ended_phase - 1
        empty_cells = sum(
            self.board[z][y][x] is None
            for y in range(3)
            for x in range(3)
        )
        return self._event(
            "end_phase",
            player,
            reason=reason,
            ended_phase=ended_phase,
            empty_cells_at_end=empty_cells,
        )

    def random_move(self):
        actions = [action for action in self.get_legal_actions() if action.kind == "put"]
        if not actions:
            return False
        self.apply_action(random.choice(actions))
        return True

    def random_action(self):
        """Compatibility helper retaining the original random phase-end policy."""
        self.advance_forced_actions()
        if self.game_over:
            return "game_end"

        actions = self.get_legal_actions()
        placement_actions = [action for action in actions if action.kind == "put"]
        if (
            self.phase_end_rule == "by_player"
            and Action("end_phase") in actions
            and self.empty_cells_in_phase() < 8
            and random.random() < 0.1
        ):
            action = Action("end_phase")
        elif placement_actions:
            action = random.choice(placement_actions)
        else:
            action = Action("pass")
        self.apply_action(action)
        return "end" if action.kind == "end_phase" else action.kind

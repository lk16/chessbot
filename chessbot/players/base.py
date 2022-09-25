from datetime import datetime
from typing import List

from chessbot.board import Board
from chessbot.enums import Color

STALEMATE_HEURISTIC = 0
CHECKMATE_HEURISTIC = 999999


class BasePlayer:
    def __init__(self, color: Color) -> None:
        assert color != Color.NOBODY
        self.color = color

    def do_move(self, board: Board) -> Board:
        raise NotImplementedError


class BaseBot(BasePlayer):
    def __init__(self, color: Color, depth: int) -> None:
        self.depth = depth
        self.nodes = 0
        self.search_start = datetime.now()
        super().__init__(color)

    def do_move(self, board: Board) -> Board:
        self.nodes = 0
        self.search_start = datetime.now()

        moves = board.get_moves()
        assert moves

        best_heuristic = -999999  # very bad
        best_move: Board = Board.empty()  # value doesn't matter

        print(f"{type(self).__name__} is thinking:")
        for i, move in enumerate(moves):
            heur = self.minimax(move, self.depth, False)

            speed = self.search_speed()
            print(
                f"{i+1:>2}/{len(moves):>2} | heur = {heur:>4} | {speed:7.0f} nodes/sec"
            )

            if heur > best_heuristic:
                best_heuristic = heur
                best_move = move

        return best_move

    def minimax(self, board: Board, depth: int, is_max: bool) -> int:
        self.nodes += 1

        if depth == 0:
            return self.heuristic(board)

        moves = board.get_moves()

        if not moves:
            if board.is_checked(board.turn):
                if board.turn == self.color:
                    return -CHECKMATE_HEURISTIC
                return CHECKMATE_HEURISTIC

            return STALEMATE_HEURISTIC

        heurs: List[int] = []

        for move in moves:
            heur = self.minimax(move, depth - 1, not is_max)
            heurs.append(heur)

        if is_max:
            return max(heurs)
        else:
            return min(heurs)

    def search_speed(self) -> float:
        elapsed_seconds = (datetime.now() - self.search_start).total_seconds()
        return self.nodes / elapsed_seconds

    def heuristic(self, board: Board) -> int:
        raise NotImplementedError

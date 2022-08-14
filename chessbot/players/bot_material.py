from typing import List

from chessbot.board import Board
from chessbot.enums import Color, PieceType
from chessbot.players.base import BasePlayer

DEPTH = 2
STALEMATE_HEURISTIC = 0
CHECKMATE_HEURISTIC = 999999


class MaterialBot(BasePlayer):
    def do_move(self, board: Board) -> Board:
        moves = board.get_moves()
        assert moves

        best_heuristic = -999999  # very bad
        best_move: Board = Board.empty()  # value doesn't matter

        print("MaterialBot is thinking:")
        for i, move in enumerate(moves):
            heur = self.minimax(move, DEPTH, False)

            if heur > best_heuristic:
                print(f"{i+1:>2}/{len(moves):>2}: heur = {heur}")
                best_heuristic = heur
                best_move = move

        return best_move

    def minimax(self, board: Board, depth: int, is_max: bool) -> int:
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

    def heuristic(self, board: Board) -> int:
        black_material = 0
        white_material = 0

        for field in board.fields:
            if field == PieceType.BLACK_PAWN:
                black_material += 1
            elif field == PieceType.BLACK_ROOK:
                black_material += 5
            elif field == PieceType.BLACK_KNIGHT:
                black_material += 3
            elif field == PieceType.BLACK_QUEEN:
                black_material += 9
            elif field == PieceType.BLACK_BISHOP:
                black_material += 3
            elif field == PieceType.WHITE_PAWN:
                white_material += 1
            elif field == PieceType.WHITE_ROOK:
                white_material += 5
            elif field == PieceType.WHITE_KNIGHT:
                white_material += 3
            elif field == PieceType.WHITE_QUEEN:
                white_material += 9
            elif field == PieceType.WHITE_BISHOP:
                white_material += 3

        if self.color == Color.WHITE:
            return white_material - black_material
        else:
            return black_material - white_material

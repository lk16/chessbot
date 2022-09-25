from chessbot.board import Board
from chessbot.enums import Color, PieceType
from chessbot.players.base import BaseBot


class MaterialBot(BaseBot):
    def __init__(self, color: Color, depth: int) -> None:
        self.piece_type_values = {
            PieceType.EMPTY: 0,
            PieceType.BLACK_PAWN: -1,
            PieceType.BLACK_ROOK: -5,
            PieceType.BLACK_KNIGHT: -3,
            PieceType.BLACK_KING: -9001,
            PieceType.BLACK_QUEEN: -9,
            PieceType.BLACK_BISHOP: -3,
            PieceType.WHITE_PAWN: 1,
            PieceType.WHITE_ROOK: 5,
            PieceType.WHITE_KNIGHT: 3,
            PieceType.WHITE_KING: 9001,
            PieceType.WHITE_QUEEN: 9,
            PieceType.WHITE_BISHOP: 3,
        }
        super().__init__(color, depth)

    def heuristic(self, board: Board) -> int:
        total = 0

        for field in board.fields:
            total += self.piece_type_values[field]

        if self.color == Color.BLACK:
            total *= -1

        return total

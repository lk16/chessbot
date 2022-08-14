from chessbot.board import Board
from chessbot.enums import Color, PieceType
from chessbot.players.base import BaseBot


class MaterialBot(BaseBot):
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

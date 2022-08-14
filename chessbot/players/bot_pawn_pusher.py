from chessbot.board import Board
from chessbot.enums import Color, PieceType, Square
from chessbot.players.base import BaseBot


class PawnPusherBot(BaseBot):
    def heuristic(self, board: Board) -> int:
        black_total = 0
        white_total = 0

        for square_id, field in enumerate(board.fields):
            square = Square(square_id)
            _, y = square.get_xy()
            if field == PieceType.BLACK_PAWN:
                black_total += y - 1
            elif field == PieceType.WHITE_PAWN:
                white_total += 6 - y

        if self.color == Color.WHITE:
            return white_total - black_total
        else:
            return black_total - white_total

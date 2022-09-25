from chessbot.board import Board
from chessbot.enums import Color, PieceType
from chessbot.players.base import BaseBot


class PawnPusherBot(BaseBot):
    def heuristic(self, board: Board) -> int:
        total = 0

        for square_id, field in enumerate(board.fields):
            y = square_id // 8

            if field == PieceType.BLACK_PAWN:
                total -= y - 1
            elif field == PieceType.WHITE_PAWN:
                total += 6 - y
            elif field == PieceType.BLACK_QUEEN:
                total -= 9
            elif field == PieceType.WHITE_QUEEN:
                total += 9

        if self.color == Color.BLACK:
            total *= -1

        return total

#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import Color, PieceType, Square


def main() -> None:
    fields = 64 * [PieceType.EMPTY]
    fields[Square.A7] = PieceType.WHITE_KING
    fields[Square.D6] = PieceType.BLACK_PAWN

    board = Board(turn=Color.WHITE, fields=fields, en_passent_column=0)
    board.show()

    is_checked = board.is_checked()
    print(f"is_checked: {is_checked}")


if __name__ == "__main__":
    main()

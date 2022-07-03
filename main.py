#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import Color, PieceType, Square


def main() -> None:
    fields = 64 * [PieceType.EMPTY]
    fields[Square.A4] = PieceType.WHITE_PAWN
    fields[Square.B4] = PieceType.BLACK_PAWN
    fields[Square.A5] = PieceType.BLACK_PAWN

    board = Board(turn=Color.BLACK, fields=fields, en_passent_column=0)

    children = board.get_moves()

    for child in children:
        child.show()

    print(f"Found {len(children)} children.")


if __name__ == "__main__":
    main()

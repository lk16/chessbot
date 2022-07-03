#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import Color, PieceType, Square


def main() -> None:
    fields = 64 * [PieceType.EMPTY]
    fields[Square.F4] = PieceType.WHITE_PAWN
    fields[Square.F5] = PieceType.BLACK_PAWN
    fields[Square.G5] = PieceType.WHITE_KNIGHT
    fields[Square.E5] = PieceType.WHITE_KNIGHT

    board = Board(turn=Color.WHITE, fields=fields, en_passent_column=5)

    children = board.get_moves()

    for child in children:
        child.show()

    print(f"Found {len(children)} children.")


if __name__ == "__main__":
    main()

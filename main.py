#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import Color, PieceType, Square


def main() -> None:
    fields = 64 * [PieceType.EMPTY]
    fields[Square.F6] = PieceType.WHITE_PAWN
    fields[Square.E7] = PieceType.BLACK_ROOK
    fields[Square.G7] = PieceType.BLACK_ROOK

    board = Board(turn=Color.WHITE, fields=fields, en_passent_column=0)

    children = board.get_moves()

    for child in children:
        child.show()

    print(f"Found {len(children)} children.")


if __name__ == "__main__":
    main()

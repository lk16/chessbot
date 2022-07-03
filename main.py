#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import Color, PieceType, Square


def main() -> None:
    fields = 64 * [PieceType.EMPTY]
    fields[Square.G3] = PieceType.WHITE_QUEEN

    board = Board(turn=Color.WHITE, fields=fields)

    children = board.get_moves()

    for child in children:
        child.show()

    print(f"Found {len(children)} children.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import PieceType, Square


def main() -> None:
    board = Board.empty()
    board.fields[Square.G3] = PieceType.WHITE_ROOK

    children = board.get_moves()

    for child in children:
        child.show()

    print(f"Found {len(children)} children.")


if __name__ == "__main__":
    main()

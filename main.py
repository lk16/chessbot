#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import PieceType, Square


def main() -> None:
    board = Board.empty()
    board.fields[Square.D5] = PieceType.WHITE_KNIGHT
    board.fields[Square.E5] = PieceType.WHITE_KING

    children = board.get_moves()

    for child in children:
        child.show()

    print(f"Found {len(children)} children.")


if __name__ == "__main__":
    main()

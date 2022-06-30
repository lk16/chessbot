#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import PieceType, Square


def main() -> None:
    board = Board.empty()
    board.fields[Square.H1] = PieceType.WHITE_KING

    for child in board.get_moves():
        child.show()


if __name__ == "__main__":
    main()

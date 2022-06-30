#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import PieceType, Square


def main() -> None:
    board = Board.empty()
    board.fields[Square.H8] = PieceType.WHITE_KNIGHT

    for child in board.get_moves():
        child.show()


if __name__ == "__main__":
    main()

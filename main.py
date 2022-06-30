#!/usr/bin/env python

from chessbot.board import Board
from chessbot.enums import PieceType, Square


def main() -> None:
    board = Board.start()
    board.show()

    board = Board.empty()
    board.fields[Square.B3] = PieceType.WHITE_KING
    board.show()


if __name__ == "__main__":
    main()

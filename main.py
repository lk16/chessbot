#!/usr/bin/env python

from chessbot.board import Board


def main() -> None:
    start_board = Board.start()
    start_board.show()

    empty_board = Board.empty()
    empty_board.show()


if __name__ == "__main__":
    main()

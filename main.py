#!/usr/bin/env python

from chessbot.board import Board


def main() -> None:
    fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

    board = Board.from_fen(fen)

    board.show()
    print(board.to_fen())
    print(board.editor_link())


if __name__ == "__main__":
    main()

#!/usr/bin/env python

from chessbot.board import Board


def main() -> None:
    fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"

    board = Board.from_fen(fen)
    board.show()


if __name__ == "__main__":
    main()

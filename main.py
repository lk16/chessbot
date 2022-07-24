#!/usr/bin/env python

from chessbot.board import Board


def main() -> None:
    fen = "6k1/8/4P3/8/8/8/1K4R1/8 b - - 0 1"

    board = Board.from_fen(fen)

    moves = board.get_moves()
    board.show()

    for move in moves:
        move.show()

    print(f"Found {len(moves)} moves.")
    print(f"start board is_checkmated: {board.is_checkmate()}")
    print(f"start board is_stalemated: {board.is_stalemate()}")


if __name__ == "__main__":
    main()

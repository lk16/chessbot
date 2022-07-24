#!/usr/bin/env python

from chessbot.board import Board


def main() -> None:
    fen = "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1"

    board = Board.from_fen(fen)

    moves = board.get_moves()
    board.show()

    for move in moves:
        move.show()
        print()
        print()
        print()

    print(f"Found {len(moves)} moves.")
    print(f"start board is_checkmated: {board.is_checkmate()}")
    print(f"start board is_stalemated: {board.is_stalemate()}")


if __name__ == "__main__":
    main()

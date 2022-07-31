#!/usr/bin/env python

from datetime import datetime
from typing import List

from chessbot.board import Board


def get_decendants(board: Board, depth: int) -> List[Board]:
    if depth == 1:
        return board.get_moves()

    descendants: List[Board] = []

    for child in board.get_moves():
        descendants += get_decendants(child, depth - 1)

    return descendants


def main() -> None:
    board = Board.start()

    for depth in range(1, 6):

        before = datetime.now()
        desc_count = len(get_decendants(board, depth))
        after = datetime.now()

        seconds = (after - before).total_seconds()

        speed = desc_count / seconds

        print(
            f"depth {depth:>2} | {desc_count:>10} descendants | {seconds:7.2f} sec | {speed:7.0f} boards/sec"
        )


if __name__ == "__main__":
    main()

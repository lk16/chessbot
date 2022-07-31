#!/usr/bin/env python

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
        desc_count = len(get_decendants(board, depth))
        print(f"At depth {depth}: found {desc_count} descendants.")


if __name__ == "__main__":
    main()

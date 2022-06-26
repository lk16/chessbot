from chessbot.board import Board


def main() -> None:
    board = Board()
    moves = board.get_children()

    for move in moves:
        move.show()


if __name__ == "__main__":
    main()

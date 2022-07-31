import random

from chessbot.board import Board


class RandomMoveBot:
    def do_move(self, board: Board) -> Board:
        moves = board.get_moves()
        return random.choice(moves)

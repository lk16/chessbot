import random

from chessbot.board import Board
from chessbot.players.base import BasePlayer


class RandomPlayer(BasePlayer):
    def do_move(self, board: Board) -> Board:
        moves = board.get_moves()
        return random.choice(moves)

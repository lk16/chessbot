#!/usr/bin/env python

from chessbot.game import Game
from chessbot.players.random import RandomMoveBot


def main() -> None:
    random_move_bot = RandomMoveBot()
    game = Game(black=random_move_bot, white=random_move_bot)
    game.play()


if __name__ == "__main__":
    main()

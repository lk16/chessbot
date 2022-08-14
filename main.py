#!/usr/bin/env python

from chessbot.enums import Color
from chessbot.game import Game
from chessbot.players.bot_material import MaterialBot
from chessbot.players.random import RandomPlayer


def main() -> None:
    white_player = MaterialBot(Color.WHITE)
    black_player = RandomPlayer(Color.BLACK)

    game = Game(black=black_player, white=white_player)
    game.play()


if __name__ == "__main__":
    main()

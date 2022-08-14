#!/usr/bin/env python

from chessbot.enums import Color
from chessbot.game import Game
from chessbot.players.bot_pawn_pusher import PawnPusherBot
from chessbot.players.random import RandomPlayer


def main() -> None:
    white_player = RandomPlayer(Color.WHITE)
    black_player = PawnPusherBot(Color.BLACK, 1)

    game = Game(black=black_player, white=white_player)
    game.play()


if __name__ == "__main__":
    main()

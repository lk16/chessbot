#!/usr/bin/env python

from chessbot.enums import Color
from chessbot.game import Game
from chessbot.players.bot_material import MaterialBot
from chessbot.players.bot_pawn_pusher import PawnPusherBot


def main() -> None:
    white_player = MaterialBot(Color.WHITE, 2)
    black_player = PawnPusherBot(Color.BLACK, 2)

    game = Game(black=black_player, white=white_player)
    game.play()


if __name__ == "__main__":
    main()

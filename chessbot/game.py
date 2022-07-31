from chessbot.board import Board
from chessbot.players.random import RandomMoveBot


class Game:
    def __init__(self, black: RandomMoveBot, white: RandomMoveBot) -> None:
        self.players = [black, white]
        self.board = Board.start()

    def get_player_to_move(self) -> RandomMoveBot:
        return self.players[self.board.turn]

    def is_game_over(self) -> bool:
        moves = self.board.get_moves()
        return len(moves) == 0

    def play(self) -> None:
        self.board.show()

        while not self.is_game_over():
            player_to_move = self.get_player_to_move()
            self.board = player_to_move.do_move(self.board)
            self.board.show()

        self.board.show()

        # TODO find out who won

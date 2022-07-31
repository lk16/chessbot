from typing import Optional, Tuple

from chessbot.board import Board
from chessbot.enums import Color, GameState, PieceType
from chessbot.players.random import RandomMoveBot


class Game:
    def __init__(self, black: RandomMoveBot, white: RandomMoveBot) -> None:
        self.players = [black, white]
        self.board = Board.start()

    def get_player_to_move(self) -> RandomMoveBot:
        return self.players[self.board.turn]

    def get_game_state(self) -> Tuple[GameState, Optional[Color]]:
        """
        Returns game state and player that won
        """
        moves = self.board.get_moves()
        if len(moves) == 0:
            if self.board.is_checked(self.board.turn):
                return GameState.CHECKMATE, self.board.turn.opponent()

            return GameState.STALEMATE, None

        num_pieces = self.board.count_piece_types()

        if (
            num_pieces[PieceType.WHITE_QUEEN] == 0
            and num_pieces[PieceType.BLACK_QUEEN] == 0
            and num_pieces[PieceType.WHITE_ROOK] == 0
            and num_pieces[PieceType.BLACK_ROOK] == 0
            and num_pieces[PieceType.WHITE_PAWN] == 0
            and num_pieces[PieceType.BLACK_PAWN] == 0
        ):
            white_knights = num_pieces[PieceType.WHITE_KNIGHT]
            black_knights = num_pieces[PieceType.BLACK_KNIGHT]
            white_bishops = num_pieces[PieceType.WHITE_BISHOP]
            black_bishops = num_pieces[PieceType.BLACK_BISHOP]

            if (
                white_knights + white_bishops <= 1
                and black_knights + black_bishops <= 1
            ):
                return GameState.INSUFFICIENT_MATERIAL, None

        return GameState.NORMAL, None

    def play(self) -> None:
        self.board.show()

        while True:
            game_state, winner = self.get_game_state()

            if game_state != GameState.NORMAL:
                break

            player_to_move = self.get_player_to_move()
            self.board = player_to_move.do_move(self.board)
            self.board.show()

        self.board.show()

        if game_state == GameState.NORMAL:
            # Should never happen
            assert False

        elif game_state == GameState.STALEMATE:
            print("Draw by stalemate.")

        elif game_state == GameState.CHECKMATE:
            assert winner
            print(f"{winner.name} won by checkmate.")

        elif game_state == GameState.INSUFFICIENT_MATERIAL:
            print("Draw by insufficient material.")

        elif game_state == GameState.REPETITION:
            print("Draw by repetition.")

        elif game_state == GameState.FIFTY_MOVE_RULE:
            print("Draw by the 50 move rule.")

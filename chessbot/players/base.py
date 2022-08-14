from chessbot.board import Board
from chessbot.enums import Color


class BasePlayer:
    def __init__(self, color: Color) -> None:
        assert color != Color.NOBODY
        self.color = color

    def do_move(self, board: Board) -> Board:
        raise NotImplementedError

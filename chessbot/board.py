from typing import Any, Final, Iterable, List, Tuple

from chessbot.board_printer import print_board
from chessbot.constants import (
    BISHOP_DIRECTIONS,
    BOARD_START_FIELDS,
    KING_DELTAS,
    KNIGHT_DELTAS,
    QUEEN_DIRECTIONS,
    ROOK_DIRECTIONS,
)
from chessbot.enums import Color, PieceType, Square
from chessbot.exceptions import InvalidSquareException


class Board:
    def __init__(self, turn: Color, fields: Iterable[PieceType]) -> None:
        self.fields: Final[Tuple[PieceType, ...]] = tuple(fields)
        self.turn: Final[Color] = turn

        self.validate()

    def validate(self) -> None:
        assert self.turn != Color.NOBODY
        assert len(self.fields) == 64

    @staticmethod
    def empty() -> "Board":
        empty_fields = [PieceType.EMPTY] * 64
        return Board(turn=Color.WHITE, fields=empty_fields)

    @staticmethod
    def start() -> "Board":
        return Board(turn=Color.WHITE, fields=BOARD_START_FIELDS)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False

        return all(
            [
                self.turn == other.turn,
                self.fields == other.fields,
            ]
        )

    def __hash__(self) -> int:
        return hash((self.fields, self.turn))

    def move_piece(self, from_: Square, to: Square) -> "Board":
        # we can't only move our own pieces
        assert self.get_piece_color(from_) == self.turn

        # we can't capture our own pieces
        assert self.get_piece_color(to) != self.turn

        # NOTE: copying into a list allows modification
        # self.fields won't (and can't) be changed
        fields = list(self.fields)

        fields[to] = fields[from_]
        fields[from_] = PieceType.EMPTY
        return Board(turn=self.turn.opponent(), fields=fields)

    def get_piece_color(self, square: Square) -> Color:
        return self.fields[square].get_color()

    def show(self, *args: Any, **kwargs: Any) -> None:
        print_board(self, *args, **kwargs)

    def find_pieces(self, piece_type: PieceType) -> List[Square]:
        squares: List[Square] = []
        for square in range(0, 64):
            if self.fields[square] == piece_type:
                squares.append(Square(square))
        return squares

    def get_knight_moves(self, square: Square) -> List["Board"]:
        x, y = square.get_xy()

        children: List["Board"] = []

        for dx, dy in KNIGHT_DELTAS:
            move_x = x + dx
            move_y = y + dy

            try:
                move_square = Square.from_xy(move_x, move_y)
            except InvalidSquareException:
                # we're walking off the board
                continue

            if self.get_piece_color(move_square) == self.turn:
                # we're about to capture our own piece
                continue

            children.append(self.move_piece(square, move_square))

        return children

    def get_king_moves(self, square: Square) -> List["Board"]:
        x, y = square.get_xy()

        children: List["Board"] = []

        for dx, dy in KING_DELTAS:
            move_x = x + dx
            move_y = y + dy

            try:
                move_square = Square.from_xy(move_x, move_y)
            except InvalidSquareException:
                # we're walking off the board
                continue

            if self.get_piece_color(move_square) == self.turn:
                # we're about to capture our own piece
                continue

            children.append(self.move_piece(square, move_square))

        return children

    def get_range_moves_one_direction(
        self,
        square: Square,
        dx: int,
        dy: int,
    ) -> List["Board"]:
        x, y = square.get_xy()

        if dx > 0:
            max_dx = 7 - x
        elif dx < 0:
            max_dx = x
        else:
            max_dx = 8

        if dy > 0:
            max_dy = 7 - y
        elif dy < 0:
            max_dy = y
        else:
            max_dy = 8

        max_distance = min(max_dx, max_dy)

        children: List["Board"] = []

        for distance in range(1, max_distance + 1):
            move_x = x + (dx * distance)
            move_y = y + (dy * distance)

            move_square = Square.from_xy(move_x, move_y)

            target_piece_color = self.get_piece_color(move_square)

            if target_piece_color == self.turn:
                # we cannot take our own piece
                break

            # target square is empty or has opponent piece

            children.append(self.move_piece(square, move_square))

            if target_piece_color == self.turn.opponent():
                # we captured a piece from the opponent
                # meaning we cannot move further in same direction
                break

        return children

    def get_rook_moves(self, square: Square) -> List["Board"]:
        children: List["Board"] = []
        for dx, dy in ROOK_DIRECTIONS:
            children += self.get_range_moves_one_direction(square, dx, dy)
        return children

    def get_bishop_moves(self, square: Square) -> List["Board"]:
        children: List["Board"] = []
        for dx, dy in BISHOP_DIRECTIONS:
            children += self.get_range_moves_one_direction(square, dx, dy)
        return children

    def get_queen_moves(self, square: Square) -> List["Board"]:
        children: List["Board"] = []
        for dx, dy in QUEEN_DIRECTIONS:
            children += self.get_range_moves_one_direction(square, dx, dy)
        return children

    def get_pawn_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

    def get_castling_moves(self) -> List["Board"]:
        return []  # TODO

    def is_checked(self) -> bool:
        """
        Returns whether the king of the player to move is under attack
        """
        return False  # TODO

    def is_checkmate(self) -> bool:
        """
        Returns whether the king of the player to move is checkmated
        """
        return False  # TODO

    def get_moves(self) -> List["Board"]:
        moves: List["Board"] = []

        if self.turn == Color.WHITE:
            king_squares = self.find_pieces(PieceType.WHITE_KING)
            knight_squares = self.find_pieces(PieceType.WHITE_KNIGHT)
            rook_squares = self.find_pieces(PieceType.WHITE_ROOK)
            bishop_squares = self.find_pieces(PieceType.WHITE_BISHOP)
            queen_squares = self.find_pieces(PieceType.WHITE_QUEEN)
            pawn_squares = self.find_pieces(PieceType.WHITE_PAWN)
        else:
            assert self.turn == Color.BLACK
            king_squares = self.find_pieces(PieceType.BLACK_KING)
            knight_squares = self.find_pieces(PieceType.BLACK_KNIGHT)
            rook_squares = self.find_pieces(PieceType.BLACK_ROOK)
            bishop_squares = self.find_pieces(PieceType.BLACK_BISHOP)
            queen_squares = self.find_pieces(PieceType.BLACK_QUEEN)
            pawn_squares = self.find_pieces(PieceType.BLACK_PAWN)

        for king_square in king_squares:
            moves += self.get_king_moves(king_square)

        for knight_square in knight_squares:
            moves += self.get_knight_moves(knight_square)

        for rook_square in rook_squares:
            moves += self.get_rook_moves(rook_square)

        for bishop_square in bishop_squares:
            moves += self.get_bishop_moves(bishop_square)

        for queen_square in queen_squares:
            moves += self.get_queen_moves(queen_square)

        for pawn_square in pawn_squares:
            moves += self.get_pawn_moves(pawn_square)

        moves += self.get_castling_moves()

        return moves

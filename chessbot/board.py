from copy import deepcopy
from typing import Any, List

from chessbot.board_printer import print_board
from chessbot.enums import Color, PieceType, Square


class Board:
    def __init__(self) -> None:
        self.fields: List[PieceType] = [PieceType.EMPTY] * 64
        self.turn = Color.WHITE

    @staticmethod
    def empty() -> "Board":
        return Board()

    @staticmethod
    def start() -> "Board":
        board = Board.empty()

        board.fields[Square.A8] = PieceType.BLACK_ROOK
        board.fields[Square.H8] = PieceType.BLACK_ROOK
        board.fields[Square.B8] = PieceType.BLACK_KNIGHT
        board.fields[Square.G8] = PieceType.BLACK_KNIGHT
        board.fields[Square.C8] = PieceType.BLACK_BISHOP
        board.fields[Square.F8] = PieceType.BLACK_BISHOP
        board.fields[Square.D8] = PieceType.BLACK_QUEEN
        board.fields[Square.E8] = PieceType.BLACK_KING

        for square in range(Square.A7, Square.A6):
            board.fields[square] = PieceType.BLACK_PAWN

        board.fields[Square.A1] = PieceType.WHITE_ROOK
        board.fields[Square.H1] = PieceType.WHITE_ROOK
        board.fields[Square.B1] = PieceType.WHITE_KNIGHT
        board.fields[Square.G1] = PieceType.WHITE_KNIGHT
        board.fields[Square.C1] = PieceType.WHITE_BISHOP
        board.fields[Square.F1] = PieceType.WHITE_BISHOP
        board.fields[Square.D1] = PieceType.WHITE_QUEEN
        board.fields[Square.E1] = PieceType.WHITE_KING

        for square in range(Square.A2, Square.A1):
            board.fields[square] = PieceType.WHITE_PAWN

        return board

    def copy(self) -> "Board":
        return deepcopy(self)

    def show(self, *args: Any, **kwargs: Any) -> None:
        print_board(self, *args, **kwargs)

    def find_pieces(self, piece_type: PieceType) -> List[Square]:
        squares: List[Square] = []
        for square in range(0, 64):
            if self.fields[square] == piece_type:
                squares.append(Square(square))
        return squares

    def get_king_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

    def get_knight_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

    def get_rook_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

    def get_bishop_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

    def get_queen_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

    def get_pawn_moves(self, square: Square) -> List["Board"]:
        return []  # TODO

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

        return moves

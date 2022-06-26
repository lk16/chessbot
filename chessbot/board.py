from copy import deepcopy
from typing import List

from chessbot.board_printer import print_board
from chessbot.enums import Color, PieceType, Square


class Board:
    def __init__(self) -> None:
        self.fields = [PieceType.EMPTY] * 64

        self.fields[Square.A8] = PieceType.BLACK_ROOK
        self.fields[Square.H8] = PieceType.BLACK_ROOK
        self.fields[Square.B8] = PieceType.BLACK_KNIGHT
        self.fields[Square.G8] = PieceType.BLACK_KNIGHT
        self.fields[Square.C8] = PieceType.BLACK_BISHOP
        self.fields[Square.F8] = PieceType.BLACK_BISHOP
        self.fields[Square.D8] = PieceType.BLACK_KING
        self.fields[Square.E8] = PieceType.BLACK_QUEEN

        for square in range(Square.A7, Square.A6):
            self.fields[square] = PieceType.BLACK_PAWN

        self.fields[Square.A1] = PieceType.WHITE_ROOK
        self.fields[Square.H1] = PieceType.WHITE_ROOK
        self.fields[Square.B1] = PieceType.WHITE_KNIGHT
        self.fields[Square.G1] = PieceType.WHITE_KNIGHT
        self.fields[Square.C1] = PieceType.WHITE_BISHOP
        self.fields[Square.F1] = PieceType.WHITE_BISHOP
        self.fields[Square.D1] = PieceType.WHITE_KING
        self.fields[Square.E1] = PieceType.WHITE_QUEEN

        for square in range(Square.A2, Square.A1):
            self.fields[square] = PieceType.WHITE_PAWN

        self.turn = Color.WHITE

        # TODO add castling
        # TODO add en passant

    def copy(self) -> "Board":
        return deepcopy(self)

    def show(self) -> None:
        print_board(self)

    def find_pieces(self, piece_type: PieceType) -> List[Square]:
        squares: List[Square] = []
        for square in range(0, 64):
            if self.fields[square] == piece_type:
                squares.append(Square(square))
        return squares

    def get_white_pawn_moves(self, pawn_square: Square) -> List["Board"]:
        moves: List[Board] = []

        pawn_rank = pawn_square.rank()

        if pawn_rank < 7:
            # move forward
            if self.fields[pawn_square - 8] == PieceType.EMPTY:
                move = self.copy()
                move.fields[pawn_square] = PieceType.EMPTY
                move.fields[pawn_square - 8] = PieceType.WHITE_PAWN
                moves.append(move)

            # move 2 forward from start rank
            if pawn_rank == 2:
                if (
                    self.fields[pawn_square - 8] == PieceType.EMPTY
                    and self.fields[pawn_square - 16] == PieceType.EMPTY
                ):
                    move = self.copy()
                    move.fields[pawn_square] = PieceType.EMPTY
                    move.fields[pawn_square - 16] = PieceType.WHITE_PAWN
                    moves.append(move)

            # TODO capture en passent

        elif pawn_rank == 7:
            # TODO promote
            pass

        # TODO regular capture

        return moves

    def get_children(self) -> List["Board"]:
        moves: List["Board"] = []

        if self.turn == Color.WHITE:
            white_pawn_squares = self.find_pieces(PieceType.WHITE_PAWN)

            for white_pawn_square in white_pawn_squares:
                moves += self.get_white_pawn_moves(white_pawn_square)

            # TODO compute moves for other white pieces

        else:
            # TODO compute moves for black pieces
            pass

        return moves

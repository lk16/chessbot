from copy import deepcopy
from enum import IntEnum
from typing import List


class Square(IntEnum):
    A8 = 0
    B8 = 1
    C8 = 2
    D8 = 3
    E8 = 4
    F8 = 5
    G8 = 6
    H8 = 7
    A7 = 8
    B7 = 9
    C7 = 10
    D7 = 11
    E7 = 12
    F7 = 13
    G7 = 14
    H7 = 15
    A6 = 16
    B6 = 17
    C6 = 18
    D6 = 19
    E6 = 20
    F6 = 21
    G6 = 22
    H6 = 23
    A5 = 24
    B5 = 25
    C5 = 26
    D5 = 27
    E5 = 28
    F5 = 29
    G5 = 30
    H5 = 31
    A4 = 32
    B4 = 33
    C4 = 34
    D4 = 35
    E4 = 36
    F4 = 37
    G4 = 38
    H4 = 39
    A3 = 40
    B3 = 41
    C3 = 42
    D3 = 43
    E3 = 44
    F3 = 45
    G3 = 46
    H3 = 47
    A2 = 48
    B2 = 49
    C2 = 50
    D2 = 51
    E2 = 52
    F2 = 53
    G2 = 54
    H2 = 55
    A1 = 56
    B1 = 57
    C1 = 58
    D1 = 59
    E1 = 60
    F1 = 61
    G1 = 62
    H1 = 63

    def rank(self) -> int:
        return 8 - (self // 8)

    def file(self) -> int:
        return self % 8


class PieceType(IntEnum):
    EMPTY = 0
    BLACK_PAWN = 1
    BLACK_ROOK = 2
    BLACK_KNIGHT = 3
    BLACK_KING = 4
    BLACK_QUEEN = 5
    BLACK_BISHOP = 6
    WHITE_PAWN = 7
    WHITE_ROOK = 8
    WHITE_KNIGHT = 9
    WHITE_KING = 10
    WHITE_QUEEN = 11
    WHITE_BISHOP = 12


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


class Board:
    def __init__(self) -> None:
        self.field = [PieceType.EMPTY] * 64

        self.field[Square.A8] = PieceType.BLACK_ROOK
        self.field[Square.H8] = PieceType.BLACK_ROOK
        self.field[Square.B8] = PieceType.BLACK_KNIGHT
        self.field[Square.G8] = PieceType.BLACK_KNIGHT
        self.field[Square.C8] = PieceType.BLACK_BISHOP
        self.field[Square.F8] = PieceType.BLACK_BISHOP
        self.field[Square.D8] = PieceType.BLACK_KING
        self.field[Square.E8] = PieceType.BLACK_QUEEN

        for square in range(Square.A7, Square.A6):
            self.field[square] = PieceType.BLACK_PAWN

        self.field[Square.A1] = PieceType.WHITE_ROOK
        self.field[Square.H1] = PieceType.WHITE_ROOK
        self.field[Square.B1] = PieceType.WHITE_KNIGHT
        self.field[Square.G1] = PieceType.WHITE_KNIGHT
        self.field[Square.C1] = PieceType.WHITE_BISHOP
        self.field[Square.F1] = PieceType.WHITE_BISHOP
        self.field[Square.D1] = PieceType.WHITE_KING
        self.field[Square.E1] = PieceType.WHITE_QUEEN

        for square in range(Square.A2, Square.A1):
            self.field[square] = PieceType.WHITE_PAWN

        self.turn = Color.WHITE

        # TODO add castling
        # TODO add en passant

    def copy(self) -> "Board":
        return deepcopy(self)

    def show(self) -> None:
        print("+-a-b-c-d-e-f-g-h-+")
        for y in range(8):
            print(f"{8-y} ", end="")
            for x in range(8):
                square = (8 * y) + x
                piece_type = self.field[square]
                if piece_type == PieceType.EMPTY:
                    print("  ", end="")
                elif piece_type == PieceType.BLACK_ROOK:
                    print("♜ ", end="")
                elif piece_type == PieceType.BLACK_KNIGHT:
                    print("♞ ", end="")
                elif piece_type == PieceType.BLACK_BISHOP:
                    print("♝ ", end="")
                elif piece_type == PieceType.BLACK_KING:
                    print("♚ ", end="")
                elif piece_type == PieceType.BLACK_QUEEN:
                    print("♛ ", end="")
                elif piece_type == PieceType.BLACK_PAWN:
                    print("♟ ", end="")
                elif piece_type == PieceType.WHITE_ROOK:
                    print("♖ ", end="")
                elif piece_type == PieceType.WHITE_KNIGHT:
                    print("♘ ", end="")
                elif piece_type == PieceType.WHITE_BISHOP:
                    print("♗ ", end="")
                elif piece_type == PieceType.WHITE_KING:
                    print("♔ ", end="")
                elif piece_type == PieceType.WHITE_QUEEN:
                    print("♕ ", end="")
                elif piece_type == PieceType.WHITE_PAWN:
                    print("♙ ", end="")
                else:
                    assert False
            print("|")
        print("+-----------------+")

    def find_pieces(self, piece_type: PieceType) -> List[Square]:
        squares: List[Square] = []
        for square in range(0, 64):
            if self.field[square] == piece_type:
                squares.append(Square(square))
        return squares

    def get_white_pawn_moves(self, pawn_square: Square) -> List["Board"]:
        moves: List[Board] = []

        pawn_rank = pawn_square.rank()

        if pawn_rank < 7:
            # move forward
            if self.field[pawn_square - 8] == PieceType.EMPTY:
                move = self.copy()
                move.field[pawn_square] = PieceType.EMPTY
                move.field[pawn_square - 8] = PieceType.WHITE_PAWN
                moves.append(move)

            # move 2 forward from start rank
            if pawn_rank == 2:
                if (
                    self.field[pawn_square - 8] == PieceType.EMPTY
                    and self.field[pawn_square - 16] == PieceType.EMPTY
                ):
                    move = self.copy()
                    move.field[pawn_square] = PieceType.EMPTY
                    move.field[pawn_square - 16] = PieceType.WHITE_PAWN
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


def main() -> None:
    board = Board()
    moves = board.get_children()

    for move in moves:
        move.show()


if __name__ == "__main__":
    main()

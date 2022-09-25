from enum import IntEnum

SQUARE_A8 = 0
SQUARE_B8 = 1
SQUARE_C8 = 2
SQUARE_D8 = 3
SQUARE_E8 = 4
SQUARE_F8 = 5
SQUARE_G8 = 6
SQUARE_H8 = 7
SQUARE_A7 = 8
SQUARE_B7 = 9
SQUARE_C7 = 10
SQUARE_D7 = 11
SQUARE_E7 = 12
SQUARE_F7 = 13
SQUARE_G7 = 14
SQUARE_H7 = 15
SQUARE_A6 = 16
SQUARE_B6 = 17
SQUARE_C6 = 18
SQUARE_D6 = 19
SQUARE_E6 = 20
SQUARE_F6 = 21
SQUARE_G6 = 22
SQUARE_H6 = 23
SQUARE_A5 = 24
SQUARE_B5 = 25
SQUARE_C5 = 26
SQUARE_D5 = 27
SQUARE_E5 = 28
SQUARE_F5 = 29
SQUARE_G5 = 30
SQUARE_H5 = 31
SQUARE_A4 = 32
SQUARE_B4 = 33
SQUARE_C4 = 34
SQUARE_D4 = 35
SQUARE_E4 = 36
SQUARE_F4 = 37
SQUARE_G4 = 38
SQUARE_H4 = 39
SQUARE_A3 = 40
SQUARE_B3 = 41
SQUARE_C3 = 42
SQUARE_D3 = 43
SQUARE_E3 = 44
SQUARE_F3 = 45
SQUARE_G3 = 46
SQUARE_H3 = 47
SQUARE_A2 = 48
SQUARE_B2 = 49
SQUARE_C2 = 50
SQUARE_D2 = 51
SQUARE_E2 = 52
SQUARE_F2 = 53
SQUARE_G2 = 54
SQUARE_H2 = 55
SQUARE_A1 = 56
SQUARE_B1 = 57
SQUARE_C1 = 58
SQUARE_D1 = 59
SQUARE_E1 = 60
SQUARE_F1 = 61
SQUARE_G1 = 62
SQUARE_H1 = 63


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

    def get_color(self) -> "Color":
        if self == PieceType.EMPTY:
            return Color.NOBODY

        if self <= PieceType.BLACK_BISHOP:
            return Color.BLACK

        return Color.WHITE


class Color(IntEnum):
    BLACK = 0
    WHITE = 1
    NOBODY = 2

    def opponent(self) -> "Color":
        if self == Color.NOBODY:
            raise ValueError("Cannot take opponent of NOBODY.")

        if self == Color.WHITE:
            return Color.BLACK

        return Color.WHITE


class Castling(IntEnum):
    WHITE_SHORT = 0
    WHITE_LONG = 1
    BLACK_SHORT = 2
    BLACK_LONG = 3


class GameState(IntEnum):
    NORMAL = 0
    STALEMATE = 1
    CHECKMATE = 2
    INSUFFICIENT_MATERIAL = 3
    REPETITION = 4
    FIFTY_MOVE_RULE = 5

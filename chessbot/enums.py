from enum import IntEnum
from typing import Tuple


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

    def get_xy(self) -> Tuple[int, int]:
        x = self % 8
        y = self // 8
        return x, y

    @staticmethod
    def from_xy(x: int, y: int) -> "Square":
        return Square(8 * y + x)


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

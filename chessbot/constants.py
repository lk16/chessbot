from chessbot.enums import PieceType

BOARD_START_FIELDS = (
    (
        PieceType.BLACK_ROOK,
        PieceType.BLACK_KNIGHT,
        PieceType.BLACK_BISHOP,
        PieceType.BLACK_QUEEN,
        PieceType.BLACK_KING,
        PieceType.BLACK_BISHOP,
        PieceType.BLACK_KNIGHT,
        PieceType.BLACK_ROOK,
    )
    + (8 * (PieceType.BLACK_PAWN,))
    + (32 * (PieceType.EMPTY,))
    + (8 * (PieceType.WHITE_PAWN,))
    + (
        PieceType.WHITE_ROOK,
        PieceType.WHITE_KNIGHT,
        PieceType.WHITE_BISHOP,
        PieceType.WHITE_QUEEN,
        PieceType.WHITE_KING,
        PieceType.WHITE_BISHOP,
        PieceType.WHITE_KNIGHT,
        PieceType.WHITE_ROOK,
    )
)


KNIGHT_DELTAS = [
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
]


KING_DELTAS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


ROOK_DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
]


BISHOP_DIRECTIONS = [
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS

PROMOTION_PIECE_TYPES = [
    [  # BLACK
        PieceType.BLACK_KNIGHT,
        PieceType.BLACK_BISHOP,
        PieceType.BLACK_QUEEN,
        PieceType.BLACK_ROOK,
    ],
    [  # WHITE
        PieceType.WHITE_KNIGHT,
        PieceType.WHITE_BISHOP,
        PieceType.WHITE_QUEEN,
        PieceType.WHITE_ROOK,
    ],
]

PRE_PROMOTION_Y = [
    6,  # BLACK
    1,  # WHITE
]


PAWN_START_Y = [
    1,  # BLACK
    6,  # WHITE
]

PAWN_DELTA_Y = [
    1,  # BLACK
    -1,  # WHITE
]

EN_PASSENT_CAPTURER_Y = [
    3,  # BLACK
    4,  # WHITE
]

FEN_CHAR_PIECE_TYPES = {
    "b": PieceType.BLACK_BISHOP,
    "B": PieceType.WHITE_BISHOP,
    "k": PieceType.BLACK_KING,
    "K": PieceType.WHITE_KING,
    "n": PieceType.BLACK_KNIGHT,
    "N": PieceType.WHITE_KNIGHT,
    "p": PieceType.BLACK_PAWN,
    "P": PieceType.WHITE_PAWN,
    "q": PieceType.BLACK_QUEEN,
    "Q": PieceType.WHITE_QUEEN,
    "r": PieceType.BLACK_ROOK,
    "R": PieceType.WHITE_ROOK,
}

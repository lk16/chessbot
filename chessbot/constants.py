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

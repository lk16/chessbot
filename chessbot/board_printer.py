from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional, Set

from chessbot.enums import Color, PieceType

if TYPE_CHECKING:
    from chessbot.board import Board


RESET_COLORS = "\033[0m"


# Matches Bash text color codes
# Source: https://misc.flogisoft.com/bash/tip_colors_and_formatting
class BashColor(IntEnum):
    DARK_SQUARE = 172
    LIGHT_SQUARE = 222
    EDGE = 52
    EDGE_TEXT = 7
    WHITE_PIECE = 20
    BLACK_PIECE = 0
    HIGHLIGHT_RED = 197


def colorize(
    text: str, bg: Optional[BashColor] = None, fg: Optional[BashColor] = None
) -> str:
    colorized = ""

    if bg:
        colorized += f"\033[30;48;5;{bg.value}m"

    if fg:
        colorized += f"\033[38;5;{fg.value}m"

    colorized += text
    colorized += RESET_COLORS

    return colorized


def v_split(left: Optional[BashColor] = None, right: Optional[BashColor] = None) -> str:
    if not (left or right):
        return " "

    if right and not left:
        return colorize("▐", fg=right)

    return colorize("▌", fg=left, bg=right)


def colorize_piece(piece: PieceType, bg: BashColor) -> str:
    text = {
        PieceType.EMPTY: " ",
        PieceType.BLACK_PAWN: "♟",
        PieceType.BLACK_ROOK: "♜",
        PieceType.BLACK_KNIGHT: "♞",
        PieceType.BLACK_KING: "♚",
        PieceType.BLACK_QUEEN: "♛",
        PieceType.BLACK_BISHOP: "♝",
        PieceType.WHITE_PAWN: "♟",
        PieceType.WHITE_ROOK: "♜",
        PieceType.WHITE_KNIGHT: "♞",
        PieceType.WHITE_KING: "♚",
        PieceType.WHITE_QUEEN: "♛",
        PieceType.WHITE_BISHOP: "♝",
    }[piece]

    piece_color = {
        Color.NOBODY: None,
        Color.BLACK: BashColor.BLACK_PIECE,
        Color.WHITE: BashColor.WHITE_PIECE,
    }[piece.get_color()]

    return colorize(text, bg=bg, fg=piece_color)


def print_board(board: "Board", red: Set[int] = set()) -> None:

    # background color by square id (0 up to 63)
    square_colors: List[BashColor] = []

    for y in range(8):
        for x in range(8):
            is_light = (x + y) % 2 == 0
            square = 8 * y + x

            if square in red:
                color = BashColor.HIGHLIGHT_RED
            elif is_light:
                color = BashColor.LIGHT_SQUARE
            else:
                color = BashColor.DARK_SQUARE

            square_colors.append(color)

    output = v_split(right=BashColor.EDGE)
    output += colorize("  a b c d e f g h  ", bg=BashColor.EDGE, fg=BashColor.EDGE_TEXT)
    output += v_split(left=BashColor.EDGE)
    output += "\n"

    for y in range(8):
        output += v_split(right=BashColor.EDGE)
        output += colorize(str(8 - y), bg=BashColor.EDGE, fg=BashColor.EDGE_TEXT)

        for x in range(8):
            square_color = square_colors[8 * y + x]

            if x == 0:
                left = BashColor.EDGE
            else:
                left = square_colors[8 * y + x - 1]

            output += v_split(left=left, right=square_color)
            output += colorize_piece(board.fields[8 * y + x], bg=square_color)

        row_last_square_color = square_colors[8 * y + 7]

        output += v_split(left=row_last_square_color, right=BashColor.EDGE)
        output += colorize(" ", bg=BashColor.EDGE)
        output += v_split(left=BashColor.EDGE)
        output += "\n"

    output += v_split(right=BashColor.EDGE)
    output += colorize("                   ", bg=BashColor.EDGE, fg=BashColor.EDGE_TEXT)
    output += v_split(left=BashColor.EDGE)
    output += "\n"

    print(output)

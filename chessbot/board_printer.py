from enum import IntEnum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from chessbot.board import Board


RESET_COLORS = "\033[0m"


# Matches Bash text color codes
# Source: https://misc.flogisoft.com/bash/tip_colors_and_formatting
class Color(IntEnum):
    DARK_SQUARE = 172
    LIGHT_SQUARE = 222
    EDGE = 52
    EDGE_TEXT = 7


def colorize(text: str, bg: Optional[Color] = None, fg: Optional[Color] = None) -> str:
    colorized = ""

    if bg:
        colorized += f"\033[30;48;5;{bg.value}m"

    if fg:
        colorized += f"\033[38;5;{fg.value}m"

    colorized += text
    colorized += RESET_COLORS

    return colorized


def v_split(left: Optional[Color] = None, right: Optional[Color] = None) -> str:
    if not (left or right):
        return " "

    if right and not left:
        return colorize("▐", fg=right)

    return colorize("▌", fg=left, bg=right)


def print_board(board: "Board") -> None:
    output = v_split(right=Color.EDGE)
    output += colorize("  a b c d e f g h  ", bg=Color.EDGE, fg=Color.EDGE_TEXT)
    output += v_split(left=Color.EDGE)
    output += "\n"

    for y in range(8):
        output += v_split(right=Color.EDGE)
        output += colorize(str(y + 1), bg=Color.EDGE, fg=Color.EDGE_TEXT)

        for x in range(8):
            if x == 0:
                left = Color.EDGE
            elif (x + y) % 2 == 0:
                left = Color.DARK_SQUARE
            else:
                left = Color.LIGHT_SQUARE

            if (x + y) % 2 == 0:
                right = Color.LIGHT_SQUARE
            else:
                right = Color.DARK_SQUARE

            output += v_split(left=left, right=right)

            field = str(board.fields[y * 8 + x])
            output += colorize(field, bg=right)

        if y % 2 == 0:
            output += v_split(left=Color.DARK_SQUARE, right=Color.EDGE)
        else:
            output += v_split(left=Color.LIGHT_SQUARE, right=Color.EDGE)

        output += colorize(" ", bg=Color.EDGE)
        output += v_split(left=Color.EDGE)
        output += "\n"

    output += v_split(right=Color.EDGE)
    output += colorize("                   ", bg=Color.EDGE, fg=Color.EDGE_TEXT)
    output += v_split(left=Color.EDGE)
    output += "\n"

    print(output)

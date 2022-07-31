from typing import Any, Dict, Final, Iterable, List, Optional, Tuple

from chessbot.board_printer import print_board
from chessbot.constants import (
    BISHOP_DIRECTIONS,
    BOARD_START_FIELDS,
    CASTLING_TO_FEN_CHAR,
    EN_PASSENT_CAPTURER_Y,
    FEN_CHAR_TO_CASTLING,
    FEN_CHAR_TO_PIECE_TYPE,
    KING_DELTAS,
    KNIGHT_DELTAS,
    PAWN_DELTA_Y,
    PAWN_START_Y,
    PIECE_TYPE_TO_FEN_CHAR,
    PRE_PROMOTION_Y,
    PROMOTION_PIECE_TYPES,
    QUEEN_DIRECTIONS,
    ROOK_DIRECTIONS,
)
from chessbot.enums import Castling, Color, PieceType, Square
from chessbot.exceptions import InvalidSquareException


class Board:
    def __init__(
        self,
        turn: Color,
        fields: Iterable[PieceType],
        en_passent_column: Optional[int] = None,
        castling: Optional[Iterable[bool]] = None,
    ) -> None:
        if castling:
            castling_tuple = tuple(castling)
        else:
            castling_tuple = 4 * (False,)

        self.fields: Final[Tuple[PieceType, ...]] = tuple(fields)
        self.turn: Final[Color] = turn
        self.en_passent_column: Optional[int] = en_passent_column
        self.castling: Final[Tuple[bool, ...]] = castling_tuple
        self.validate()

    def validate(self) -> None:
        assert self.turn != Color.NOBODY
        assert len(self.fields) == 64
        assert len(self.castling) == 4

    @staticmethod
    def empty() -> "Board":
        empty_fields = [PieceType.EMPTY] * 64
        return Board(turn=Color.WHITE, fields=empty_fields)

    @staticmethod
    def start() -> "Board":
        return Board(turn=Color.WHITE, fields=BOARD_START_FIELDS, castling=4 * [True])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False

        return all(
            [
                self.turn == other.turn,
                self.fields == other.fields,
                self.en_passent_column == other.en_passent_column,
                self.castling == other.castling,
            ]
        )

    @staticmethod
    def from_fen(fen: str) -> "Board":
        split_fen = fen.split(" ")
        assert len(split_fen) == 6

        (
            fen_pieces,
            fen_turn,
            fen_castling,
            fen_en_passent,
            pawn_clock,
            full_move_count,
        ) = split_fen

        fen_piece_rows = fen_pieces.split("/")
        assert len(fen_piece_rows) == 8

        fields = 64 * [PieceType.EMPTY]

        for y, row in enumerate(fen_piece_rows):
            x = 0
            for char in row:
                if char.isnumeric():
                    x += int(char)
                else:
                    fields[8 * y + x] = FEN_CHAR_TO_PIECE_TYPE[char]
                    x += 1

            assert x == 8

        if fen_turn == "b":
            turn = Color.BLACK
        elif fen_turn == "w":
            turn = Color.WHITE
        else:
            assert False

        castling = 4 * [False]
        if fen_castling != "-":
            for char in fen_castling:
                castling[FEN_CHAR_TO_CASTLING[char]] = True

        if fen_en_passent == "-":
            en_passent_column = None
        else:
            assert fen_en_passent[0] in "abcdefgh"
            en_passent_column = ord(fen_en_passent[0]) - ord("a")

        # TODO use
        _ = pawn_clock
        _ = full_move_count

        return Board(
            turn=turn,
            fields=fields,
            en_passent_column=en_passent_column,
            castling=castling,
        )

    def to_fen(self) -> str:
        fen_pieces = ""
        for y in range(8):
            empty_counter = 0
            for x in range(8):
                piece_type = self.fields[8 * y + x]

                if piece_type == PieceType.EMPTY:
                    empty_counter += 1
                else:
                    if empty_counter != 0:
                        fen_pieces += str(empty_counter)
                        empty_counter = 0
                    fen_pieces += PIECE_TYPE_TO_FEN_CHAR[piece_type]

            if empty_counter != 0:
                fen_pieces += str(empty_counter)

            if y != 7:
                fen_pieces += "/"

        if self.turn == Color.WHITE:
            fen_turn = "w"
        else:
            fen_turn = "b"

        fen_castling = ""
        for c in Castling:
            if self.castling[c]:
                fen_castling += CASTLING_TO_FEN_CHAR[c]

        if self.en_passent_column is None:
            fen_en_passent = "-"
        else:
            fen_en_passent = chr(ord("a") + self.en_passent_column)
            if self.turn == Color.WHITE:
                fen_en_passent += "6"
            else:
                fen_en_passent += "3"

        # TODO set when created
        pawn_clock = "0"
        full_move_count = "0"

        return " ".join(
            [
                fen_pieces,
                fen_turn,
                fen_castling,
                fen_en_passent,
                pawn_clock,
                full_move_count,
            ]
        )

    def editor_link(self) -> str:
        fen = self.to_fen()
        return "https://lichess.org/editor/" + "_".join(fen.split(" ")) + "?color=white"

    def __hash__(self) -> int:
        return hash(self.to_fen())

    def move_piece(
        self,
        from_: Square,
        to: Square,
        en_passent_column: Optional[int] = None,
        disallow_castling: Optional[List[Castling]] = None,
    ) -> "Board":
        # we can't only move our own pieces
        assert self.get_piece_color(from_) == self.turn

        # we can't capture our own pieces
        assert self.get_piece_color(to) != self.turn

        # NOTE: copying into a list allows modification
        # self.fields won't (and can't) be changed
        fields = list(self.fields)

        castling = list(self.castling)
        if disallow_castling is not None:
            for disallow_castling_item in disallow_castling:
                castling[disallow_castling_item] = False

        fields[to] = fields[from_]
        fields[from_] = PieceType.EMPTY
        return Board(
            turn=self.turn.opponent(),
            fields=fields,
            en_passent_column=en_passent_column,
            castling=castling,
        )

    def promote(self, from_: Square, to: Square, piece_type: PieceType) -> "Board":
        fields = list(self.fields)
        fields[from_] = PieceType.EMPTY
        fields[to] = piece_type
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

            if self.turn == Color.WHITE:
                disallow_castling = [Castling.WHITE_SHORT, Castling.WHITE_LONG]
            else:
                disallow_castling = [Castling.BLACK_SHORT, Castling.BLACK_LONG]

            child = self.move_piece(
                square,
                move_square,
                disallow_castling=disallow_castling,
            )

            children.append(child)

        return children

    def get_range_moves_one_direction(
        self,
        square: Square,
        dx: int,
        dy: int,
        disallow_castling: Optional[List[Castling]] = None,
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

            child = self.move_piece(
                square,
                move_square,
                disallow_castling=disallow_castling,
            )

            children.append(child)

            if target_piece_color == self.turn.opponent():
                # we captured a piece from the opponent
                # meaning we cannot move further in same direction
                break

        return children

    def get_rook_moves(self, square: Square) -> List["Board"]:
        disallow_castling = None

        if self.turn == Color.WHITE:
            if square == Square.A1:
                disallow_castling = [Castling.WHITE_LONG]
            elif square == Square.H1:
                disallow_castling = [Castling.WHITE_SHORT]
        else:
            if square == Square.A8:
                disallow_castling = [Castling.BLACK_LONG]
            elif square == Square.H8:
                disallow_castling = [Castling.BLACK_SHORT]

        children: List["Board"] = []
        for dx, dy in ROOK_DIRECTIONS:
            children += self.get_range_moves_one_direction(
                square, dx, dy, disallow_castling=disallow_castling
            )
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

    def get_pawn_capture_moves(self, square: Square) -> List["Board"]:
        x, y = square.get_xy()

        capture_squares: List[Square] = []
        moves: List["Board"] = []

        pawn_delta = PAWN_DELTA_Y[self.turn]

        if x != 0:
            left_capture_square = Square.from_xy(x - 1, y + pawn_delta)
            capture_squares.append(left_capture_square)

        if x != 7:
            right_capture_square = Square.from_xy(x + 1, y + pawn_delta)
            capture_squares.append(right_capture_square)

        pre_promotion_y = PRE_PROMOTION_Y[self.turn]

        for capture_square in capture_squares:
            if self.get_piece_color(capture_square) == self.turn.opponent():

                if y == pre_promotion_y:
                    for piece_type in PROMOTION_PIECE_TYPES[self.turn]:
                        moves.append(self.promote(square, capture_square, piece_type))
                else:
                    moves.append(self.move_piece(square, capture_square))

        return moves

    def get_pawn_push_moves(self, square: Square) -> List["Board"]:
        """
        Return moves of pawn moving forward including promotion
        """
        x, y = square.get_xy()

        pawn_delta = PAWN_DELTA_Y[self.turn]
        forward = Square.from_xy(x, y + pawn_delta)

        start_y = PAWN_START_Y[self.turn]
        pre_promotion_y = PRE_PROMOTION_Y[self.turn]

        moves: List["Board"] = []

        if self.get_piece_color(forward) == Color.NOBODY:
            if y != pre_promotion_y:
                moves.append(self.move_piece(square, forward))

            if y == start_y:
                two_forward = Square.from_xy(x, y + (2 * pawn_delta))
                if self.get_piece_color(two_forward) == Color.NOBODY:
                    moves.append(
                        self.move_piece(square, two_forward, en_passent_column=x)
                    )

            if y == pre_promotion_y:
                for piece_type in PROMOTION_PIECE_TYPES[self.turn]:
                    moves.append(self.promote(square, forward, piece_type))

        return moves

    def get_pawn_en_passent_moves(self, square: Square) -> List["Board"]:
        x, y = square.get_xy()

        if not self.en_passent_column:
            return []

        if y != EN_PASSENT_CAPTURER_Y[self.turn]:
            return []

        if x not in [self.en_passent_column + 1, self.en_passent_column - 1]:
            return []

        move_square = Square.from_xy(
            self.en_passent_column,
            y + PAWN_DELTA_Y[self.turn],
        )

        if self.fields[move_square] != PieceType.EMPTY:
            return []

        en_passent_square = Square.from_xy(
            self.en_passent_column,
            EN_PASSENT_CAPTURER_Y[self.turn],
        )

        fields = list(self.fields)
        fields[move_square] = self.fields[square]
        fields[en_passent_square] = PieceType.EMPTY
        fields[square] = PieceType.EMPTY

        move = Board(fields=fields, turn=self.turn.opponent())
        return [move]

    def get_pawn_moves(self, square: Square) -> List["Board"]:
        return (
            self.get_pawn_push_moves(square)
            + self.get_pawn_capture_moves(square)
            + self.get_pawn_en_passent_moves(square)
        )

    def get_white_castling_moves(self) -> List["Board"]:

        # The king is not currently in check.
        if self.is_checked(self.turn):
            return []

        moves: List["Board"] = []

        # Neither the king nor the rook has previously moved.
        # There are no pieces between the king and the rook.
        # The king does not pass through a square that is attacked by an opposing piece.
        if (
            self.castling[Castling.WHITE_SHORT]
            and self.fields[Square.F1] == PieceType.EMPTY
            and self.fields[Square.G1] == PieceType.EMPTY
            and not self.is_attacked(Square.F1, self.turn.opponent())
        ):
            # we CAN castle short as white

            fields = list(self.fields)
            fields[Square.E1] = PieceType.EMPTY
            fields[Square.F1] = PieceType.WHITE_ROOK
            fields[Square.G1] = PieceType.WHITE_KING
            fields[Square.H1] = PieceType.EMPTY

            castling = list(self.castling)
            castling[Castling.WHITE_SHORT] = False
            castling[Castling.WHITE_LONG] = False

            short_castle_move = Board(
                turn=self.turn.opponent(),
                fields=fields,
                castling=castling,
            )

            moves.append(short_castle_move)

        # Neither the king nor the rook has previously moved.
        # There are no pieces between the king and the rook.
        # The king does not pass through a square that is attacked by an opposing piece.
        if (
            self.castling[Castling.WHITE_LONG]
            and self.fields[Square.B1] == PieceType.EMPTY
            and self.fields[Square.C1] == PieceType.EMPTY
            and self.fields[Square.D1] == PieceType.EMPTY
            and not self.is_attacked(Square.D1, self.turn.opponent())
        ):
            # we CAN castle long as white

            fields = list(self.fields)
            fields[Square.A1] = PieceType.EMPTY
            fields[Square.C1] = PieceType.WHITE_KING
            fields[Square.D1] = PieceType.WHITE_ROOK
            fields[Square.E1] = PieceType.EMPTY

            castling = list(self.castling)
            castling[Castling.WHITE_SHORT] = False
            castling[Castling.WHITE_LONG] = False

            long_castle_move = Board(
                turn=self.turn.opponent(),
                fields=fields,
                castling=castling,
            )

            moves.append(long_castle_move)

        return moves

    def get_black_castling_moves(self) -> List["Board"]:
        # The king is not currently in check.
        if self.is_checked(self.turn):
            return []

        moves: List["Board"] = []

        # Neither the king nor the rook has previously moved.
        # There are no pieces between the king and the rook.
        # The king does not pass through a square that is attacked by an opposing piece.
        if (
            self.castling[Castling.BLACK_SHORT]
            and self.fields[Square.F8] == PieceType.EMPTY
            and self.fields[Square.G8] == PieceType.EMPTY
            and not self.is_attacked(Square.F8, self.turn.opponent())
        ):
            # we CAN castle short as black

            fields = list(self.fields)
            fields[Square.E8] = PieceType.EMPTY
            fields[Square.F8] = PieceType.BLACK_ROOK
            fields[Square.G8] = PieceType.BLACK_KING
            fields[Square.H8] = PieceType.EMPTY

            castling = list(self.castling)
            castling[Castling.BLACK_SHORT] = False
            castling[Castling.BLACK_LONG] = False

            short_castle_move = Board(
                turn=self.turn.opponent(),
                fields=fields,
                castling=castling,
            )

            moves.append(short_castle_move)

        # Neither the king nor the rook has previously moved.
        # There are no pieces between the king and the rook.
        # The king does not pass through a square that is attacked by an opposing piece.
        if (
            self.castling[Castling.BLACK_LONG]
            and self.fields[Square.B8] == PieceType.EMPTY
            and self.fields[Square.C8] == PieceType.EMPTY
            and self.fields[Square.D8] == PieceType.EMPTY
            and not self.is_attacked(Square.D8, self.turn.opponent())
        ):
            # we CAN castle long as black

            fields = list(self.fields)
            fields[Square.A8] = PieceType.EMPTY
            fields[Square.C8] = PieceType.BLACK_KING
            fields[Square.D8] = PieceType.BLACK_ROOK
            fields[Square.E8] = PieceType.EMPTY

            castling = list(self.castling)
            castling[Castling.BLACK_SHORT] = False
            castling[Castling.BLACK_LONG] = False

            long_castle_move = Board(
                turn=self.turn.opponent(),
                fields=fields,
                castling=castling,
            )

            moves.append(long_castle_move)

        return moves

    def get_castling_moves(self) -> List["Board"]:
        if self.turn == Color.WHITE:
            return self.get_white_castling_moves()
        else:
            return self.get_black_castling_moves()

    def is_attacked_by_knight(self, king_square: Square, attacker: Color) -> bool:
        king_x, king_y = king_square.get_xy()

        for dx, dy in KNIGHT_DELTAS:
            knight_x = king_x + dx
            knight_y = king_y + dy

            try:
                knight_square = Square.from_xy(knight_x, knight_y)
            except InvalidSquareException:
                continue

            if attacker == Color.BLACK:
                if self.fields[knight_square] == PieceType.BLACK_KNIGHT:
                    return True
            else:
                if self.fields[knight_square] == PieceType.WHITE_KNIGHT:
                    return True

        return False

    def is_attacked_by_rook_or_queen(
        self, king_square: Square, attacker: Color
    ) -> bool:
        king_x, king_y = king_square.get_xy()

        for dx, dy in ROOK_DIRECTIONS:
            for distance in range(1, 8):
                piece_x = king_x + (dx * distance)
                piece_y = king_y + (dy * distance)

                try:
                    piece_square = Square.from_xy(piece_x, piece_y)
                except InvalidSquareException:
                    break

                piece_type = self.fields[piece_square]

                if piece_type == PieceType.EMPTY:
                    continue

                if attacker == Color.BLACK:
                    if piece_type in [PieceType.BLACK_ROOK, PieceType.BLACK_QUEEN]:
                        return True
                    else:
                        break
                else:
                    if piece_type in [PieceType.WHITE_ROOK, PieceType.WHITE_QUEEN]:
                        return True
                    else:
                        break
        return False

    def is_attacked_by_bishop_or_queen(
        self, king_square: Square, attacker: Color
    ) -> bool:
        king_x, king_y = king_square.get_xy()

        for dx, dy in BISHOP_DIRECTIONS:
            for distance in range(1, 8):
                piece_x = king_x + (dx * distance)
                piece_y = king_y + (dy * distance)

                try:
                    piece_square = Square.from_xy(piece_x, piece_y)
                except InvalidSquareException:
                    break

                piece_type = self.fields[piece_square]

                if piece_type == PieceType.EMPTY:
                    continue

                if attacker == Color.BLACK:
                    if piece_type in [PieceType.BLACK_BISHOP, PieceType.BLACK_QUEEN]:
                        return True
                    else:
                        break
                else:
                    if piece_type in [PieceType.WHITE_BISHOP, PieceType.WHITE_QUEEN]:
                        return True
                    else:
                        break

        return False

    def is_attacked_by_pawn(self, king_square: Square, attacker: Color) -> bool:
        king_x, king_y = king_square.get_xy()

        pawn_squares: List[Square] = []
        for dx in [-1, 1]:
            pawn_x = king_x + dx
            pawn_y = king_y - PAWN_DELTA_Y[attacker]

            try:
                pawn_square = Square.from_xy(pawn_x, pawn_y)
            except InvalidSquareException:
                continue

            pawn_squares.append(pawn_square)

        for pawn_square in pawn_squares:
            if attacker == Color.BLACK:
                if self.fields[pawn_square] == PieceType.BLACK_PAWN:
                    return True
            else:
                if self.fields[pawn_square] == PieceType.WHITE_PAWN:
                    return True

        return False

    def is_attacked_by_king(self, king_square: Square, attacker: Color) -> bool:
        if attacker == Color.WHITE:
            king_piecetype = PieceType.WHITE_KING
        else:
            king_piecetype = PieceType.BLACK_KING

        x, y = king_square.get_xy()

        for dx, dy in KING_DELTAS:
            try:
                attacking_king_square = Square.from_xy(x + dx, y + dy)
            except InvalidSquareException:
                continue

            if self.fields[attacking_king_square] == king_piecetype:
                return True

        return False

    def is_checked(self, color: Color) -> bool:
        """
        Returns whether the king of the player to move is under attack
        """
        assert color != Color.NOBODY

        if color == Color.WHITE:
            king_squares = self.find_pieces(PieceType.WHITE_KING)
        else:
            king_squares = self.find_pieces(PieceType.BLACK_KING)

        assert len(king_squares) == 1
        king_square = king_squares[0]

        return self.is_attacked(king_square, color.opponent())

    def is_attacked(self, square: Square, attacker: Color) -> bool:
        return (
            self.is_attacked_by_knight(square, attacker)
            or self.is_attacked_by_rook_or_queen(square, attacker)
            or self.is_attacked_by_bishop_or_queen(square, attacker)
            or self.is_attacked_by_pawn(square, attacker)
            or self.is_attacked_by_king(square, attacker)
        )

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

        safe_moves: List["Board"] = []

        for move in moves:
            if not move.is_checked(self.turn):
                safe_moves.append(move)

        return safe_moves

    def is_checkmate(self) -> bool:
        """
        Returns whether the king of the player to move is checkmated
        """
        moves = self.get_moves()
        return self.is_checked(self.turn) and len(moves) == 0

    def is_stalemate(self) -> bool:
        """
        Returns whether player to move has no moves but is not in check
        """
        moves = self.get_moves()
        return not self.is_checked(self.turn) and len(moves) == 0

    def count_piece_types(self) -> Dict[PieceType, int]:
        counts = {piece_type: 0 for piece_type in PieceType}

        for field in self.fields:
            counts[field] += 1

        return counts

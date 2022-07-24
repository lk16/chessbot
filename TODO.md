
# TODO

A chess board / position representation
- keep track where pieces are
- castling
- en passant
- player to move

Things to consider
- 3 fold repetition
- 50 move rule

---

# Links
- [Chess unicode symbols](https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode)
- [Chessboard editor](https://lichess.org/editor)
- [Chess opening tree sizes](https://www.chessprogramming.org/Perft_Results)
- [FEN wiki](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)

# Coming up
- update `castling` field of `Board` when king or rook moves
- compute castling moves (requires computing check)
- forbid moves that put player-to-move in check
- confirm opening tree sizes
- build a bot
- play bot vs bot
- play human vs bot

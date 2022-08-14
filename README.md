# Chess bot

In this repo we create a chess bot. This is a project that is developed on my [twitch stream](https://twitch.tv/thebigmerp).

Initially the aim of this stream is to show people without programming experience how something like this is done.

## Streams

Every last commit after a stream ends gets a tag. That way progress can be seen here while watching the streams back.

#### [stream-01](https://github.com/lk16/chessbot/tree/stream-01)
- Setup repo (off-stream)
- Added `Board` class
- Printing a board in black/white

#### [stream-02](https://github.com/lk16/chessbot/tree/stream-01)
- Add colorized board printing (off-stream)
- Add moves for king, knight, rook, bishop and queen

#### [stream-03](https://github.com/lk16/chessbot/tree/stream-03)
- Add all pawn moves, including promotion, capturing and "en passent"

#### [stream-04](https://github.com/lk16/chessbot/tree/stream-04)
- Add Board/FEN conversion (off-stream)
- Bugfix: capture and promote at the same time
- Detect check
- Castling
- Prevent moves that put yourself in check

#### [stream-05](https://github.com/lk16/chessbot/tree/stream-05)
- Debug opening tree sizes using [Chessnut](https://github.com/cgearhart/Chessnut)
- Implement "en passent" correctly
- Build a bot that plays random moves
- Play bot vs bot
- Fix bug: king can capture other king
- Detect game endings

#### [stream-06](https://github.com/lk16/chessbot/tree/stream-06)
- Implement tree-search using minimax
- Add smarter bots `MaterialBot` and `PawnPusherBot`
- Fix assertion bug in `Game`

### See also
Future features and fixes can be found in the [TODO](./TODO.md) file.

## Links to used resources
- [Chess unicode symbols wiki](https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode)
- [Chessboard editor](https://lichess.org/editor)
- [Chess opening tree sizes](https://www.chessprogramming.org/Perft_Results)
- [Chess FEN notation wiki](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
- [Chess library Chessnut](https://github.com/cgearhart/Chessnut) (removed from repo, was only used for debugging)

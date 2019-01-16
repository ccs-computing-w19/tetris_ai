# tetris_ai
AI to play tetris with user-inputted pieces.

The user is given a 4x4 grid to draw their own enominoes (tetris pieces of n blocks), using up to 4 connected blocks.
This gives the following 9 enomino possibilities (4 more than normal tetris):
[to be added]


The AI will play tetris using the user-inputted pieces or the user can play themself.

GAMEPLAY:
1. user draws their own enominoes on 4x4 grid, which will be the enominoes available in the game
2. user can choose to either place the game or watch the AI play
3. if user chooses to play, they mvoe the enominoes using the arrow keys to clear more rows and prevent overflowing to get a higher score

RULES:
1. enominoes fall from top of screen and land either on the bottom or on top of another enominoes
2. user can move enominoes side to side and rotate clockwise (and counterclockwise) using arrow keys (left, right, up, z)
3. whenever a row is filled with enomino pieces, it "clears" (disappears) and all ground enominoes above the row fall down one row
4. score is calculated by number of rows cleared, combos, etc
5. game is over when enominoes overflow the top row

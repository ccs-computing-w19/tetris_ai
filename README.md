# tetris_ai
AI to play tetris with user-inputted pieces.

## Gameplay
1. user can choose to either place the game or watch the AI play or play against the AI or watch two AIs play against each other
2. if user chooses to play, they move the enominoes using the arrow keys to clear more rows and prevent overflowing to get a higher score
3. combos and multiple row clears give more points

## Rules
1. enominoes fall from top of screen and land either on the bottom or on top of another enominoes
2. user can move enominoes side to side and rotate clockwise (and counterclockwise) using arrow keys (left, right, up, z)
3. whenever a row is filled with enomino pieces, it "clears" (disappears) and all ground enominoes above the row fall down one row
4. score is calculated by number of rows cleared, combos, etc
5. game is over when enominoes overflow the top row

## Use
To run: `$ python3 graphical_game.py --silent`

## Prerequisites
Python \
Pygame

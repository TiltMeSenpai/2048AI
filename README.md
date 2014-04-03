2048AI
======

AI platform for 2048(http://gabrielecirulli.github.io/2048/) using Selenium

WARNING: Code contained may make you want to cry, hate me, vomit, or some combination of those three. I have a feeling
  that I've been programming too much in Java for school, and Python has miraculous abilities to get obcene amounts of
  work done in a single line. Also, I wasn't planning to do anything with this besides entertain my thought, so 
  readability went and hid in a corner of my mind. I appologize and take responsibility for this monstrosity.
  
HOW TO DO INTERESTING THINGS:

The only code really worth editing is in the GameAgents file. Everything else most likely isn't worth reading through.
Essentially, to build your own AI, you inherit the ProtoAgent class, and implement a play() method. play() should decide
what the best move at the given moment is (Probably by looking at the game state). The rest of the file is to take care of
the basic stuff for you.

Important Stuff:

Any refrence to dir is most likely a direction, and is one of the values [game2048.UP, game2048.RIGHT, game2048.DOWN, game2048.LEFT]

getField(): Returns a 2d array containing the values of the tiles (0 is no tile)

look(dir, state = None): "Simulates" a move in the provided direction, and returns a 2d array, similar to getField(),
except with the field after a move (Ignoring the new tile)

move(dir): Simulates a keypress in the 2048 window, actually making a move in the game. Also updates the internal state.

lookUp(i, j, field): Returns a list of the items above the item at field[i][j].

lookLeft(i, j, field): Same as above, except to the left.

lookRight(i, j, field): Guess.

lookDown(i, j, field): I hope you get the picture.

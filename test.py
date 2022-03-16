import Py2048 as game
import numpy as np


board = np.array([[0, 2, 2, 4],
                  [2, 0, 0, 0],
                  [0, 0, 0, 4],
                  [2, 4, 4, 4]])


b = game.Board(board)
e = game.Engine()
c = game.Color()


print(b)
e.move(b, game.LEFT)
print(b)
e.move(b, game.UP)
print(b)
e.move(b, game.RIGHT)
print(b)
e.move(b, game.DOWN)
print(b)

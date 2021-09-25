from game import Game

game = Game(animate=True)

while game.run:
    game.display()
    game.eventHandler()

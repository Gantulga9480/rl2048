from game import Game

game = Game()

while game.run:
    game.eventHandler()
    game.display()

from game import Game

game = Game()

while game.run:
    game.display()
    game.eventHandler()

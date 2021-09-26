from game import Game

game = Game(animate=True)

while game.running:
    game.display()
    game.eventHandler()

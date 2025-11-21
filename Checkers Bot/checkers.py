from checkers.game import Game


game = Game()
game.whose_turn() #1 or 2
game.get_possible_moves() #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
game.move([9, 13])
game.is_over() #True or False
from stockfish import *

# print(help(Stockfish))

stock = Stockfish(parameters={"Threads": 2, "Minimum Thinking Time": 30})
stock.set_position(["e2e4", "e7e6"])
print(stock.get_best_move())


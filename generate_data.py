from projectfiles.game_history_generator import *
from projectfiles.feature_extract import *
import sys

import pickle

if __name__ == "__main__":
	num_games = int(sys.argv[1])
	output_file = sys.argv[2]

	extractor = ResourceExtractor()
	X, y = GameHistoryGenerator.generate(num_games,
		agent1 = TradeAgent(),
		agent2 = TradeAgent(),
		extractor = extractor)

	with open(output_file, "wb") as f:
		pickle.dump((X, y), f)

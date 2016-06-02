from projectfiles.game_history_generator import *
from projectfiles.feature_extract import *
import sys
import pickle

sys.setrecursionlimit(300)

if __name__ == "__main__":
    num_games = int(sys.argv[1])
    if len(sys.argv) == 2:
        output_file = "data.hsdat"
    else:
        output_file = sys.argv[2]

    while num_games > 0:
        extractor = ResourceExtractor()
        X, y = GameHistoryGenerator.generate(min(num_games, 100),
            agent1 = TradeAgent(),
            agent2 = TradeAgent(),
            extractor = extractor)
        num_games -= 100
        print(str(num_games) + " games left.")
        with open(output_file, "ab+") as f:
            pickle.dump((X, y), f)

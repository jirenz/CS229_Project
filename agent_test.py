from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents import *

from projectfiles.random_deck_generator import RandomDeckGenerator
from projectfiles.agent import *
import sys
import shelve

from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger
from projectfiles.agent import *
from projectfiles.feature_extract import *
from projectfiles.strategy_agent import *
from projectfiles.game_history_generator import *
from learning.model import *
from learning.function_approximator import *

import numpy as np
import pickle

#from projectfiles.util import spark_weights

sys.setrecursionlimit(300)

from collections import *

def test_agent_once(one, other = None):
	#print("game_started")
	generator = RandomDeckGenerator()
	deck1 = generator.generate()
	deck2 = deck1.copy()

	if other is None:
		other = TradeAgent()
		#other = RandomAgent()
	game = Game([deck1, deck2], [one, other])
	new_game = game.copy()
	try:
		new_game.start()
		# new_data = GameHistoryGenerator.process_history(history, new_game)
		# Data = open("data.txt", "a")
		# for i in new_data:
			# tmp = i[0]
			# tmp.append(i[1])
			# for j in range(len(tmp)):
				# tmp[j] = str(tmp[j])
			# Data.write(" ".join(tmp))
			# Data.write("\n")
		# Data.close()
		print("Game lasted: " + str(new_game._turns_passed))
		print("winning agent: " + new_game.winner.agent.name)
	except Exception as e:
		print("Game error: " + str(e))
		# raise e
		return False
	
	# spark_weights(ql.weights)
	return new_game.winner.agent.name

def run_agent(one, other, number):
	i = 0
	err = 0
	winning_count = defaultdict(int)
	while i < number:
		winner = test_agent_once(one, other)
		if winner:
			i += 1
			if winner in winning_count:
				winning_count[winner] += 1
			else:
				winning_count[winner] = 1
		else:
			print("Error")
			err += 1
			#if err > 100:
			#	print("Aborting after 5 errors.")
			#	break
	print(dict(winning_count))
	return winning_count

if __name__ == "__main__":
	model_name = sys.argv[1]
	
	if len(sys.argv) >= 3:
		oppo = sys.argv[2]
	else:
		oppo = "trade"
	
	if len(sys.argv) >= 4:
		num_games = int(sys.argv[3])
	else:
		num_games = 20

	if len(sys.argv) >= 5:
		max_depth = int(sys.argv[4])
	else:
		max_depth = 2

	if model_name == "heuristic":
		model = BasicHeuristicModel()
	else:
		with open("models/" + model_name, "rb") as f:
			model = pickle.load(f)
	
	our_agent = StrategyAgent(model, model_name, max_depth)
	if oppo == "trade":
		oppo_agent = TradeAgent()
	elif oppo == "random":
		oppo_agent = RandomAgent()
	else:
		raise Exception("Unknown agent " + oppo)

	#try:
	#	spark_weights(model.weights)
	#except:
	#	pass

	#try:
	#	model.feature_extractor.debug(model.weights)
	#except:
	#	pass
	
	result = run_agent(our_agent, oppo_agent, num_games)

	with open("results", "a") as f:
		f.writelines(["{} {} {} {} => {}\n".format(model_name, oppo, num_games, max_depth, result[model_name])])

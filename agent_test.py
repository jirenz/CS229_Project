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

from learning.model import *

import numpy as np
import pickle

from projectfiles.util import spark_weights

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
	except Exception as e:
		print("Game error: " + str(e))
		raise e
		# raise
		#print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
		# new_game
		return False
	print("Game lasted: " + str(new_game._turns_passed))
	print("winning agent: " + new_game.winner.agent.name)
	# spark_weights(ql.weights)
	return new_game.winner.agent.name

def run_agent(one, other, number):
	i = 0
	err = 0
	winning_count = {}
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
	print(winning_count)


if __name__ == "__main__":
	# OLD STUFF
		# ql = AIAgent(eta = 0.001, explore_prob = 0.1, discount = 0.5, feature_extractor = feature_extractor_2)
		# run_agent(ql, ql, int(sys.argv[1]))

		# ql.explore_prob = 0.0
		# ql.learn = False
		# run_agent(ql, None, int(sys.argv[2]))
		# approximator1 = LinearFunctionApproximator()
		# approximator2 = BasicFunctionApproximator()

		#print("Training")
		#approximator.train(int(sys.argv[1]))

	# Nice
	# train_models.py ql_sp_relative 20 1
	# train_models.py ql_sp_relative 20 2

	# Nice
	# train_models.py ql_fs_resource 20 1
	# train_models.py ql_fs_resource 20 2

	# nah
	# train_models.py ql_sd_resource 20 1
	# train_models.py ql_sd_resource 20 2

	# Nice
	# train_models.py st_fs_resource 20 1
	# train_models.py st_fs_resource 20 2
	
	# Ok
	# train_models.py ql_fs_pear 20 1
	# train_models.py ql_fs_pear 20 2

	# nah
	# train_models.py ql_sd_pear 20 1
	# train_models.py ql_sd_pear 20 2

	# Nice
	# train_models.py st_fs_pear 20 1
	# train_models.py st_fs_pear 20 2

	# StateDifference models converge beautifully while training, but don't work?
	# Why? Are we using them wrong in StrategyAgent or are they just really terrible?

	model_name = sys.argv[1]
	if model_name == "heuristic":
		model = BasicHeuristicModel()
	else:
		with open(model_name, "rb") as f:
			model = pickle.load(f)

	try:
		spark_weights(model.weights)
	except:
		pass

	try:
		model.feature_extractor.debug(model.weights)
	except:
		pass
	
	num_games = int(sys.argv[2])
	max_depth = int(sys.argv[3])
	run_agent(StrategyAgent(model, model_name, max_depth), TradeAgent(), num_games)


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
from projectfiles.feature_extract_2 import *

# from sparklines import sparklines

from projectfiles.strategy_agent import *
from learning.function_approximator import *

def spark_weights(weights):
	W = weights - np.min(weights)
	W = W * 30 / np.max(W)
	#for line in sparklines(list(W), num_lines = 3):
	#	print(line)

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
	#try:
	new_game.start()
	#except Exception as e:
	#	print("Game error: " + str(e))
		#print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
	#	del new_game
	#	return False
	print("winning agent: " + new_game.winner.agent.__class__.__name__)
	# spark_weights(ql.weights)
	return new_game.winner.agent.__class__.__name__

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
	# ql = AIAgent(eta = 0.001, explore_prob = 0.1, discount = 0.5, feature_extractor = feature_extractor_2)
	# run_agent(ql, ql, int(sys.argv[1]))

	# ql.explore_prob = 0.0
	# ql.learn = False
	# run_agent(ql, None, int(sys.argv[2]))
	run_agent(StrategyAgent(), TradeAgent(), int(sys.argv[1]))


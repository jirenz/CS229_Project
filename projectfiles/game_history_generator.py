from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.agents import *
from projectfiles.random_deck_generator import RandomDeckGenerator
from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger
from projectfiles.feature_extract import *

from learning.model import *
import numpy as np

class GameHistoryGenerator:
	def generate(numgames, agent1 = TradeAgent(), agent2 = TradeAgent(), extractor = ResourceExtractor()):
		i = 0
		games = []
		while i < numgames:
			result = GameHistoryGenerator.generate_one(agent1, agent2, extractor)
			if not result is None:
				print("Generating game", i)
				games += result
				i += 1
		X = np.array([state_vector for state_vector, value in games])
		y = np.array([value for state_vector, value in games])
		return X, y

	def generate_one(agent1, agent2, extractor):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()
		game = Game([deck1, deck2], [agent1, agent2])
		try:
			history = game.start_with_history()
		except Exception as e:
			return None
		if not game.game_ended:
			return None
		return GameHistoryGenerator.process_history(history, game, extractor)

	def process_history(history, game, extractor):
		results = []
		for historic_game in history:
			if game.winner is None:
				event = "tie"
			else:
				if historic_game.current_player.name == game.winner.name:
					event = "win"
				else: 
					event = "lose"
			base_reward = HearthstoneMDP.getReward(None, event)
			value = base_reward * (HearthstoneMDP.getDiscount(None) ** (game._turns_passed - historic_game._turns_passed))
			results.append([extractor(historic_game), value])
		return results

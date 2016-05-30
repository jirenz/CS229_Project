import numpy as np
import learning.mdp

from projectfiles.random_deck_generator import RandomDeckGenerator
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.agents import *
import projectfiles.util

from projectfiles.feature_extract import *

class HearthstoneMDP(learning.mdp.MDP):
	def __init__(self, strategy):
		self.strategy = strategy
	
	def start_state(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()

		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		game.pre_game()
		return game

	def is_end_state(self, state):
		return state.game_ended

	def getActions(self, state):
		# An "action" is actually parametrized directly by the state corresponding
		# to the current player's actions. The strategy object enumerates a list of
		# possible actions
		return self.strategy.getActions(state.copy())

	def getRandomAction(self, state):
		return self.strategy.getRandomAction(state.copy())

	def getBestAction(self, state, heuristic):
		return self.strategy.getBestAction(state.copy(), heuristic)

	def getSuccAndReward(self, state, next_action):
		next_state = next_action.copy()

		reward = 0.0
		if next_state.game_ended:
			if next_state.winner is None:
				reward = self.getReward("tie")
			elif state.current_player.name == next_state.winner.name:
				reward = self.getReward("win")
			else:
				reward = self.getReward("lose")

		return (next_state, reward)

	def getReward(self, event):
		return {"win" : 10, "lose" : -10, "tie" : 0.1}[event]
	
	def getDiscount(self):
		return 0.90 #?

class Model:
	def __init__(self):
		pass

	def __call__(self, state, action):
		# the action is a state!
		next_state = action
		return self.eval(state, next_state)

	def eval(self, state, next_state):
		raise NotImplementedError("")

	def update(self, state, next_state, delta):
		raise NotImplementedError("")

class LinearModel(Model):
	def __init__(self, feature_extractor, initial_weights = None):
		self.feature_extractor = feature_extractor
		self.weights = initial_weights if initial_weights is not None else feature_extractor.get_initial()

class StatePairLinearModel(LinearModel):
	# Takes a feature extractor that expects TWO state arguments
	def __init__(self, feature_extractor, initial_weights = None):
		super().__init__(feature_extractor, initial_weights)
		assert(isinstance(self.feature_extractor, StatePairFeatureExtractor))

	def eval(self, state, next_state):
		assert(state.current_player.name == next_state.current_player.name)

		if isinstance(self.feature_extractor, StateFeatureExtractor):
			return np.dot(self.weights, self.feature_extractor(next_state) - self.feature_extractor(state))
		else:
			assert(isinstance(self.feature_extractor, StatePairFeatureExtractor))
			return np.dot(self.weights, self.feature_extractor(state, next_state))

	def update(self, state, next_state, delta):
		assert(state.current_player.name == next_state.current_player.name)
	
		phi = self.feature_extractor(state, next_state)
		print("curplay", state.current_player.name, \
				"health", state.current_player.hero.health, \
				"my_next_health", next_state.current_player.hero.health, \
				"enemy_health", state.current_player.opponent.hero.health, \
				"enemy_next_heatlh", next_state.current_player.opponent.hero.health, \
				"delta", delta)
		# print(phi)

		self.weights += delta * phi
		# self.feature_extractor.debug(self.weights)
	
class FinalStateLinearModel(LinearModel):
	# Takes a feature extractor that expects ONE state argument
	def __init__(self, feature_extractor, initial_weights = None):
		super().__init__(feature_extractor, initial_weights)
		assert(isinstance(self.feature_extractor, StateFeatureExtractor))

	def eval(self, state, next_state):
		return np.dot(self.weights, self.feature_extractor(next_state))

	def update(self, state, next_state, delta):
		phi = self.feature_extractor(next_state)
		self.weights += delta * phi
		# self.weights /= np.sqrt(np.dot(self.weights, self.weights)) + 1e-6

class StateDifferenceLinearModel(LinearModel):
	def __init__(self, feature_extractor, initial_weights = None):
		super().__init__(feature_extractor, initial_weights)
		assert(isinstance(self.feature_extractor, StateFeatureExtractor))

	def eval(self, state, next_state):
		return np.dot(self.weights, self.feature_extractor(next_state) - self.feature_extractor(state))

	def update(self, state, next_state, delta):
		phi = self.feature_extractor(state)
		next_phi = self.feature_extractor(next_state)
		print("curplay", state.current_player.name, \
				"health", state.current_player.hero.health, \
				"my_next_health", next_state.current_player.hero.health, \
				"enemy_health", state.current_player.opponent.hero.health, \
				"enemy_next_heatlh", next_state.current_player.opponent.hero.health, \
				"delta", delta)
		# self.feature_extractor.debug(next_phi - phi)
		self.weights += delta * (next_phi - phi)
		self.feature_extractor.debug(self.weights)

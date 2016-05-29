import numpy as np
import learning.mdp

from projectfiles.random_deck_generator import RandomDeckGenerator
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.agents import *

class HearthstoneMDP(learning.mdp.MDP):
	def __init__(self, strategy):
		self.strategy = strategy
	
	def start_state(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()

		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		game.pre_game()
		game.current_player = game.players[0]
		return game

	def is_end_state(self, state):
		return state.game_ended

	def getActions(self, state):
		# An "action" is actually parametrized directly by the state corresponding
		# to the current player's actions. The strategy object enumerates a list of
		# possible actions
		new_state = state.copy()
		new_state._start_turn()
		actions = self.strategy(new_state)
		for a in actions:
			if new_state.current_player.name != a.current_player.name:
				print("OMG", new_state.current_player, a.current_player)
		return actions

	def getSuccAndReward(self, state, next_action):
		next_state = next_action.copy()
		next_state._end_turn()

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
		return {"win" : 100, "lose" : -100, "tie" : 10}[event]
	
	def getDiscount(self):
		return 0.9 #?

class StatePairLinearModel:
	# Takes a feature extractor that expects TWO state arguments
	def __init__(self, initial_weights, feature_extractor):
		self.weights = initial_weights
		self.feature_extractor = feature_extractor

	def __call__(self, state, action):
		# the action is a state!
		next_state = action.copy()
		next_state._end_turn()
		assert(next_state.current_player == state.current_player)

		return self.eval(state, next_state)

	def eval(self, state, next_state):
		return np.dot(self.weights, self.feature_extractor(state, next_state))

	def update(self, state, next_state, delta):
		phi = self.feature_extractor(state, next_state)
		self.weights += delta * oldPhi
		self.weights /= np.sqrt(np.dot(self.weights, self.weights)) + 1e-6

class SimulatingStatePairLinearModel(StatePairLinearModel):
	# Takes a feature extractor that expects TWO state arguments
	def __init__(self, initial_weights, feature_extractor):
		super().__init__(initial_weights, feature_extractor)

	def __call__(self, state, action):
		# To evaluate the payback of an action with only state-parametrized
		# function approximators, we simulate one random turn (for now) by the enemy player.
		# In the future this could be DP or another player
		next_state = action.copy()
		next_state._end_turn()
		next_state._start_turn() # switch to the other player
		old_agent = next_state.current_player.agent

		# In the future replace this with some other estimation strategy
		# Perhaps we can average several random runs
		next_state.current_player.agent = RandomAgent()
		while not next_state.game_ended:
			if not next_state.current_player.agent.do_turn():
				break

		next_state.current_player.agent = old_agent

		next_state._end_turn()
		next_state._start_turn()
		assert(next_state.current_player == state.current_player)

		return super().eval(state, next_state)

class FinalStateLinearModel:
	# Takes a feature extractor that expects ONE state argument
	def __init__(self, initial_weights, feature_extractor):
		self.weights = initial_weights
		self.feature_extractor = feature_extractor

	def __call__(self, state, action):
		# the action is a state!
		next_state = action.copy()
		if next_state.current_player.name != state.current_player.name:
			print("OMG", next_state.current_player.name, state.current_player.name)
		assert(next_state.current_player.name == state.current_player.name)
		next_state._end_turn()
		assert(next_state.current_player.name == state.current_player.name)

		return self.eval(next_state)

	def eval(self, state, next_state):
		return np.dot(self.weights, self.feature_extractor(next_state))

	def update(self, state, next_state, delta):
		phi = self.feature_extractor(next_state)
		self.weights += delta * oldPhi
		self.weights /= np.sqrt(np.dot(self.weights, self.weights)) + 1e-6

class TreeSearchFinalStateLinearModel(FinalStateLinearModel):
	# Takes a feature extractor that expects ONE state argument
	def __init__(self, initial_weights, feature_extractor):
		self.weights = initial_weights
		self.feature_extractor = feature_extractor

	def __call__(self, state, action):
		# the action is a state!
		next_state = action.copy()

		# DO SOME TREE SEARCH HERE
		next_state._end_turn()
		assert(next_state.current_player == state.current_player)

		return self.eval(state, next_state)

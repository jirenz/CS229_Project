import numpy as np
from sklearn import linear_model
from sknn.mlp import Regressor, Layer
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
		return {"win" : 10, "lose" : -8, "tie" : 31}[event]
	
	def getDiscount(self):
		return 0.8

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
		assert(state.current_player.name == next_state.current_player.name)
		print("curplay", state.current_player.name, \
				"health", state.current_player.hero.health, \
				"my_next_health", next_state.current_player.hero.health, \
				"enemy_health", state.current_player.opponent.hero.health, \
				"enemy_next_heatlh", next_state.current_player.opponent.hero.health, \
				"delta", delta)

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
		super().update(state, next_state, delta)
		phi = self.feature_extractor(state, next_state)
		self.weights += delta * phi
		# self.feature_extractor.debug(self.weights)
	
class FinalStateLinearModel(LinearModel):
	# Takes a feature extractor that expects ONE state argument
	def __init__(self, feature_extractor, initial_weights = None):
		super().__init__(feature_extractor, initial_weights)
		assert(isinstance(self.feature_extractor, StateFeatureExtractor))

	def eval(self, state, next_state):
		if next_state.current_player_win(): return 1e9
		if next_state.current_player_lose(): return -1e9
		return np.dot(self.weights, self.feature_extractor(next_state))

	def train(self, dataset):
		clf = linear_model.LinearRegression()
		X, y = dataset
		# X = [self.feature_extractor(state) for state, value in dataset]
		# y = [value for state, value in dataset]
		clf.fit(X, y)
		self.weights = clf.coef_
		# print(self.weights)

	def update(self, state, next_state, delta):
		super().update(state, next_state, delta)
		phi = self.feature_extractor(next_state)
		self.weights += delta * phi

class StateDifferenceLinearModel(LinearModel):
	def __init__(self, feature_extractor, initial_weights = None):
		super().__init__(feature_extractor, initial_weights)
		assert(isinstance(self.feature_extractor, StateFeatureExtractor))

	def eval(self, state, next_state):
		return np.dot(self.weights, self.feature_extractor(next_state) - self.feature_extractor(state))

	def update(self, state, next_state, delta):
		super().update(state, next_state, delta)
		phi = self.feature_extractor(state)
		next_phi = self.feature_extractor(next_state)
		# self.feature_extractor.debug(next_phi - phi)
		self.weights += delta * (next_phi - phi)
		self.feature_extractor.debug(self.weights)

class BasicHeuristicModel(Model):
	def __init__(self):
		super().__init__()
		
	def eval(self, state_1, state_2):
		def score(player):
			score = 0
			for i in player.minions:
				score += i.calculate_attack()
				score += i.health
			score += len(player.hand) * 2
			score += player.hero.health + player.hero.armor
			return score

		return score(state_2.current_player) - score(state_2.other_player)

class FinalStateNeuralModel(Model):
	def __init__(self, feature_extractor, nn = None):
		self.feature_extractor = feature_extractor
		self.nn = nn if nn is not None else self.get_initial()
		# self.train()

	def get_initial(self):
		return Regressor(
				layers=[
					Layer("Rectifier", units=100),
					# Layer("Sigmoid", units = 200),
					# Layer("Tanh", units = 100)
					Layer("Linear")],
				learning_rate=0.001,
				n_iter=10,
				f_stable = 0.1)

	def eval(self, state, next_state):
		if next_state.current_player_win(): return 1e9
		if next_state.current_player_lose(): return -1e9
		vec = np.array(self.feature_extractor(next_state))
		return self.nn.predict(np.ndarray(shape = (1, len(vec)), buffer = vec))
		# return np.dot(self.weights, self.feature_extractor(next_state))

	def train(self, dataset):
		X, y = dataset
		# X = np.array([self.feature_extractor(state) for state, value in dataset])
		# y = [value for state, value in dataset]
		self.nn.fit(X, y)

	# def train(self):
		# Data = open("data.txt", "r")
		# Tmp = Data.read().splitlines()
		# training_set = []
		# for i in Tmp:
			# c = i.split(" ")
			# for j in range(0, len(c)):
				# c[j] = float(c[j])
			# training_set.append(c)
		# X = []
		# y = []
		# for data_point in training_set:
			# X.append(data_point[0:-1])
			# y.append(data_point[-1])
		# for i in X:
			# if (len(i) != 38):
				# print(i)
		# X = np.ndarray(shape = (len(y), len(X[0])), buffer = np.array(X))
		# y = np.ndarray(shape = (len(y), 1), buffer = np.array(y))
		# self.nn.fit(X, y)
		# print("Learning from data size: " + str(len(y)))
		# Data.close()

class DeepNeuralModel(FinalStateNeuralModel):
	def get_initial(self):
		return Regressor(
				layers=[
					Layer("Rectifier", units=100),
					Layer("Sigmoid", units = 200),
					Layer("Tanh", units = 100),
					Layer("Linear")],
				learning_rate=0.001,
				n_iter=10,
				f_stable = 0.1)

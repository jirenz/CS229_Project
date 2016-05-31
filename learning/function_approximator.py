from hearthbreaker.engine import *
from projectfiles.feature_extract import *
import numpy as np
import random

from projectfiles.game_history_generator import *
from sklearn import linear_model

class BasicFunctionApproximator:
	def __init__(self):
		pass
		
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

class SimpleExtractor:
	def extract(player):
		attack = 0;
		health = 0;
		for i in player.minions:
			attack += i.calculate_attack()
			health += i.health
		feat = [attack, health]
		feat.append(len(player.hand))
		feat.append(player.hero.health + player.hero.armor)
		feat.append(player.game.other_player.hero.health)
		return np.array(feat, dtype=np.float64)

	def initial():
		return np.zeros((5, ))

	
class LinearFunctionApproximator(BasicFunctionApproximator):
	def __init__(self, initial_weights = None):
		self.extractor = ResourceExtractor()
		if initial_weights is None:
			self.weights = self.extractor.get_initial()
		else:
			self.weights = initial_weights

	def __call__(self, state):
		return np.dot(self.extractor(state), self.weights)

	def eval(self, state_1, state_2):
		return np.dot(self.extractor(state_2), self.weights)

	def train(self, numgames):
		training_set = GameHistoryGenerator()(numgames)
		clf = linear_model.LinearRegression()
		X = []
		y = []
		for data_point in training_set:
			X.append(self.extractor(data_point[0]))
			y.append(data_point[1])
		clf.fit(X, y)
		self.weights = clf.coef_
		print(self.weights)

# deprecated
	def update(self, game, score, delta):
		phi = self.extractor(game)
		original_score = np.dot(self.weights, phi)
		self.weights += 0.001 * delta * (score - original_score) * phi
		self.weights /= np.sqrt(np.dot(self.weights, self.weights)) + 1e-6

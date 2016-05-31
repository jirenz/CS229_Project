from hearthbreaker.engine import *
from projectfiles.feature_extract import *
import numpy as np
import random

from projectfiles.game_history_generator import *
from sklearn import linear_model
# from projectfiles.pear_extractor import *

print("function_approximator.py is deprecated")

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
		self.extractor = PearExtractor()
		self.weights = [0.026,0.007,-0.004,0.046,0.005,-0.021,0.052,0.003,
		-0.001,0.036,0.003,0.080,0.021,0.008,0.089,0.082,-0.028,
		-0.100,0.025,-0.009,0.037,0.004,0.018,-0.019,-0.010,0.014,-0.025,-0.005,
		0.014,-0.039,-0.007,0.008,-0.020,-0.007,-0.073,
		-0.032,-0.004,-0.016,-0.038,-0.014,0.059,-0.032,0.011,-0.056,-0.003,-0.022]
		#if initial_weights is None:
		#	self.weights = self.extractor.get_initial()
		#else:
		#	self.weights = initial_weights

	def __call__(self, state):
		return np.dot(self.extractor(state), self.weights)

	def eval(self, state_1, state_2):
		#print(len(self.extractor(state_2)), len(self.weights))
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

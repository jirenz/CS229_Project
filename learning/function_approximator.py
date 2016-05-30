from hearthbreaker.engine import *
from projectfiles.feature_extract import *
import numpy as np
import random

from projectfiles.game_history_generator import *


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
		if initial_weights is None:
			self.weights = feature_extractor_initial()
		else:
			self.weights = initial_weights

	def eval(self, state_1, state_2):
		return np.dot(feature_extractor(state_2.current_player), self.weights)

	def train(self, numgames):
		deltas = [0.3, 0.1, 0.01, 0.05]
		training_set = GameHistoryGenerator()(numgames)
		for delta in deltas:
			traning_set = random.shuffle(training_set)
			for data_point in training_set:
				print(str(self.weights))
				self.update(data_point[0], data_point[1], delta)

	def update(self, game, score, delta):
		phi = feature_extractor(game.current_player)
		original_score = np.dot(self.weights, phi)
		self.weights += 0.001 * delta * (score - original_score) * phi
		self.weights /= np.sqrt(np.dot(self.weights, self.weights)) + 1e-6

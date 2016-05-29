from projectfiles.util import GameHelper, FixedActionAgent
import collections
import numpy as np
import random

class StrategyNode():
	def __init__(self, game, state_set):
		super().__init__()
		self.generate_strategies(game, state_set)

	def generate_strategies(self, game, state_set):
		game_hash = GameHelper.hashgame(game);
		if not (game_hash in state_set):
			self.visited = False
			state_set.add(game_hash)
			self.game = game
			self.substrategies = []
			self.actions = GameHelper.generate_actions(game)
			for action in self.actions:
				outcome = game.copy()
				GameHelper.execute(outcome, action)
				self.substrategies.append([action, StrategyNode(outcome, state_set)])
		else:
			self.visited = True
			self.game = game
			# print("hash collision found!")

	def get_outcomes(self):
		if self.visited: return []
		outcome = [] # action_list game(reference)
		outcome.append(self.game)
		for [action, strategy] in self.substrategies:
			outcome += strategy.get_outcomes()
		return outcome

	def get_optimal(self, path, approximator, original_state, ans_path):
		if self.visited: return
		value = approximator(original_state, self.game)
		if (value > ans_path[0]):
			ans_path[0] = value
			ans_path[1] = path
		for [action, strategy] in self.substrategies:
			path.append(strategy)
			strategy.get_optimal(path, approximator, original_state, ans_path)
			path = path[0:-1]

class StrategyManager():
	def __init__(self, function_approximator):
		self.approximator = function_approximator
		# self.approximator(state, next_state) => value
		pass

	def get_outcomes(self):
		return self.root.get_outcomes()

	def think(self, state):
		self.store_state = set()
		self.root = StrategyNode(state, self.store_state)

	def getActions(self, state):
		self.think(state)
		return self.get_outcomes()

	def getRandomAction(self, state):
		outcome = state.copy()
		while True:
			actions = GameHelper.generate_actions(outcome) + ["NO_ACTION"]
			if len(actions) == 0:
				break

			action = random.choice(actions)
			if action == "NO_ACTION":
				break
			else:
				outcome = GameHelper.execute(outcome, action)
		return outcome

	def getBestActions(self, state, heuristic, max_actions = 1):
		self.think(state)
		self.path = []
		self.ans_path = [-10000, []]
		self.root.get_optimal(self.path, heuristic, self.root.game, self.ans_path)
		print(self.ans_path)
		return [self.ans_path[1][-1].game]

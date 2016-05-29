from projectfiles.util import GameHelper, FixedActionAgent
import collections
import numpy as np
import random
import queue

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

	def get_outcomes(self):
		if self.visited: return []
		outcome = [] # action_list game(reference)
		outcome.append(self.game)
		for [action, strategy] in self.substrategies:
			outcome += strategy.get_outcomes()
		return outcome

	def get_optimal(self, approximator, original_state, ans_pair):
		if self.visited: return
		value = approximator(original_state, self.game)
		if (value > ans_pair[0]):
			ans_pair[0] = value
			ans_pair[1] = self.game
		ans_pair[2] += 1
		if (ans_pair[2] > 100): return
		for [action, strategy] in self.substrategies:
			strategy.get_optimal(approximator, original_state, ans_pair)
			if (ans_pair[2] > 100): return

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

	def getActions(self, state, max_actions = 10):
		self.think(state)
		return self.get_outcomes()

	def getRandomAction(self, state):
		outcome = state.copy()
		while True:
			actions = GameHelper.generate_actions(outcome)
			if len(actions) == 0:
				break
			action = random.choice(actions + ["NO_ACTION"])
			if action == "NO_ACTION":
				break
			else:
				GameHelper.execute(outcome, action)
		return outcome

	def getBestAction(self, state, heuristic):
		self.think(state)
		self.ans_pair = [-10000, None, 0]
		self.root.get_optimal(heuristic, self.root.game, self.ans_pair)
		return self.ans_pair[1]

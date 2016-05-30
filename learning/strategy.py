from projectfiles.util import GameHelper, FixedActionAgent
import collections
import numpy as np
import random
from collections import deque
import heapq

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
	def __init__(self):
		pass

	def getActions(self, state):
		outcomes = []
		visited_states, q = set(), deque()
		visited_states.add(GameHelper.hashgame(state))
		q.append(state)
		while len(q) > 0:
			current_state = q.popleft()
			outcomes.append(current_state)

			actions = GameHelper.generate_actions(current_state)
			for action in actions:
				outcome = current_state.copy()
				GameHelper.execute(outcome, action)
				if GameHelper.hashgame(outcome) not in visited_states:
					visited_states.add(GameHelper.hashgame(outcome))
					q.append(outcome)

		return outcomes

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
		max_search, iteration = 20, 0
		visited_states, pq = set(), []
		best_value, best_outcomes = heuristic(state, state), [state]
		visited_states.add(GameHelper.hashgame(state))
		heapq.heappush(pq, ((best_value, iteration), state))
		while len(pq) > 0 and iteration < max_search:
			current_value, current_state = heapq.heappop(pq)
			# print(current_value, current_state.current_player.hero.__to_json__())

			actions = GameHelper.generate_actions(current_state)
			for action in actions:
				outcome = current_state.copy()
				GameHelper.execute(outcome, action)
				if GameHelper.hashgame(outcome) not in visited_states:
					next_value = heuristic(state, outcome)
					if abs(best_value - next_value) < 1e-6:
						best_outcomes.append(outcome)
					elif best_value < next_value:
						best_value, best_outcomes = next_value, [outcome]
					iteration += 1
					visited_states.add(GameHelper.hashgame(outcome))
					heapq.heappush(pq, ((next_value, iteration), outcome))

		return random.choice(best_outcomes)

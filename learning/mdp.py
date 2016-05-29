import random

class MDP:
	"""Abstract interface for modelling MDPs"""

	def start_state(self):
		"""Return the initial state of the MDP"""
		raise NotImplementedError("")

	def is_end_state(self, state):
		"""Return true if the given state is an end state"""
		raise NotImplementedError("")

	def getActions(self, state):
		"""Propose a set of actions doable at state"""
		raise NotImplementedError("")

	def getRandomAction(self, state):
		"""Propose a random action"""
		return random.choice(self.getActions(state))

	def getBestActions(self, state, heuristic, max_actions = 1):
		scoredActions = map(lambda action: (heuristic(state, action), action), self.getActions(state))
		scoredActions.sort(key=lambda q: q[0])
		return scoredActions[:max_actions]

	def getReward(self, state, next_state):
		"""Calculate the reward from the next_state"""
		raise NotImplementedError("")

	def getDiscount(self):
		return 1.0

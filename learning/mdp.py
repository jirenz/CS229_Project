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

	def getReward(self, state, next_state):
		"""Calculate the reward from the next_state"""
		raise NotImplementedError("")

	def getDiscount(self):
		return 1.0

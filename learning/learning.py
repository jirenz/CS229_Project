import random

class QLearningAlgorithm:
	def __init__(self, mdp, eta, explore_prob, function_approximator):
		self.mdp = mdp
		self.eta = eta
		self.explore_prob = explore_prob
		self.F = function_approximator

	def getQ(self, state, action):
		return self.F(state, action)

	def getV(self, state):
		return max(self.getQ(state, action) for action in self.mdp.getActions(state))

	def getQPolicy(self, state):
		return max((self.getQ(state, action), action) for action in self.mdp.getActions(state))[1]

	def train(self, epochs = 10):
		for epoch in range(epochs):
			state = self.mdp.start_state()

			while not self.mdp.is_end_state(state):
				print("current state", state.current_player.name)
				if random.random() < self.explore_prob:
					next_action = random.choice(self.mdp.getActions(state))
				else:
					next_action = self.getQPolicy(state)

				next_state, reward = self.mdp.getSuccAndReward(state, next_action)
				self.F.update(state, next_action, \
					reward + self.mdp.getDiscount() * self.getV(next_state))

				state = next_state

class ExperienceReplayQ(QLearningAlgorithm):
	def __init__(self, mdp, eta, explore_prob, rewards, function_approximator,
					experience_size = 1000,
					replay_size = 100,
					replays_per_epoch = 1):
		super().__init__(mdp, eta, explore_prob, rewards, function_approximator)
		self.experience_size = experience_size
		self.replay_size = replay_size
		self.replays_per_epoch = replays_per_epoch

		# list of (state, next_state, reward) tuples
		self.experience = []
	
	def train(self, epochs = 10):
		for epoch in range(epochs):
			state = self.mdp.start_state()
			history = []

			while not self.mdp.is_end_state(state):
				if random.random() < self.explore_prob:
					next_action = random.choice(self.mdp.getActions(state))
				else:
					next_action = self.getQPolicy(state)

				history.append((state, next_action))

				next_state, _ = self.mdp.getSuccAndReward(state, next_action)
				state = next_state

			# ... s1 a1 (p0), s2 a2 (p1), END : last action by p1, p1 either won or lost
			# the last state tells you the winner. suppose p0 won, then we should get
			# (s1, a1, win_reward), (s2, a2, lose_reward)

			# train once in reverse:
			# last states get a special case reward:
			s1, a1 = history[-2]
			s2, a2 = history[-1]
			if state.winner is None:
				self.experience.append((s1, a1, self.mdp.getReward("tie")))
				self.experience.append((s2, a2, self.mdp.getReward("tie")))
			else:
				if state.winner == s1.current_player:
					self.experience.append((s1, a1, self.mdp.getReward("win")))
					self.experience.append((s2, a2, self.mdp.getReward("lose")))
				else:
					self.experience.append((s1, a1, self.mdp.getReward("lose")))
					self.experience.append((s2, a2, self.mdp.getReward("win")))

			# for all other states, give a zero reward
			for s, a in history[-3::-1]:
				self.experience.append((s, a, 0))

			# truncate experience
			if len(self.experience) > self.experience_size:
				self.experience = random.sample(self.experience, self.experience_size)

			for replay in range(self.replays_per_epoch):
				replays = random.sample(self.experience, self.replay_size)
				for r_state, next_action, reward in replays:
					next_state, _ = self.mdp.getSuccAndReward(r_state, next_action)
					self.F.update(r_state, next_action, \
						reward + self.mdp.getDiscount() * self.getV(next_state))

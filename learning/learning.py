import random
import json

import numpy as np
from sparklines import sparklines

class QLearningAlgorithm:
	def __init__(self, mdp, eta, explore_prob, function_approximator):
		self.mdp = mdp
		self.eta = eta
		self.explore_prob = explore_prob
		self.F = function_approximator

	def getQ(self, state, action):
		next_state = action.copy()
		next_state._end_turn()
		return self.F(state, next_state)

	def getV(self, state):
		return self.getQ(state, self.mdp.getBestAction(state, self.getQ))
		# return max(self.getQ(state, action) for action in self.mdp.getActions(state))

	def spark_weights(weights):
		W = weights - np.min(weights)
		W = W * 30 / (np.max(W) + 1e-6)
		for line in sparklines(list(W), num_lines = 3):
			print(line)

	def epsilon_greedy(self, state):
		if random.random() < self.explore_prob:
			print("epsilon_greedy: get random action")
			# next_action = random.choice(self.mdp.getActions(state))
			return self.mdp.getRandomAction(state)
		else:
			print("epsilon_greedy: get best action")
			return self.mdp.getBestAction(state, self.getQ)
	
	def simulate_game(self, callback):
		state = self.mdp.start_state()

		turns = 0
		while not self.mdp.is_end_state(state):
			state._start_turn()
			print("simulate_game: turn", turns, "current player", state.current_player.name)
			# print(state.current_player.hero.__to_json__())

			action = self.epsilon_greedy(state)
			next_state, reward = self.mdp.getSuccAndReward(state, action)
			assert(action.current_player.name == state.current_player.name)
			callback(state, action, reward, next_state)
			next_state._end_turn()

			state = next_state
			turns += 1

		return state

	def train(self, epochs = 10):
		def qlearning_update(state, action, reward, next_state):
			self.F.update(state, action, \
				self.eta * (reward + self.mdp.getDiscount() * self.getV(next_state) - self.getQ(state, action)))
			QLearningAlgorithm.spark_weights(self.F.weights)

		for epoch in range(epochs):
			self.simulate_game(qlearning_update)


class ExperienceReplayQ(QLearningAlgorithm):
	def __init__(self, mdp, eta, explore_prob, function_approximator,
			experience_size = 500,
			replays_per_epoch = 50):
		super().__init__(mdp, eta, explore_prob, function_approximator)
		self.experience_size = experience_size
		self.replays_per_epoch = replays_per_epoch

		# list of (state, next_state, reward) tuples
		self.experience = []

	def train(self, epochs = 10):
		for epoch in range(epochs):
			history = []

			def save_history(state, action, reward, next_state):
				assert(state.current_player.name == action.current_player.name)
				history.append((state.copy(), action.copy()))

			state = self.simulate_game(save_history)

			# ... s1 a1 (p0), s2 a2 (p1), END : last action by p1, p1 either won or lost
			# the last state tells you the winner. suppose p0 won, then we should get
			# (s1, a1, win_reward), (s2, a2, lose_reward)

			# train once in reverse:
			# last states get a special case reward:
			s1, a1 = history[-2]
			s2, a2 = history[-1]
			game_experience = []
			print("RESULT", s1.current_player.name, s2.current_player.name, state.winner.name if state.winner is not None else "tie")

			if state.winner is None:
				game_experience.append((s1, a1, self.mdp.getReward("tie")))
				game_experience.append((s2, a2, self.mdp.getReward("tie")))
			else:
				if state.winner.name == s1.current_player.name:
					game_experience.append((s1, a1, self.mdp.getReward("win")))
					game_experience.append((s2, a2, self.mdp.getReward("lose")))
				else:
					game_experience.append((s1, a1, self.mdp.getReward("lose")))
					game_experience.append((s2, a2, self.mdp.getReward("win")))

			# for all other states, give a zero reward
			for s, a in history[-3::-1]:
				game_experience.append((s, a, 0))

			# train on the current game
			for r_state, action, reward in game_experience:
				print("Replay", reward)
				next_state, _ = self.mdp.getSuccAndReward(r_state, action)
				assert(r_state.current_player.name == next_state.current_player.name)
				# print(r_state.current_player.name, action.current_player.name, next_state.current_player.name)
				self.F.update(r_state, action, \
						self.eta * (reward + self.mdp.getDiscount() * self.getV(next_state) - self.getQ(r_state, action)))
				QLearningAlgorithm.spark_weights(self.F.weights)

			# truncate experience
			self.experience += game_experience
			if len(self.experience) > self.experience_size:
				self.experience = random.sample(self.experience, self.experience_size)

			for episode in range(self.replays_per_epoch):
				print("Epoch", epoch, "episode", episode, reward)
				r_state, action, reward = random.choice(self.experience)
				next_state, _ = self.mdp.getSuccAndReward(r_state, action)
				self.F.update(r_state, action, \
						self.eta * (reward + self.mdp.getDiscount() * self.getV(next_state) - self.getQ(r_state, action)))
				QLearningAlgorithm.spark_weights(self.F.weights)


class ActionTreeNode():
	def __init__(self, game_state, state_set, parent = None, action = GameHelper.no_action, function_approximator = None):
		self.game = game_state
		self.parent = parent
		self.action = action
		if parent is None:
			self.depth = 0
		else:
			self.depth = parent.depth + 1
		self.state_set = state_set

	def generate_children(self):
		actions = GameHelper.generate_actions(self.game)

		for action in actions:
			new_game = game.copy()
			GameHelper.execute(new_game, action)
			new_game_hash = GameHelper.hashgame(game);
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

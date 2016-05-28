class GameHelper():
	def __init__(self):
		self.base = 314159
		self.bigp = 1000000007
		pass

	def generate_actions(self, game):
		player = game.current_player
		if game.game_ended: return []

		actions = []
		enemy_targets = self.get_enemy_targets(player)
		for i, attack_minion in filter(lambda p: p[1].can_attack(), enumerate(player.minions)):
			actions += [(0, i, target) for target in range(len(enemy_targets))]
		if player.hero.can_attack():
			actions += [(1, None, target) for target in range(len(enemy_targets))]
		for i, card in filter(lambda p: p[1].can_use(player, player.game), enumerate(player.hand)):
			try:
				actions += [(2, i, target) for target in range(len(card.targets))]
			except:
				actions += [(2, i, None)]
		if player.hero.power.can_use():
			actions += [(3, None, None)]
		#if len(actions) > 5:
		#	print("action_size: " + str(len(actions)))
		return actions

	def get_enemy_targets(self, player):
		found_taunt = False
		targets = []
		for enemy in player.game.other_player.minions:
			if enemy.taunt and enemy.can_be_attacked():
				found_taunt = True
			if enemy.can_be_attacked():
				targets.append(enemy)

		if found_taunt:
			targets = [target for target in targets if target.taunt]
		else:
			targets.append(player.game.other_player.hero)
		return targets

	def excecute(self, game, action):
		machine = DoFixedThingsMachine(*action)
		game.current_player.agent = machine
		machine.do_turn(game.current_player)
		return game

	def hashgame(self,game):
		player = game.current_player
		state_list = feature_extractor(player)
		ans = 1
		for i in state_list:
			ans = (ans * self.base + i ) % self.bigp;
		return ans

	def game_to_json(self, game):
		return json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1)

class StrategyNode(GameHelper):
	def __init__(self, game, state_set):
		self.generate_strategies(game, state_set)

	def generate_strategies(self, game, state_set):
		game_hash = self.hashgame(game);
		if not (game_hash in state_set):
			state_set.add(game_hash)
			self.game = game
			self.substrategies = []
			self.actions = self.generate_actions(game)
			for action in self.actions:
				outcome = game.copy()
				self.excecute(outcome, action)
				self.substrategies.append([action, StrategyNode(outcome, state_set)])
		else:
			self.game = None
			# print("hash collision found!")

	def get_outcomes(self):
		if (self.game == None): return []
		outcome = [] # action_list game(reference)
		outcome.append(self.game)
		for [action, strategy] in self.substrategies:
			outcome += strategy.get_outcomes()
		return outcome

class StrategyManager():
	def __init__(self, function_approximator):
		self.F = function_approximator
		# self.F(state, next_state) => value
		pass

	def __call__(self, state):
		store_state = set()
		strategy_node = StrategyNode(state, store_state);
		return strategy_node.get_outcomes()

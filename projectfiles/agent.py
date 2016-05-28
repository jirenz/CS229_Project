from hearthbreaker.agents.basic_agents import *
import collections
import numpy as np

class DoFixedThingsMachine(Agent):
	def __init__(self, chosen_index, entity_index, target_index, minion_position_index = 0):
		self.chosen_index = chosen_index
		self.entity_index = entity_index
		self.target_index = target_index
		self.minion_position_index = minion_position_index

	def do_card_check(self, cards):
		return [True, True, True, True]

	def do_turn(self, player):
		if self.chosen_index == 0:
			player.minions[self.entity_index].attack()
		elif self.chosen_index == 1:
			player.hero.attack()
		elif self.chosen_index == 2:
			player.game.play_card(player.hand[self.entity_index])
		elif self.chosen_index == 3:
			player.hero.power.use()

	def choose_target(self, targets):
		if self.target_index is not None:
			return targets[self.target_index]
		else:
			return targets[random.randint(0, len(targets) - 1)]

	def choose_index(self, card, player):
		return self.minion_position_index

	def choose_option(self, options, player):
		return options[random.randint(0, len(options) - 1)]

class Strategies():
	def __init__(self):

	def 
	
class AIAgent(DoNothingAgent):
	def __init__(self, eta, explore_prob, discount, feature_extractor, learn = True):
		super().__init__()

		def wrap_feature_extractor(feature_extractor):
			def wrapped_feature_extractor(game, action):

				next_game = game.copy()
				next_game.current_player.agent = DoFixedThingsMachine(*action)
				next_game.current_player.agent.do_turn(next_game.current_player)
				return feature_extractor(game, next_game, action)
				# return feature_extractor(next_game.current_player)
			
			return wrapped_feature_extractor

		self.eta = eta
		self.explore_prob = explore_prob
		self.discount = discount
		self.feature_extractor = wrap_feature_extractor(feature_extractor)
		self.weights = None
		self.learn = learn

	def do_card_check(self, cards):
		return [True, True, True, True]

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
			targets.append(self.player.game.other_player.hero)
		return targets

	def get_actions(self, player):
		if player.game.game_ended: return []

		actions = []
		enemy_targets = self.get_enemy_targets(player)
		for i, attack_minion in filter(lambda p: p[1].can_attack(), enumerate(player.minions)):
			actions += [(0, i, target) for target in range(len(enemy_targets))]
		if player.hero.can_attack():
			actions += [(1, None, target) for target in range(len(minion_targets))]
		for i, card in filter(lambda p: p[1].can_use(player, player.game), enumerate(player.hand)):
			try:
				actions += [(2, i, target) for target in range(len(card.targets))]
			except:
				actions += [(2, i, None)]
		if player.hero.power.can_use():
			actions += [(3, None, None)]
		print("action_size: " + str(len(actions)))
		return actions

	def decide(self, actions):
		if random.random() < self.explore_prob:
			return random.choice(actions)
		else:
			return max((self.Q(self.player.game, action), action) for action in actions)[1]

	def Q(self, game, action):
		if self.weights is None:
			self.weights = np.zeros(np.size(self.feature_extractor(game, action)))
		return np.dot(self.weights, self.feature_extractor(game, action))

	def do_turn(self, player):
		self.player = player

		actions = self.get_actions(self.player)
		if len(actions) == 0:
			return False

		best_decision = self.decide(actions)

		oldQ = self.Q(self.player.game, best_decision)
		oldPhi = self.feature_extractor(self.player.game, best_decision)
		self.machine = DoFixedThingsMachine(*best_decision)
		self.machine.do_turn(self.player)

		reward = 0.0
		if self.player.game.game_ended:
			#print("check", self.player.game.winner,self.player,self.player.opponent)
			if self.player.game.winner is self.player:
				reward = 100.0
			elif self.player.game.winner is None:
				reward = 0.0
			else:
				reward = -100.0

		actions = self.get_actions(self.player)
		newV = max(self.Q(self.player.game, action) for action in actions) if len(actions) > 0 else 0

		if self.learn:
			self.weights += self.eta * (reward + self.discount * newV - oldQ) * oldPhi
			self.weights /= np.sqrt(np.dot(self.weights, self.weights)) + 1e-6

		return True

	def choose_target(self, targets):
		return self.machine.choose_target(targets)

	def choose_index(self, card, player):
		return self.machine.choose_index(card, player)

	def choose_option(self, options, player):
		options = self.filter_options(options, player)
		return self.machine.choose_option(options, player)

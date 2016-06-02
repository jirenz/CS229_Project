from projectfiles.random_deck_generator import RandomDeckGenerator
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.agents import *

import numpy as np

class StatePairFeatureExtractor:
	def __call__(self, state, next_state):
		raise NotImplementedError("")

	def get_initial(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()
		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		return np.zeros(self.__call__(game, game).shape)

	def debug(self, extracted):
		raise NotImplementedError("")

class StateFeatureExtractor:
	def __call__(self, state):
		raise NotImplementedError("")

	def get_initial(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()
		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		return np.zeros(self.__call__(game).shape)

	def debug(self, extracted):
		raise NotImplementedError("")

def resource(player):
	resources = {}
	minion_stats = [(minion.calculate_attack(), minion.health) for minion in player.minions]
	minion_stats.sort()
	for i, minion in enumerate(minion_stats + [None] * (8 - len(player.minions))):
		if minion is not None:
			attack, health = minion
		else:
			attack, health = 0, 0
		resources['minion-%d-attack' % i] = attack
		resources['minion-%d-health' % i] = health
	resources['minion-total-attack'] = sum(attack for attack, health in minion_stats)
	resources['minion-total-health'] = sum(health for attack, health in minion_stats)
	resources['minion-count'] = len(player.minions)
	resources['hero-health'] = player.hero.health
	resources['hero-armor'] = player.hero.armor
	resources['combined-health'] = resources['hero-health'] + resources['minion-total-health']
	resources['mana'] = player.mana
	resources['max-mana'] = player.max_mana
	# resources['current-overload'] = player.current_overload
	# resources['upcoming-overload'] = player.upcoming_overload
	resources['deck-cards'] = len(player.deck.cards)
	resources['hand-cards'] = len(player.hand)
	# resources['fatigue'] = player.fatigue
	resources['spell-damage'] = player.spell_damage
	resources['spell-multiplier'] = player.spell_multiplier
	resources['heal-multiplier'] = player.heal_multiplier
	resources['heal-does-damage'] = player.heal_does_damage
	# resources['cards-played'] = player.cards_played
	return resources

def diff(a, b):
	feats = {}
	for k in a.keys():
		feats[k] = a[k] - b[k]
	return feats

def prefix_update(a, b, prefix):
	for k in b.keys():
		a[prefix + k] = b[k]

class RelativeResourceExtractor(StatePairFeatureExtractor):
	def __init__(self):
		self.keys = None

	def __call__(self, game, next_game):
		player = game.current_player
		oppo = player.opponent
		player_next = next_game.current_player
		oppo_next = player_next.opponent
		if player.name != player_next.name:
			player_next, oppo_next = oppo_next, player_next
		# print("EXTRACT", player.name, player_next.name, oppo.name, oppo_next.name)
		assert(player.name == player_next.name)

		feat = {}

		player_r, player_next_r = resource(player), resource(player_next)
		oppo_r, oppo_next_r = resource(oppo), resource(oppo_next)
		player_gain = diff(player_next_r, player_r)
		oppo_gain = diff(oppo_next_r, oppo_r)
		# relative_gain = diff(diff(player_next_r, player_r), diff(oppo_next_r, oppo_r))

		prefix_update(feat, player_r, 'player-')
		prefix_update(feat, player_next_r, 'player-next-')
		prefix_update(feat, oppo_r, 'oppo-')
		prefix_update(feat, oppo_next_r, 'oppo-next-')
		prefix_update(feat, player_gain, 'player-gain-')
		prefix_update(feat, oppo_gain, 'oppo-gain-')
		# prefix_update(feat, relative_gain, 'relative-gain-')

		if self.keys is None:
			self.keys = list(feat.keys())
			self.keys.sort()

		return np.array([feat[key] for key in self.keys], dtype=np.float64)

	def debug(self, weights):
		if self.keys is None:
			self.get_initial()

		vals = [(val, i) for i, val in enumerate(list(weights))]
		vals.sort(key=lambda x: abs(x[0]), reverse=True)

		for val, i in vals[:10]:
			print(self.keys[i], ":", val)

class ResourceExtractor(StateFeatureExtractor):
	def __init__(self):
		self.keys = None

	def __call__(self, game):
		player = game.current_player
		oppo = player.opponent

		feat = {}

		player_r = resource(player)
		oppo_r = resource(oppo)

		prefix_update(feat, player_r, 'player-')
		prefix_update(feat, oppo_r, 'oppo-')

		if self.keys is None:
			self.keys = list(feat.keys())
			self.keys.sort()

		return np.array([feat[key] for key in self.keys], dtype=np.float64)

	def debug(self, weights):
		if self.keys is None:
			self.get_initial()

		vals = [(val, i) for i, val in enumerate(list(weights))]
		vals.sort(key=lambda x: abs(x[0]), reverse=True)

		for val, i in vals[:10]:
			print(self.keys[i], ":", val)

class SimpleExtractor(StateFeatureExtractor):
	def __init__(self):
		pass

	def __call__(self, game):
		player = game.current_player
		attack = 0;
		health = 0;
		for i in player.minions:
			attack += i.calculate_attack()
			health += i.health
		feat = [attack, health]
		feat.append(len(player.hand))
		feat.append(player.hero.health + player.hero.armor)
		feat.append(player.game.other_player.hero.health)
		return np.array(feat, dtype=np.float64)

	def get_initial():
		return np.zeros((5, ))
	
	def debug(self, weights):
		print(weights)

class PearExtractor():		
	def __call__(self, game):
		player = game.current_player
		oppo = player.opponent
		feat = []
		
		# add my own information
		count = 0
		tmp = []
		for i in player.minions:
			tmp.append([i.calculate_attack(), i.health])
			count += 1
		tmp.sort()
		for i in tmp: feat += i
		for i in range(0, 8 - count): feat += [0, 0]
		feat += [(player.hero.health + player.hero.armor) / 5]
		feat += [len(player.deck.cards) / 5, len(player.hand) / 2]
		
		# add opponent's information
		count = 0
		tmp = []
		for i in oppo.minions:
			tmp.append([i.calculate_attack(), i.health])
			count += 1
		tmp.sort()
		for i in tmp: feat += i
		for i in range(0, 8 - count): feat += [0, 0]
		feat += [(oppo.hero.health + oppo.hero.armor) / 5]
		feat += [len(oppo.deck.cards) / 5, len(oppo.hand) / 2]

		return feat

	#def debug(self, weights):
	#	print(weights)

	# this is now saved in linear_pear_extractor_model, no need for the hack
	# def get_initial(self):
		# return np.array([0.026,0.007,-0.004,0.046,0.005,-0.021,0.052,0.003,\
		# -0.001,0.036,0.003,0.080,0.021,0.008,0.089,0.082,-0.028,\
		# -0.100,0.025,-0.009,0.037,0.004,0.018,-0.019,-0.010,0.014,-0.025,-0.005,\
		# 0.014,-0.039,-0.007,0.008,-0.020,-0.007,-0.073,\
		# -0.032,-0.004,-0.016,-0.038,-0.014,0.059,-0.032,0.011,-0.056,-0.003,-0.022])

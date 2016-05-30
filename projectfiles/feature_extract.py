from projectfiles.random_deck_generator import RandomDeckGenerator
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.agents import *

import numpy as np

class StatePairFeatureExtractor:
	def __call__(self, state, next_state):
		raise NotImplementedError("")

	def get_initial(self):
		raise NotImplementedError("")

	def debug(self, extracted):
		raise NotImplementedError("")

class StateFeatureExtractor:
	def __call__(self, state):
		raise NotImplementedError("")

	def get_initial(self):
		raise NotImplementedError("")

	def debug(self, extracted):
		raise NotImplementedError("")

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

		def resource(player):
			resources = {}
			minion_stats = [(minion.calculate_attack(), minion.health) for minion in player.minions]
			minion_stats.sort()
			for i, minion in enumerate(minion_stats + [None] * (8 - len(player.minions))):
				if minion is not None:
					attack, health = minion
					# resources['minion-%d-attack' % i] = attack
					# resources['minion-%d-health' % i] = health
				else:
					pass
					# resources['minion-%d-attack' % i] = 0
					# resources['minion-%d-health' % i] = 0
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
			resources['cards-played'] = player.cards_played
			return resources
		
		def diff(a, b):
			feats = {}
			for k in a.keys():
				feats[k] = a[k] - b[k]
			return feats

		def prefix_update(a, b, prefix):
			for k in b.keys():
				a[prefix + k] = b[k]

		player_r, player_next_r = resource(player), resource(player_next)
		oppo_r, oppo_next_r = resource(oppo), resource(oppo_next)
		player_gain = diff(player_next_r, player_r)
		oppo_gain = diff(oppo_next_r, oppo_r)
		relative_gain = diff(diff(player_next_r, player_r), diff(oppo_next_r, oppo_r))

		prefix_update(feat, player_r, 'player-')
		prefix_update(feat, player_next_r, 'player-next-')
		prefix_update(feat, oppo_r, 'oppo-')
		prefix_update(feat, oppo_next_r, 'oppo-next-')
		prefix_update(feat, player_gain, 'player-gain-')
		prefix_update(feat, oppo_gain, 'oppo-gain-')
		prefix_update(feat, relative_gain, 'relative-gain-')

		# del next_game
		# print(len(feat))
		if self.keys is None:
			self.keys = list(feat.keys())
			self.keys.sort()

		return np.array([feat[key] for key in self.keys], dtype=np.float64)

	def get_initial(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()
		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		return np.zeros(self.__call__(game, game).shape)

	def debug(self, weights):
		for i, key in enumerate(self.keys):
			print(key, ":", weights[i])

class ResourceExtractor(StateFeatureExtractor):
	def __init__(self):
		self.keys = []
		for i in range(7):
			self.keys += ["pm%d-atk" % i, "pm%d-health" % i, "pm%d-?" % i]
		self.keys += ["p-health", "p-armor"]
		for i in range(7):
			self.keys += ["em%d-atk" % i, "em%d-health" % i, "em%d-?" % i]
		self.keys += ["e-health", "e-armor"]
		self.keys += ["p-mana", "e-mana"]
		self.keys += ["p-current-overload", "e-current-overload"]
		self.keys += ["p-upcoming-overload", "e-upcoming-overload"]
		self.keys += ["p-max-mana", "e-max-mana"]
		self.keys += ["p-deck", "e-deck"]
		self.keys += ["p-fatigue", "e-fatigue"]
		self.keys += ["p-spell-damage", "e-spell-damage"]
		self.keys += ["p-spell-multiplier", "e-spell-multiplier"]
		self.keys += ["p-heal-multiplier", "e-heal-multiplier"]
		self.keys += ["p-heal-damage", "e-heal-damage"]
		self.keys += ["p-cards-played", "e-cards-played"]

	def __call__(self, game):
		player = game.current_player
		oppo = player.opponent
		feat = []
		
		# add my own information
		count = 0
		tmp = []
		for i in player.minions:
			tmp.append([i.calculate_attack(), i.health, 1])
			count += 1
		tmp.sort()
		for i in tmp: feat += i
		for i in range(0, 7 - count): feat += [0, 0, 0]
		feat += [player.hero.health, player.hero.armor]
		
		# add opponent's information
		count = 0
		tmp = []
		for i in oppo.minions:
			tmp.append([i.calculate_attack(), i.health, 1])
			count += 1
		tmp.sort()
		for i in tmp: feat += i
		for i in range(0, 7 - count): feat += [0, 0, 0]
		# feat += [oppo.hero.health, oppo.hero.armor]

		# add other information
		feat += [player.mana, oppo.mana]
		feat += [player.current_overload, oppo.current_overload]
		feat += [player.upcoming_overload, oppo.upcoming_overload]
		feat += [player.max_mana, oppo.max_mana]
		feat += [len(player.deck.cards), len(oppo.deck.cards)]
		feat += [player.fatigue, oppo.fatigue]
		feat += [player.spell_damage, oppo.spell_damage]
		feat += [player.spell_multiplier, oppo.spell_multiplier]
		feat += [player.heal_multiplier, oppo.heal_multiplier]
		feat += [player.heal_does_damage, oppo.heal_does_damage]
		feat += [player.cards_played, oppo.cards_played]

		# print(len(feat))
		return np.array(feat, dtype=np.float64)

	def get_initial(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()
		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		return np.zeros(self.__call__(game).shape)

	def debug(self, weights):
		vals = [(val, i) for i, val in enumerate(list(weights))]
		vals.sort(key=lambda x: abs(x[0]), reverse=True)

		for val, i in vals[:20]:
			print(self.keys[i], ":", val)


class TestResourceExtractor(StateFeatureExtractor):
	def __init__(self):
		self.keys = None

	def __call__(self, game):
		player = game.current_player
		oppo = player.opponent

		feat = {}

		def resource(player):
			resources = {}
			minion_stats = [(minion.calculate_attack(), minion.health) for minion in player.minions]
			minion_stats.sort()
			for i, minion in enumerate(minion_stats + [None] * (8 - len(player.minions))):
				if minion is not None:
					attack, health = minion
				else:
					attack, health = 0, 0
				# resources['minion-%d-attack' % i] = attack
				# resources['minion-%d-health' % i] = health
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

		player_r = resource(player)
		oppo_r = resource(oppo)

		prefix_update(feat, player_r, 'player-')
		prefix_update(feat, oppo_r, 'oppo-')

		# print(len(feat))

		if self.keys is None:
			self.keys = list(feat.keys())
			self.keys.sort()

		return np.array([feat[key] for key in self.keys], dtype=np.float64)

	def get_initial(self):
		generator = RandomDeckGenerator()
		deck1 = generator.generate()
		deck2 = deck1.copy()
		game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
		return np.zeros(self.__call__(game).shape)

	def debug(self, weights):
		if self.keys is None:
			self.get_initial()

		vals = [(val, i) for i, val in enumerate(list(weights))]
		vals.sort(key=lambda x: abs(x[0]), reverse=True)

		for val, i in vals[:20]:
			print(self.keys[i], ":", val)

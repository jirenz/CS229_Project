import numpy as np

def feature_extractor_2(game, next_game, action):
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
		for i, minion in enumerate(minion_stats + [None] * (7 - len(player.minions))):
			if minion is not None:
				attack, health = minion
				resources['minion-%d-attack'] = attack
				resources['minion-%d-health'] = health
			else:
				resources['minion-%d-attack'] = 0
				resources['minion-%d-health'] = 0
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
		# resources['spell-damage'] = player.spell_damage
		# resources['spell-multiplier'] = player.spell_multiplier
		# resources['heal-multiplier'] = player.heal_multiplier
		# resources['heal-does-damage'] = player.heal_does_damage
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
	player_gain = diff(player_r, player_next_r)
	oppo_gain = diff(oppo_r, oppo_next_r)
	relative_gain = diff(diff(player_r, player_next_r), diff(oppo_r, oppo_next_r))

	prefix_update(feat, player_r, 'player-')
	prefix_update(feat, player_next_r, 'player-next-')
	prefix_update(feat, oppo_r, 'oppo-')
	prefix_update(feat, oppo_next_r, 'oppo-next-')
	prefix_update(feat, player_gain, 'player-gain-')
	prefix_update(feat, oppo_gain, 'oppo-gain-')
	prefix_update(feat, relative_gain, 'relative-gain-')

	del next_game
	# print(feat)
	return np.array(list(feat.values()), dtype=np.float64)

def feature_extractor_2_temporary(state, next_state):
	return feature_extractor_2(state, next_state, None)

def feature_extractor_2_initial():
	return np.zeros((91, ))

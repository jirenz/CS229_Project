import numpy as np

def feature_extractor(player):
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

def feature_extractor_initial():
	return np.zeros((66, ))

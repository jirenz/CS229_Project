def feature_extractor(player):
	oppo = player.opponent
	feat = []
	
	# add my own information
	count = 0
	tmp = []
	for i in player.minions:
		tmp.append([i.attack, i.health, 1])
		count += 1
	tmp.sort()
	for i in tmp: feat += i
	for i in range(0, 7 - count): feat += [0, 0, 0]
	feat += [player.health, player.armor]
	
	# add opponent's information
	count = 0
	tmp = []
	for i in oppo.minions:
		tmp.append([i.attack, i.health, 1])
		count += 1
	tmp.sort()
	for i in tmp: feat += i
	for i in range(0, 7 - count): feat += [0, 0, 0]
	feat += [oppo.health, oppo.armor]

	# add other information
	feat += [player.mana, oppo.mana]
	feat += [player.current_overload, oppo.current_overload]
	feat += [player.upcoming_overload, oppo.upcoming_overload]
	feat += [player.max_mana, oppo.max_mana]
	feat += [len(player.deck), len(oppo.deck)]
	feat += [player.fatigue, oppo.fatigue]
	feat += [player.spell_damage, oppo.spell_damage]
	feat += [player.spell_multiplier, oppo.spell_multiplier]
	feat += [player.heal_multiplier, oppo.heal_multiplier]
	feat += [player.heal_does_damage, oppo.heal_does_damage]
	feat += [player.cards_played, oppo.cards_played]
	
	return feat

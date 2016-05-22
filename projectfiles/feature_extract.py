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
	
	return feat

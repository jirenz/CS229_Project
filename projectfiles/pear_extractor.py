class PearExtractor():
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
		feat += [oppo.hero.health, oppo.hero.armor]

		return feat


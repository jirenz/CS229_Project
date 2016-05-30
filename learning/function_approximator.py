from hearthbreaker.engine import *

class BasicFunctionApproximator:
	def eval(state_1, state_2):
		def score(player):
			score = 0
			for i in player.minions:
				score += i.calculate_attack()
				score += i.health
			score += len(player.hand) * 2
			score += player.hero.health + player.hero.armor
			return score

		return score(state_2.current_player) - score(state_2.other_player)

	

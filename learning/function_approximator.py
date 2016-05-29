from hearthbreaker.engine import *

class BasicFunctionApproximator:
	def __call__(self, state_1, state_2):
		return self.score(state_2.current_player) - self.score(state_2.other_player)

	def score(self, player):
		score = 0
		for i in player.minions:
			score += i.calculate_attack()
			score += i.health
		score += len(player.hand) * 2
		score += player.hero.health + player.hero.armor
		return score
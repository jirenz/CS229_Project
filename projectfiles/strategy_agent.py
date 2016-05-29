from hearthbreaker.agents.basic_agents import *
import collections
from projectfiles.feature_extract import *
from learning.strategy import *
from learning.function_approximator import *

class StrategyAgent(DoNothingAgent):
	def __init__(self): # eta, explore_prob, discount, feature_extractor, learn = True):
		super().__init__()

	def do_card_check(self, cards):
		return [True, True, True, True]

	def do_turn(self, player):
		game = player.game
		while True:
			action = self.decide(game)
			GameHelper.execute(game, action)
			print("Me: " + str(player.hero.health) + " Him: " + str(game.other_player.hero.health))
			if action == "No_Action":
				return

	def choose_target(self, targets):
		raise
		return
		# return self.machine.choose_target(targets)

	def choose_index(self, card, player):
		raise
		return # self.machine.choose_index(card, player)

	def choose_option(self, options, player):
		raise
		# options = self.filter_options(options, player)
		return # self.machine.choose_option(options, player)

	def decide(self, game):
		max_value = -1000
		max_action = "No_Action"
		actions = GameHelper.generate_actions(game)
		for action in actions:
			new_game = game.copy()
			GameHelper.execute(new_game, action)
			new_value = BasicFunctionApproximator.eval(None, new_game)
			if new_value > max_value:
				max_value = new_value
				max_action = action
		return max_action

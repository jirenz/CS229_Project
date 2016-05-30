from projectfiles.feature_extract import *
from hearthbreaker.agents.basic_agents import *
import random
import sys

class FixedActionAgent(Agent):
	def __init__(self, chosen_index, entity_index, target_index, minion_position_index = 0):
		self.chosen_index = chosen_index
		self.entity_index = entity_index
		self.target_index = target_index
		self.minion_position_index = minion_position_index

	def do_card_check(self, cards):
		return [True, True, True, True]

	def do_turn(self, player):
		if self.chosen_index == 0:
			player.minions[self.entity_index].attack()
		elif self.chosen_index == 1:
			player.hero.attack()
		elif self.chosen_index == 2:
			player.game.play_card(player.hand[self.entity_index])
		elif self.chosen_index == 3:
			player.hero.power.use()

	def choose_target(self, targets):
		if self.target_index is not None:
			return targets[self.target_index]
		else:
			return targets[random.randint(0, len(targets) - 1)]

	def choose_index(self, card, player):
		return self.minion_position_index

	def choose_option(self, options, player):
		return options[random.randint(0, len(options) - 1)]

class GameHelper:
	def generate_actions(game):
		player = game.current_player
		if game.game_ended: return []
		actions = []
		enemy_targets = GameHelper.get_enemy_targets(player)
		for i, attack_minion in filter(lambda p: p[1].can_attack(), enumerate(player.minions)):
			actions += [(0, i, target) for target in range(len(enemy_targets))]
		if player.hero.can_attack():
			actions += [(1, None, target) for target in range(len(enemy_targets))]
		for i, card in filter(lambda p: p[1].can_use(player, player.game), enumerate(player.hand)):
			try:
				actions += [(2, i, target) for target in range(len(card.targets))]
			except:
				actions += [(2, i, None)]
		#if player.hero.power.can_use():
		#	actions += [(3, None, target) for target in range(len(player.hero.power.power_targets()))]
		actions += ["No_Action"]
		#if len(actions) > 5:
		#   print("action_size: " + str(len(actions)))
		return actions

	def get_enemy_targets(player):
		found_taunt = False
		targets = []
		for enemy in player.game.other_player.minions:
			if enemy.taunt and enemy.can_be_attacked():
				found_taunt = True
			if enemy.can_be_attacked():
				targets.append(enemy)

		if found_taunt:
			targets = [target for target in targets if target.taunt]
		else:
			targets.append(player.game.other_player.hero)
		return targets

	def execute(game, action):
		#try: 
			if action == "No_Action": return
			machine = FixedActionAgent(*action)
			agent_backup = game.current_player.agent
			game.current_player.agent = machine
			machine.do_turn(game.current_player)
			game.current_player.agent = agent_backup
			return True
		#except Exception as e:
			# game.current_player.agent = agent_backup
		#	print("Excecution Error: " + str(e))
			# print("System stack: " + sys.exc_info()[0])
		#	raise # bacause the first action fails means that the action we found is erronous
		#	return False

	def hashgame(game):
		return tuple(feature_extractor(game.current_player)).__hash__()

	def game_to_json(game):
		return json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1)

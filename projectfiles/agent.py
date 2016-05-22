from hearthbreaker.agents import *
import collections

class DoFixedThingsMachine(Agent):
    def __init__(self, choose_index, entity_index, target_index, minion_position_index = 0):
        self.choose_index = choose_index
        self.entity_index = entity_index
        self.target_index = target_index
        self.minion_position_index = minion_position_index

    def do_turn(self, player):
		if choose_index == 0:
            self.player.minions[entity_index].attack()
        elif choose_index == 1:
            self.player.hero.attack()
        elif choose_index == 2:
            self.player.game.play_card(self.player.hand[entity_index])
        elif choose_index == 3:
            self.player.hero.power.use()

    def choose_target(self, targets):
		if self.target_index is not None:
			return targets[self.target_index]
		else
			return random.randint(0, len(targets) - 1)

    def choose_index(self, card, player):
        return minion_position_index
        
    def choose_option(self, options, player):
        return options[random.randint(0, len(options) - 1)]

class AIAgent(DoNothingAgent):
	def __init__(self, eta, explore_prob, feature_extractor):
        super().__init__()
		self.eta = eta
		self.explore_prob = explore_prob
		self.feature_extractor = feature_extractor
		self.weights = collection.defaultdict(float)

    def do_card_check(self, cards):
        return [True, True, True, True]

    def do_turn(self, player):
        attack_minions = [minion for minion in filter(lambda minion: minion.can_attack(), player.minions)]
        if player.hero.can_attack():
            attack_minions.append(player.hero)
        playable_cards = [card for card in filter(lambda card: card.can_use(player, player.game), player.hand)]
        if player.hero.power.can_use():
            possible_actions = len(attack_minions) + len(playable_cards) + 1
        else:
            possible_actions = len(attack_minions) + len(playable_cards)
        if possible_actions > 0:
            action = random.randint(0, possible_actions - 1)
            if player.hero.power.can_use() and action == possible_actions - 1:
                player.hero.power.use()
            elif action < len(attack_minions):
                attack_minions[action].attack()
            else:
                player.game.play_card(playable_cards[action - len(attack_minions)])
            return True
        else:
            return False
	
	def get_enemy_targets(self, player):
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
            targets.append(self.player.game.other_player.hero)
		return targets

	def get_actions(self, player):
		if player.game.game_ended(): return []

		actions = []
		enemy_targets = self.get_enemy_targets(player)
		for i, attack_minion in filter(lambda (i, minion): minion.can_attack(), enumerate(player.minions)):
			actions += [(0, i, target) for target in xrange(len(enemy_targets))]
		if player.hero.can_attack():
			actions += [(1, None, target) for target in xrange(len(minion_targets))]
		for i, card in filter(lambda (i, card): card.can_use(player, player.game), enumerate(player.hand)):
			actions += [(2, i, target) for target in xrange(len(card.targets))]
		if player.hero.power.can_use():
			actions += [(3, None, None)]
		return actions

	def decide(self, actions):
		if random.random() < self.explore_prob:
			return random.choice(actions)
		else:
			return max((self.Q(self.player.game, action), action) for action in actions)[1]
	
	def Q(self, game, action):
		copied_game = game.copy()
		copied_game.current_player.agent = DoFixedThingsMachine(*action)
		copied_game.current_player.agent.do_turn()
		total = 0.0
		for f, v in self.feature_extractor(copied_game.current_player):
			total += self.weights[f] * v
		return total

    def do_turn(self, player):
        # copied_game = self.player.game.copy()
		actions = self.get_actions(self.player)
		if len(actions) == 0:
			return

        best_decision = self.decide(actions) #copied_game)

		oldQ = self.Q(self.player.game, best_decision)
        self.machine = DoFixedThingsMachine(*best_decision)
        self.machine.do_turn()
		
		reward = 0.0
		if self.player.game.game_ended():
			if self.player.game.winner is self.player:
				newV = 100.0
			elif self.player.game.winner is None:
				newV = 0.0
			else:
				newV = -100.0
		else:
			newV = max(self.Q(self.player.game, action) for action in self.get_actions(self.player))

		for f, v in self.feature_extractor(self.player):
			self.weights += self.eta * (reward + 1.0 * newV - oldQ)

    def choose_target(self, targets):
        return self.machine.choose_target(targets)

    def choose_index(self, card, player):
        return self.machine.choose_index(card, player)

    def choose_option(self, options, player):
        options = self.filter_options(options, player)
        return self.machine.choose_option(options, player)

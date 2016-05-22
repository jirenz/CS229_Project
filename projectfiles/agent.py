from hearthbreaker.agents import *

class DoFixedThingsMachine:
    def __init__(self, action_index, entity_index, target_index, minion_position_index = 0):
        self.action_index = action_index
        self.entity_index = entity_index
        self.target_index = target_index
        self.minion_position_index = minion_position_index

    def do_action(self, player):
        if action_index == "0":
            self.player.minions[entity_index].attack()
        elif action_index == "1":
            self.player.hero.attack()
        elif action_index == "2":
            self.player.game.play_card(self.player.hand[entity_index])
        elif action_index == "3":
            self.player.hero.power.use()

    def action_target(self, targets):
        return targets[self.target_index]

    def action_index(self, card, player):
        return minion_position_index
        
    def action_option(self, options, player):
        return options[random.randint(0, len(options) - 1)]

class AIAgent(DoNothingAgent):
        def __init__(self):
        super().__init__()

    def do_card_check(self, cards):
        return [True, True, True, True]

    def do_turn(self, player):
        copied_game = self.player.game.copy()
        best_decision = decide(copied_game)
        self.machine = DoFixedThingsMachine(*best_decision)
        self.machine.do_action()

    def choose_target(self, targets):
        return self.machine.action_target(targets)

    def choose_index(self, card, player):
        return self.machine.action_index(card, player)

    def choose_option(self, options, player):
        options = self.filter_options(options, player)
        return self.machine.action_option(options, player)


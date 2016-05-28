from projectfiles.feature_extract import *
from hearthbreaker.agents.basic_agents import *
import collections
import numpy as np
from projectfiles.feature_extract import *



class DoFixedThingsMachine(Agent):
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

class GameHelper():
    def __init__(self):
        self.base = 314159
        self.bigp = 1000000007
        pass

    def generate_actions(self, game):
        player = game.current_player
        if game.game_ended: return []

        actions = []
        enemy_targets = self.get_enemy_targets(player)
        for i, attack_minion in filter(lambda p: p[1].can_attack(), enumerate(player.minions)):
            actions += [(0, i, target) for target in range(len(enemy_targets))]
        if player.hero.can_attack():
            actions += [(1, None, target) for target in range(len(enemy_targets))]
        for i, card in filter(lambda p: p[1].can_use(player, player.game), enumerate(player.hand)):
            try:
                actions += [(2, i, target) for target in range(len(card.targets))]
            except:
                actions += [(2, i, None)]
        if player.hero.power.can_use():
            actions += [(3, None, None)]
        #if len(actions) > 5:
        #   print("action_size: " + str(len(actions)))
        return actions

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
            targets.append(player.game.other_player.hero)
        return targets

    def excecute(self, game, action):
        machine = DoFixedThingsMachine(*action)
        game.current_player.agent = machine
        machine.do_turn(game.current_player)
        return game

    def hashgame(self,game):
        player = game.current_player
        state_list = feature_extractor(player)
        ans = 1
        for i in state_list:
            ans = (ans * self.base + i ) % self.bigp;
        return ans

    def game_to_json(self, game):
        return json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1)

class StrategyNode(GameHelper):
    def __init__(self, game, state_set):
        super().__init__()
        self.generate_strategies(game, state_set)

    def generate_strategies(self, game, state_set):
        game_hash = self.hashgame(game);
        if not (game_hash in state_set):
            state_set.add(game_hash)
            self.game = game
            self.substrategies = []
            self.actions = self.generate_actions(game)
            for action in self.actions:
                outcome = game.copy()
                self.excecute(outcome, action)
                self.substrategies.append([action, StrategyNode(outcome, state_set)])
        else:
            self.game = None
            # print("hash collision found!")

    def get_outcomes(self):
        if (self.game == None): return []
        outcome = [] # action_list game(reference)
        outcome.append(self.game)
        for [action, strategy] in self.substrategies:
            outcome += strategy.get_outcomes()
        return outcome

    def get_optimal(self, path, approximator, original_state):
        value = approximator(original_state, self.game)

class StrategyManager():
    def __init__(self, function_approximator):
        self.approximator = function_approximator
        # self.approximator(state, next_state) => value
        pass

    def best_action_list(self):
        self.path = [];
        root.get_optimal(self.path, self.approximator, root.game)

    def get_outcomes(self, state):
        return self.root.get_outcomes()

    def think(self, state):
        self.store_state = set()
        self.root = StrategyNode(state, self.store_state)

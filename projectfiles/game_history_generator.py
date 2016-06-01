from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.agents import *
from projectfiles.random_deck_generator import RandomDeckGenerator
from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger
from projectfiles.feature_extract import *

class GameHistoryGenerator:
    #def generate(numgames, agent1 = TradeAgent(), agent2 = TradeAgent()):
    #    i = 0
    #    games = []
    #    while i < numgames:
    #        results = self.generate_one(agent1, agent2)
    #        if not results is None:
    #            games += results
    #            i += 1
    #    return games

    def generate_one(agent1, agent2):
        generator = RandomDeckGenerator()
        deck1 = generator.generate()
        deck2 = deck1.copy()
        game = Game([deck1, deck2], [agent1, agent2])
        try:
            history = game.start_with_history()
        except Exception as e:
            return None
        if not game.game_ended:
            return None
        return self.process_history(history)

    def process_history(history, game):
        results = []
        helper = PearExtractor()
        for historic_game in history:
            if game.winner is None:
                base_reward = 3
            else:
                if historic_game.current_player.name == game.winner.name:
                    base_reward = 10
                else: 
                    base_reward = -8
            value = base_reward * (0.7 ** (game._turns_passed - historic_game._turns_passed))
            results.append([helper(historic_game), value])
        return results

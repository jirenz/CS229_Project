from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents import *

from projectfiles.random_deck_generator import RandomDeckGenerator
from projectfiles.agent import *
import sys
import shelve

from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger
from projectfiles.agent import *
from projectfiles.feature_extract import *
from projectfiles import *
from learning.strategy import StrategyManager
from learning.model import *

def test_strategy():
    generator = RandomDeckGenerator()
    deck1 = generator.generate()
    deck2 = deck1.copy()
    game = Game([deck1, deck2], [TradeAgent(), TradeAgent()])
    game.pre_game()
    game.current_player = game.players[1]
    while not game.game_ended:
        manager = StrategyManager(StatePairLinearModel(RelativeResourceExtractor()))
        manager.think(game)
        outcomes = manager.get_outcomes()
        print("Number of outcomes: " + str(len(outcomes)) + '\n')
        # for situation in outcomes:
        #     print("See: " + str(situation.other_player.hero.__to_json__()) + '\n')
        # input("Presss enter to continue:")

        game.play_single_turn()

if __name__ == "__main__":
    for i in range(10):
        test_strategy()

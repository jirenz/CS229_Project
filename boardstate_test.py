from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents import *

from projectfiles.random_deck_generator import RandomDeckGenerator
import sys
import shelve

from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger

def generate_one(filename):
    loader = DeckLoader()
    generator = RandomDeckGenerator()
    # deck1 = loader.load_deck("zoo.hsdeck")
    # deck2 = loader.load_deck("zoo.hsdeck")
    deck1 = generator.generate()
    deck2 = generator.generate()
    game = Game([deck1, deck2], [TradeAgent(), TradeAgent()])
    new_game = game.copy()
    game_log = Hearthlogger()
    game_log.attach(new_game)
    try:
        new_game.start()
    except Exception as e:
       #print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
       #print(new_game._all_cards_played)
       del new_game
       del game_log

       return False
    # print("winning agent: " + new_game.winner.agent.__class__.__name__)
    game_log.save(filename)
    del new_game
    del game_log
    return True

def generate_number(folder_name, prefix, start, over):
    i = start
    while i < over:
        if generate_one(folder_name + prefix + "_" + str(i)):
            i += 1

def enshelf_one(index):
    loader = DeckLoader()
    generator = RandomDeckGenerator()
    # deck1 = loader.load_deck("zoo.hsdeck")
    # deck2 = loader.load_deck("zoo.hsdeck")
    deck1 = generator.generate()
    deck2 = generator.generate()
    game = Game([deck1, deck2], [TradeAgent(), TradeAgent()])
    new_game = game.copy()
    game_log = Hearthlogger()
    game_log.attach(new_game)
    try:
        new_game.start()
    except Exception as e:
       #print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
       #print(new_game._all_cards_played)
       del new_game
       del game_log
       print(e)
       return False
    # print("winning agent: " + new_game.winner.agent.__class__.__name__)
    game_log.shelf(index)
    del new_game
    del game_log
    return True

def populate_shelf(start, over):
    i = start
    while i < over:
        if enshelf_one(i):
            i += 1

if __name__ == "__main__":
    if sys.argv[1] == "-j":
        generate_number("projectfiles/LR-statevalue/logfiles/", "test_one", int(sys.argv[2]), int(sys.argv[3]))
    if sys.argv[1] == "-s":
        populate_shelf(int(sys.argv[2]), int(sys.argv[3]))



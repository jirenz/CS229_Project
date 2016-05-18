from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents.basic_agents import *

import sys

from projectfiles.deck_loader import DeckLoader

def generate():
    loader = DeckLoader()
    deck1 = loader.load_deck("zoo.hsdeck")
    deck2 = loader.load_deck("zoo.hsdeck")
    game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
    new_game = game.copy()

    try:
        new_game.start_with_log()
    except Exception as e:
        print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
        print(new_game._all_cards_played)
        raise e

    del new_game
    print("done!")

if __name__ == "__main__":
    generate()
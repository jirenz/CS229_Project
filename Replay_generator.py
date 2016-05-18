from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents.basic_agents import *

import sys

from projectfiles.deck_loader import DeckLoader

def generate_replays():
    loader = DeckLoader()
    deck1 = loader.load_deck("zoo.hsdeck")
    deck2 = loader.load_deck("zoo.hsdeck")
    game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
    new_game = game.copy()
    replay = record(new_game)
    try:
        new_game.start()
    except Exception as e:
        print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
        print(new_game._all_cards_played)
        raise e

    replay.write_json("replay_text.hsreplay")
    del new_game
    print("done!")

def log_gamestates():
    replay = Replay().read_json("replay_text.hsreplay")
    print("done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("not enough arguments provided\n")
        sys.exit()
    if sys.argv[1] == '-g':
        generate_replays()
    elif sys.argv[1] == '-l':
        log_gamestates()
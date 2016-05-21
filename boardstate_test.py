from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents.basic_agents import *

import sys

from projectfiles.deck_loader import DeckLoader

class Hearthlogger:

    def __init__(self):
        self.game = None
        self.states = []
        self.winner = None

    def attach(self, game):
        game.tracking = True
        game.logger = self
        self.game = game

    def log(self, json_str):
        self.states.append(json_str)

    def save(self, file_name = "default_log.txt"):
        with open(file_name, "w") as text_file:
            if self.winner:
                text_file.write("winner: " + self.winner + '\n')
            for state in self.states:
                text_file.write(state)
                text_file.write('\n')
        text_file.close()
        print("Saved to " + file_name + '.\n')


def generate():
    loader = DeckLoader()
    deck1 = loader.load_deck("zoo.hsdeck")
    deck2 = loader.load_deck("zoo.hsdeck")
    game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
    new_game = game.copy()
    game_log = Hearthlogger()
    game_log.attach(new_game)
    try:
        new_game.start_with_debug()
    except Exception as e:
        print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
        print(new_game._all_cards_played)
        game_log.save()
        raise e

    game_log.save("log1.txt")
    del new_game
    print("done!")

if __name__ == "__main__":
    generate()


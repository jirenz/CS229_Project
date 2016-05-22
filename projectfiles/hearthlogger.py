from hearthbreaker.engine import Deck, card_lookup, Game
import json
import shelve

class Hearthlogger:

    def __init__(self):
        self.game = None
        self.states = []
        self.winner = None
        self.games = []

    def attach(self, game):
        game.tracking = True
        game.logger = self
        self.game = game

    def log(self, json_str):
        self.states.append(json_str)
        self.games.append(self.game.copy())

    def save(self, file_name = "default_log"):
        file_name += ".hslog"
        with open(file_name, "w") as text_file:
            if self.winner:
                text_file.write("winner: " + self.winner + '\n')
            for state in self.states:
                text_file.write(state)
                text_file.write('\n')
        text_file.close()
        print("Saved to " + file_name + '.\n')

    def shelf(self,number):
        s = shelve.open("projectfiles/LR-statevalue/gamefiles.dat",writeback=True)
        if not "gamelogger" in s:
            s["gamelogger"] = []
        s["gamelogger"].append(self)
        s.close()

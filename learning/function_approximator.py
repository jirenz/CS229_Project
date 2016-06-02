from hearthbreaker.engine import *
from projectfiles.feature_extract import *
import numpy as np
import random

from projectfiles.game_history_generator import *
from sklearn import linear_model
from sknn.mlp import Regressor, Layer
# from projectfiles.pear_extractor import *

#print("function_approximator.py is deprecated")


class BasicFunctionApproximator:
    def __init__(self):
        pass
        
    def eval(self, state_1, state_2):
        def score(player):
            score = 0
            for i in player.minions:
                score += i.calculate_attack()
                score += i.health
            score += len(player.hand) * 2
            score += player.hero.health + player.hero.armor
            return score

        return score(state_2.current_player) - score(state_2.other_player)

class SimpleExtractor:
    def extract(player):
        attack = 0;
        health = 0;
        for i in player.minions:
            attack += i.calculate_attack()
            health += i.health
        feat = [attack, health]
        feat.append(len(player.hand))
        feat.append(player.hero.health + player.hero.armor)
        feat.append(player.game.other_player.hero.health)
        return np.array(feat, dtype=np.float64)

    def initial():
        return np.zeros((5, ))
    
class LinearFunctionApproximator():
    def __init__(self, initial_weights = None):
        self.extractor = PearExtractor()
        self.train()
        #if initial_weights is None:
        #   self.weights = self.extractor.get_initial()
        #else:
        #   self.weights = initial_weights

    def __call__(self, state):
        #print(len(self.extractor(state)), len(self.weights))
        return self.eval(state)

    def eval(self, state):
        if state.current_player_win(): return 100000000
        if state.current_player_lose(): return -10000000    
        return np.dot(self.extractor(state), self.weights)

    def train(self):
        Data = open("data.txt", "r")
        Tmp = Data.read().splitlines()
        training_set = []
        for i in Tmp:
            c = i.split(" ")
            for j in range(0, len(c)):
                c[j] = float(c[j])
            training_set.append(c)
        clf = linear_model.LinearRegression()
        X = []
        y = []
        for data_point in training_set:
            X.append(data_point[0:-1])
            y.append(data_point[-1])
        for i in X:
            if (len(i) != 38):
                print(i)
        clf.fit(X, y)
        self.weights = clf.coef_
        print("Learning from data size: " + str(len(y)))
        Data.close()

class BasicNeuroApproximator():
    def __init__(self, initial_weights = None, nn = None):
        self.extractor = PearExtractor()
        if nn is None:
            self.nn = self.regressor()
        else:
            self.nn = nn
        self.train()
        #if initial_weights is None:
        #   self.weights = self.extractor.get_initial()
        #else:
        #   self.weights = initial_weights

    def regressor(self):
        return Regressor(
            layers=[
            Layer("Rectifier", units=100),
            # Layer("Sigmoid", units = 200),
            # Layer("Tanh", units = 100)
            Layer("Linear")],
            learning_rate=0.001,
            n_iter=10,
            f_stable = 0.1)

    def __call__(self, state):
        #print(len(self.extractor(state)), len(self.weights))
        return self.eval(state)

    def eval(self, state):
        if state.current_player_win(): return 100000000
        if state.current_player_lose(): return -10000000
        vec = np.array(self.extractor(state))
        return self.nn.predict(np.ndarray(shape = (1, len(vec)), buffer = vec))

    def train(self):
        Data = open("data.txt", "r")
        Tmp = Data.read().splitlines()
        training_set = []
        for i in Tmp:
            c = i.split(" ")
            for j in range(0, len(c)):
                c[j] = float(c[j])
            training_set.append(c)
        clf = linear_model.LinearRegression()
        X = []
        y = []
        for data_point in training_set:
            X.append(data_point[0:-1])
            y.append(data_point[-1])
        for i in X:
            if (len(i) != 38):
                print(i)
        X = np.ndarray(shape = (len(y), len(X[0])), buffer = np.array(X))
        y = np.ndarray(shape = (len(y), 1), buffer = np.array(y))
        self.nn.fit(X, y)
        print("Learning from data size: " + str(len(y)))
        Data.close()

class DeepNeuroApproximator(BasicNeuroApproximator):
    def regressor(self):
        return Regressor(
            layers=[
            Layer("Rectifier", units=100),
            Layer("Sigmoid", units = 200),
            Layer("Tanh", units = 100),
            Layer("Linear")],
            learning_rate=0.001,
            n_iter=10,
            f_stable = 0.1)
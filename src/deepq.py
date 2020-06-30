from random import random

from PyQt5.QtWidgets import (QGraphicsScene)
import numpy as np

from car import Car
from weightset import WeightSet
from memory import Memory

class DeepQ():
    def __init__(self, car, map):
        self.car = car
        self.map = map
        self.mem = Memory(10)

        (n_inputs, n_hidden, n_output) = self.car.getNNStructure()
        w = WeightSet(n_inputs, n_hidden, n_output, self.car.getWeightSet())
        w.mutate(1.0)
        self.car.setWeightSet(w)

        self.explore_probability = 0.8

    def run(self):
        action = "exploit"

        #if self.mem.size() < 10:
        #    action = "explore"
        #elif random() > self.explore_probability:
        #    action = "explore"

        if action == "explore":
            # select random
            # execute action
            # get loss (optimal - current)
            # store to memory
            pass
        elif action == "exploit":
            print("exploit")
            previous_score = self.car.getScore()
            best_score = previous_score + 1

            # run network & execute action
            actions = self.car.runNN()

            # update score
            self.map.updateScore(self.car)

            # get loss
            current_score = self.car.getScore()
            loss = best_score - current_score

            # store to memory
            self.mem.push(self.car.getEndPointLengths(), actions, loss)

        if self.mem.isFull():
            #self.learn()
            self.nextEpisode()

        if self.car.isCrashed():
            self.nextEpisode()

    def learn(self):
        pass

    def nextEpisode(self):
        print("nextEpisode")
        self.mem.clear()

        (n_inputs, n_hidden, n_output) = self.car.getNNStructure()
        w = WeightSet(n_inputs, n_hidden, n_output, self.car.getWeightSet())
        w.mutate(1.0)
        self.car.setWeightSet(w)

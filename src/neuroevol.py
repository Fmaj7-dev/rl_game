import random

from PyQt5.QtWidgets import (QGraphicsScene)
import numpy as np

from car import Car
from weightset import WeightSet

class NeuroEvol():
    def __init__(self, cars, map):
        self.cars = cars
        self.map = map
        self.num_cars = len(cars)

        # current generation we are on
        self.generation = 0

        self.score = 0
        self.last_score = 0
        self.repeated_score = 0

        # number of ticks (runs) of the current generation
        self.num_ticks = 0

        # max time of the generation
        self.MAX_TICKS = 1000

        self.previous_best_car = 0
        self.previous_best_weights = 0
        self.previous_best_score = 0
        self.best_weights = None

        self.game_won = False

    def run(self):

        num_cars_crashed = 0
        self.num_ticks += 1

        for i, car in enumerate(self.cars):

            if car.getScore() > 250 or self.game_won == True:
                print()
                print("************ GAME WON *************")
                #s = input("press enter : ") 
                self.game_won = True

            if car.isCrashed():
                num_cars_crashed += 1
                continue

            # if the car went backwards
            if car.getScore() < car.getPreviousScore() and self.game_won == False:
                if self.num_ticks > 10:
                    #print("END 1")
                    car.setCrashed()

            # ignore crashed cars
            if car.isCrashed():
                num_cars_crashed += 1
                continue
            
            x1, y1 = car.getPosition()            
            car.runNN()
            car.update()

            x2, y2 = car.getPosition()

            # after the first 10 ticks, stop every car that does not advance
            if self.num_ticks > 10 and abs(x1-x2)<0.01 and abs(y1-y2)<0.01 and self.game_won == False:
                car.setCrashed()
                #print("END 2*")
                num_cars_crashed += 1

            self.map.updateScore(car)

            # detect collision
            if self.map.isColliding(car):
                #print("END 3**")
                car.setCrashed()
                num_cars_crashed += 1

            self.map.laserCollision(car)

        # if every car crashed or time is up
        if num_cars_crashed >= self.num_cars:
            self.score = self.nextGeneration()
            if self.last_score == self.score:
                self.repeated_score += 1
            else:
                self.last_score = self.score



        # advance to the next generation only if the score < 250
        # once the score reaches 250 we can assume the game has been resolved
        if self.score < 250 and self.num_ticks == self.MAX_TICKS and self.game_won == False:
            print("END3")
            print()
            self.score = self.nextGeneration()
        
        return self.generation, self.score, self.best_weights

    def nextGeneration(self):
        # get best car & weights
        best_car, best_score, second_best_car, second_best_score = self.getBestCar()
        self.best_weights = self.cars[best_car].getWeightSet()
        #second_best_weights = self.cars[second_best_car].getWeightSet()


#        if self.previous_best_score != self.cars[0].getScore():
#            print("-----> DETERMINISM <------")
#            print("previous best score: " + str(self.previous_best_score))
#            print("current best score: "+str(self.cars[0].getScore()))
#            print(self.cars[0].getWeightSet())
#            print("-----> DETERMINISM <------")
            

        if self.previous_best_car != best_car:
            #previous_best_weights_now = self.cars[self.previous_best_car].getWeightSet()
            #previous_best_car_score_now = self.cars[self.previous_best_car].getScore()

            self.previous_best_car = best_car
            self.previous_best_weights = self.best_weights
            self.previous_best_score = best_score

        # get nn structure 
        (n_inputs, n_hidden, n_output) = self.cars[best_car].getNNStructure()

        for i, car in enumerate(self.cars):
            # car 0 will hold the best car
            if i == 0:
                w = WeightSet(n_inputs, n_hidden, n_output, self.best_weights)

                car.setWeightSet(w)
                #idd = np.sum(self.cars[0].getWeightSet())
            
            else:
                w = WeightSet(n_inputs, n_hidden, n_output, self.best_weights)
                w.mutate(np.random.rand())
                car.setWeightSet(w)

            car.setCrashed(False)
            car.reset()
            #"""

        self.generation += 1
        self.num_ticks = 0

        #idd = np.sum(self.cars[0].getWeightSet())
        #print("finishing nextGeneration: " + str(idd))
        print("########### GENERATION " +str(self.generation))

        return best_score

    def getBestCar(self):
        best_score = 0
        best_car = 0

        for i, car in enumerate(self.cars):
            score = car.getScore()
            #idd = np.sum(car.getWeightSet())
            #print("score of car # "+str(i) +": " + str(score) +" -> " + str(car.getWeightSet()[0]) + " " +str(car.getWeightSet()[1])+ " " +str(car.getWeightSet()[2])+ " " +str(car.getWeightSet()[3]) )
            #print("score of car # "+str(i) +": " + str(score) +" -> " + str(idd) )
            if  score > best_score:
                best_car = i
                best_score = score

        # faster
        second_best_score = 0
        second_best_car = 0

        for i, car in enumerate(self.cars):
            score = car.getScore()
            if i != best_car:
                if  score >= second_best_score:
                    second_best_car = i
                    second_best_score = score

        # just for debugging
        for i, car in enumerate(self.cars):
            score = car.getScore()
            idd = np.sum(car.getWeightSet())

            if i == 0:
                print("best previous car: " + str(idd))

            if i == best_car:
                print("score of car # "+str(i) +": " + str(score) +" -> " + str(idd) + " <<<<<")
            elif i == second_best_car:
                print("score of car # "+str(i) +": " + str(score) +" -> " + str(idd) + " <<")
            else:
                print("score of car # "+str(i) +": " + str(score) +" -> " + str(idd))

        return (best_car, best_score, second_best_car, second_best_score)

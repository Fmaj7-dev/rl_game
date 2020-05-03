import random

from PyQt5.QtWidgets import (QGraphicsScene)

from car import Car
from weightset import WeightSet

class NeuroEvol():
    def __init__(self, cars, map):
        self.cars = cars
        self.map = map
        self.num_cars = len(cars)

        # current generation we are on
        self.generation = 0

        # number of ticks (runs) of the current generation
        self.num_ticks = 0

        # max time of the generation
        self.MAX_TICKS = 500

    def run(self):

        num_cars_crashed = 0
        self.num_ticks += 1

        for i, car in enumerate(self.cars):
            #print ("processing car number "+str(i))
            if car.isCrashed():
                num_cars_crashed += 1
                continue

            # test logic
            """if i == 0:
                lengths = car.getEndPointLengths()
                if len(lengths) > 9:
                    if lengths[1] +lengths[2]+10 < lengths[9] + lengths[8]:
                        car.steerLeft()
                    elif lengths[9] + lengths[8] +10 < lengths[1] + lengths[2]:
                        car.steerRight()
                    else:
                        car.accelerate()

                if random.randint(0,3) == 0:
                    car.accelerate()

                if random.randint(0,100) == 0:
                    pass#car.steerRight()
                
                if random.randint(0,100) == 0:
                    pass#car.steerLeft()

            else:
                #pass
                car.runNN()"""
            
            car.runNN()
            
            car.update()

            self.map.updateScore(car)

            if self.map.isColliding(car):
                car.setCrashed()

            self.map.laserCollision(car)

        # if every car crashed or time is up
        if num_cars_crashed == self.num_cars or self.num_ticks == self.MAX_TICKS:
            print("NEXT GENERATION")
            self.nextGeneration()
            

    def nextGeneration(self):
        # get best car & weights
        best_car, best_score = self.getBestCar()
        best_weights = self.cars[best_car].getWeightSet()

        print("Best Score: "+str(best_score))

        # get nn structure 
        (n_inputs, n_hidden, n_output) = self.cars[best_car].getNNStructure()

        for i, car in enumerate(self.cars):
            if i != best_car:
                w = WeightSet(n_inputs, n_hidden, n_output, best_weights)
                w.mutate(0.5)
                car.setWeightSet(w)
                print(w)

            car.setCrashed(False)
            car.reset()
            

        self.generation += 1
        self.num_ticks = 0

    def getBestCar(self):
        best_score = 0
        best_car = 0

        for i, car in enumerate(self.cars):
            score = car.getScore()
            print("score of car # "+str(i) +": " + str(score))
            if  score > best_score:
                best_car = i
                best_score = score

        return (best_car, best_score)

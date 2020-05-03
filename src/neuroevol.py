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

        self.score = 0

        # number of ticks (runs) of the current generation
        self.num_ticks = 0

        # max time of the generation
        self.MAX_TICKS = 500

        self.previous_best_car = 0
        self.previous_best_weights = 0
        self.previous_best_score = 0

    def run(self):

        num_cars_crashed = 0
        num_cars_stopped = 0
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

            x1, y1 = car.getPosition()            
            car.runNN()
            car.update()

            x2, y2 = car.getPosition()

            if abs(x1-x2)<0.01 and abs(y1-y2)<0.01:
                num_cars_stopped += 1

            self.map.updateScore(car)

            if self.map.isColliding(car):
                car.setCrashed()

            self.map.laserCollision(car)

        # if every car crashed or time is up
        """if num_cars_crashed + num_cars_stopped == self.num_cars:
            print("cars stopped")
            self.score = self.nextGeneration()"""

        if self.num_ticks == self.MAX_TICKS:
            print("max ticks reached")
            self.score = self.nextGeneration()
        
        return self.generation, self.score

    def nextGeneration(self):
        # get best car & weights
        best_car, best_score = self.getBestCar()
        best_weights = self.cars[best_car].getWeightSet()

        f = open("bests.txt", "a")
        f.write("\n------------------------")
        f.write("\nBest car "+str(best_car)+" score: "+str(best_score)+" \n\n")
        f.write(str(best_weights))

        if self.previous_best_car != best_car:
            f.write("\nPrevious best car "+str(self.previous_best_car)+" score: "+str(self.previous_best_score)+" \n")
            f.write(str(self.previous_best_weights))

            print()

            previous_best_weights_now = self.cars[self.previous_best_car].getWeightSet()
            previous_best_car_score_now = self.cars[self.previous_best_car].getScore()

            f.write("\nPrevious best car: "+str(self.previous_best_car)+" Previous best score now: "+str(previous_best_car_score_now)+" \n")
            f.write("Previous best car weights \n"+str(previous_best_weights_now)+" \n")

            self.previous_best_car = best_car
            self.previous_best_weights = best_weights
            self.previous_best_score = best_score

        f.close()        

        # get nn structure 
        (n_inputs, n_hidden, n_output) = self.cars[best_car].getNNStructure()

        for i, car in enumerate(self.cars):
            if i != best_car:
                w = WeightSet(n_inputs, n_hidden, n_output, best_weights)
                if best_score == 31:
                    w = WeightSet(n_inputs, n_hidden, n_output)
                    w.mutate(1.0)
                else:
                    w.mutate(0.5)

                car.setWeightSet(w)
                #print(w)
                print("mutating: " + str(i)+ " -> " +str(w.weights[0])+ " "+str(w.weights[1]) + " "+str(w.weights[2]))
            else:
                if best_score == 31:
                    w = WeightSet(n_inputs, n_hidden, n_output)
                    w.mutate(1.0)
                    car.setWeightSet(w)
                    print("mutating: " + str(i)+ " -> " +str(w.weights[0])+ " "+str(w.weights[1]) + " "+str(w.weights[2]))
                else:
                    print("not mutating: " + str(i)+ " -> " +str(car.getWeightSet()[0]) + " "+str(car.getWeightSet()[1])+ " "+str(car.getWeightSet()[2]))

            car.setCrashed(False)
            car.reset()
            

        self.generation += 1
        self.num_ticks = 0

        return best_score

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

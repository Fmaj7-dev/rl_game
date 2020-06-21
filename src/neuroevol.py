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

        self.game_won = False

    def run(self):

        num_cars_crashed = 0
        self.num_ticks += 1

        for i, car in enumerate(self.cars):

            if car.getScore() > 250:
                print()
                print("************ GAME WON *************")
                s = input("press enter : ") 
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

        
        
        return self.generation, self.score

    def nextGeneration(self):
        # get best car & weights
        best_car, best_score, second_best_car, second_best_score = self.getBestCar()
        best_weights = self.cars[best_car].getWeightSet()
        second_best_weights = self.cars[second_best_car].getWeightSet()


#        if self.previous_best_score != self.cars[0].getScore():
#            print("-----> DETERMINISM <------")
#            print("previous best score: " + str(self.previous_best_score))
#            print("current best score: "+str(self.cars[0].getScore()))
#            print(self.cars[0].getWeightSet())
#            print("-----> DETERMINISM <------")
            

        if self.previous_best_car != best_car:
            previous_best_weights_now = self.cars[self.previous_best_car].getWeightSet()
            previous_best_car_score_now = self.cars[self.previous_best_car].getScore()

            self.previous_best_car = best_car
            self.previous_best_weights = best_weights
            self.previous_best_score = best_score

        # get nn structure 
        (n_inputs, n_hidden, n_output) = self.cars[best_car].getNNStructure()

        """
        #breakpoint()
        for i, car in enumerate(self.cars):
            if i != best_car:
                w = WeightSet(n_inputs, n_hidden, n_output, best_weights)
                if best_score == 31:
                    w = WeightSet(n_inputs, n_hidden, n_output)
                    w.mutate(1.0)
                else:
                    w.mutate(0.2)

                car.setWeightSet(w)
                print("mutating: " + str(i)+ " -> " +str(w.weights[0])+ " "+str(w.weights[1]) + " "+str(w.weights[2]))

            # if the best car is still on the origin, we will random its weights again
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

        #"""

        #"""
        for i, car in enumerate(self.cars):
            # car 0 will hold the best car
            if i == 0:
                w = WeightSet(n_inputs, n_hidden, n_output, best_weights)

                car.setWeightSet(w)
                idd = np.sum(self.cars[0].getWeightSet())


            # car 1 will have the second best car
#            elif i == 1:
#                #w = WeightSet(n_inputs, n_hidden, n_output, second_best_weights)
#                w = WeightSet(n_inputs, n_hidden, n_output, [-2.215822425020668, -0.19543484652276386, -0.7877224332655192, -1.0677225770385452, 1.963552833543816, 0.7927110177336647, -1.7325688023980281, 1.0578010075419184, -0.47482378421047405, 0.23492812508811559, 0.8155010224442626, 0.3780462604278832, 2.45987198502938, 0.781497239460632, -0.8642852619405358, 1.135620585491476, 0.6727567871994219, -1.1785727847701737, 0.8066764021643629, 0.30638280074245927, 0.34535686073450617, 0.9443852228353897, 0.6776371019248881, -0.007674063684503472, 1.9330652257107903, 0.9148677980978497, -0.08837328752639602, 2.2106897260157643, 0.8049333907323256, 2.190417001188423, -0.8727849535276425, 1.1347210354858641, 1.9740786877450238, -0.5102911595630633, 1.1026920460743783, 0.17782979970543425, -0.5297677059230407, -0.47996464271220896, -0.8669840205875055, 0.12086216760273172, -0.17963037272551532, 0.8182179165456491, -1.718203895546123, -0.4719921726233347, 1.4974316831796264, 0.25800099766949486, -0.9026543599878197, 0.40021839083867333, 0.24207067028796736, -0.9445294576993009, 0.8639235499624459, -0.08857106726878992, 0.7812571909962575, 1.1440926945412941, 0.20419746861408708, -0.7541921187951445, -2.010216654566063, -2.0843316213428005, -0.5582302623977843, 0.6128253216693214, 0.06578864864896251, -0.35188217414045164, -0.16007448660830478, -0.7064755007657966, 0.032264810771252796, -0.2562739365599819, -0.1825848784124418, -0.5545932404325518, 1.1747618002330382, 0.7124817644338045, 0.5595469343023752, 0.15032388659522092, 0.920419303313525, -1.3528658889640388, 0.04621160367091715, 0.36972874103394227, 1.494141897266825, -0.01605403924858619, -0.7696127630272848, -1.0261395775913584, 0.026185149185798437, 0.07128726054946169, -0.7975065804790082, -0.7084881015290911, 0.5838830222840011, 1.2841046951788975, -1.5072258203839384, 0.102208999741308, 0.42876125888076383, 1.937562720390904, -0.43772557538684836, 0.014040818007840617, -0.05678859588627712, 0.5298100656836389])
#               
#                [-2.215822425020668, 1.9860255392481883, 0.8970972558139287, -1.6442408789103549, 1.963552833543816, 0.9286347673223432, -0.19902502391952712, -0.5951426741041482, -0.47482378421047405, 0.23492812508811559, 0.3054616396189878, 0.3780462604278832, 2.45987198502938, 0.48328570877898486, 0.1862210394043706, 1.135620585491476, 0.6727567871994219, -0.19109391507143272, -1.391378308187495, 0.38908568992215947, 0.34535686073450617, 0.9443852228353897, 0.6776371019248881, -0.007674063684503472, -1.3157751173477283, 0.9148677980978497, 1.2019734751142657, 2.2106897260157643, 0.8049333907323256, 2.190417001188423, 1.005635737777903, 1.1347210354858641, 1.9740786877450238, -0.5102911595630633, -0.27734274873427583, 0.17782979970543425, -1.3211623359590354, 1.4720580310344626, -0.8669840205875055, 0.12086216760273172, -0.17963037272551532, 1.9123596419164914, -1.718203895546123, -0.4719921726233347, 0.5112029511152223, 0.25800099766949486, -0.9026543599878197, -0.6649464205381669, 0.24207067028796736, -0.9445294576993009, 0.3113036974347176, -0.08857106726878992, 1.7000461456184004, 1.1440926945412941, 0.20419746861408708, -0.683547349751068, -2.010216654566063, -2.0843316213428005, 0.2967286223260184, 0.6128253216693214, 0.06578864864896251, -0.35188217414045164, -0.16007448660830478, 0.3971935132750622, 0.8224252227075678, -0.2562739365599819, -0.1825848784124418, -0.6052229943297487, 1.1747618002330382, 0.7124817644338045, 0.5595469343023752, -2.539610093623961, 0.920419303313525, -1.3528658889640388, -1.0758693164342827, -0.06732870874897676, -0.18197804685512634, -0.01605403924858619, -1.3770809275199376, -1.0261395775913584, 0.026185149185798437, 0.07128726054946169, 1.2365889728135153, -0.12876680887658984, -0.7050966266325779, 1.2841046951788975, -1.5072258203839384, 0.102208999741308, 0.42876125888076383, 0.34371379247115486, -0.43772557538684836, 0.014040818007840617, -0.05678859588627712, 0.5298100656836389]
#                car.setWeightSet(w)
#            # car 2 and 3 will have a mixture between the best two
#            elif i < 10:
#                w1 = WeightSet(n_inputs, n_hidden, n_output, best_weights)
#                w2 = WeightSet(n_inputs, n_hidden, n_output, second_best_weights)
#                wmix = WeightSet.mix(w1, w2)
#                car.setWeightSet(wmix)
#            # car 4..n will have random mutations of the best car

            
            else:
                w = WeightSet(n_inputs, n_hidden, n_output, best_weights)
                w.mutate(np.random.rand())
                car.setWeightSet(w)

            car.setCrashed(False)
            car.reset()
            #"""

        self.generation += 1
        self.num_ticks = 0

        idd = np.sum(self.cars[0].getWeightSet())
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

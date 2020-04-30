import random

from PyQt5.QtWidgets import (QGraphicsScene)

from car import Car

class NeuroEvol():
    def __init__(self, cars, map):
        self.cars = cars
        self.map = map

    def run(self):
        for i, car in enumerate(self.cars):
            #print ("processing car number "+str(i))
            if car.isCrashed():
                continue

            # test logic
            if i == 0:
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
                car.runNN()

            car.update()

            if self.map.isColliding(car):
                car.setCrashed()

            self.map.laserCollision(car)


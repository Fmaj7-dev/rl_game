import random

from PyQt5.QtWidgets import (QGraphicsScene)

from car import Car

class NeuroEvol():
    def __init__(self, cars, map):
        self.cars = cars
        self.map = map

    def run(self):
        for i, car in enumerate(self.cars):
            if car.isCrashed():
                continue

            # test logic
            if i == 0:
                lengths = car.getEndPointLengths()
                print(len(lengths))
                if len(lengths) > 9:
                    if lengths[1] +10 < lengths[9]:
                        car.steerLeft()
                        print("left")
                    elif lengths[9] +10 < lengths[1]:
                        car.steerRight()
                        print("right")
                    else:
                        car.accelerate()
                        print("accel")

            if random.randint(0,3) == 0:
                car.accelerate()

            if random.randint(0,100) == 0:
                car.steerRight()
            
            if random.randint(0,100) == 0:
                car.steerLeft()

            car.update()

            if self.map.isColliding(car):
                car.setCrashed()

            self.map.laserCollision(car)


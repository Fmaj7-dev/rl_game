import random

from PyQt5.QtWidgets import (QGraphicsScene)

from car import Car

class NeuroEvol():
    def __init__(self, cars, map):
        self.cars = cars
        self.map = map

    def run(self):
        for car in self.cars:
            if car.isCrashed:
                continue

            if random.randint(0,3) == 0:
                car.accelerate()

            if random.randint(0,5) == 0:
                car.steerRight()
            
            if random.randint(0,5) == 0:
                car.steerLeft()

            car.update()

            if self.map.isColliding(car):
                car.setCrashed()

            self.map.laserCollision(car)


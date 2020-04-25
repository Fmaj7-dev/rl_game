from PyQt5.QtWidgets import (QGraphicsScene)

from car import Car

class NeuroEvol():
    def __init__(self, cars, map):
        self.cars = cars
        self.map = map

    def run(self):
        for car in self.cars:
            car.accelerate()
            car.steerRight()
            car.update()

            if self.map.isColliding(car):
                car.setCrashed()

            self.map.laserCollision(car)


from car import Car

import math

from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage)


class Map():
    def __init__(self, scene, view):
        self.background = QPixmap ("../resources/maps/level1/background.png")
        self.collision = QPixmap("../resources/maps/level1/collision.png")
        _ = scene.addPixmap(self.background)
        view.resize(self.background.size().width(), self.background.size().height() )

    def isColliding(self, car):
        points = car.getAllCollisionPoints()
        
        for point in points:
            x = point[0]
            y = point[1]

            pixel = self.collision.toImage().pixel(x, y)
            colors = QColor(pixel).getRgb()

            if colors[0:3] == (0,0,0):
                return True

        return False

    def laserCollision(self, car):
        x, y = car.getPosition()
        lasers = car.getLaserAngles()
        angle = car.getAngle()
        length = 500

        endPoints = []

        for laser in lasers:
            absolute_angle = angle + laser
            
            y_increment = length * math.cos( math.radians( absolute_angle ) )
            x_increment = length * math.sin( math.radians( absolute_angle ) )

            # absolute position of corner
            y_abs = y - y_increment
            x_abs = x + x_increment

            endPoints.append( (x_abs, y_abs) )

            #pixel = self.collision.toImage().pixel(x_abs, y_abs)
            #colors = QColor(pixel).getRgb()

        #car.setEndPoints(endPoints)

        laserEnds = []
        laserEndLengths = []
        for endPoint in endPoints:
            dx = (endPoint[0] - x )/length
            dy = (endPoint[1] - y )/length

            for i in range(length):
                check_x = x + dx*i
                check_y = y + dy*i

                pixel = self.collision.toImage().pixel(check_x, check_y)
                #print("x: "+str(check_x)+ "y: "+str(check_y))
                colors = QColor(pixel).getRgb()

                if colors[0:3] == (0,0,0):
                    laserEnds.append((check_x, check_y))
                    laserEndLengths.append(i)
                    break
        
        car.setEndPoints(laserEnds, laserEndLengths)
        
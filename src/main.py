import math
import numpy as np

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap)

class Car():
    def __init__(self, scene, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        self.speed = 0

        self.inertia_x = 0
        self.inertia_y = 0

        self.MAX_SPEED = 3
        self.ACCEL = 0.5
        self.INERTIA = 0.95
        self.FRICTION = 0.97

        pix = QPixmap("../resources/red_car.png")
        self.car = scene.addPixmap( pix )
        
        self.car.setPos(self.x, self.x)
        self.car.setRotation(angle)
        self.car.setOffset(-pix.width()/2, -pix.height()/3)


        print(self.x, self.y)

    def moveForward(self):
        y_increment = self.speed * math.cos( math.radians( self.angle ) )
        x_increment = self.speed * math.sin( math.radians( self.angle ) )

        self.inertia_y = self.INERTIA * self.inertia_y + (1-self.INERTIA) * y_increment
        self.inertia_x = self.INERTIA * self.inertia_x + (1-self.INERTIA) * x_increment

        self.y -= self.inertia_y
        self.x += self.inertia_x
        self.car.setPos(self.x, self.y)

    def moveBackward(self):
        y_increment = self.speed * math.cos( math.radians( self.angle ) )
        x_increment = self.speed * math.sin( math.radians( self.angle ) )

        inertia = 0.95

        self.inertia_y = self.INERTIA * self.inertia_y + (1-self.INERTIA) * y_increment
        self.inertia_x = self.INERTIA * self.inertia_x + (1-self.INERTIA) * x_increment

        self.y += self.inertia_y
        self.x -= self.inertia_x
        """self.y += self.speed * math.cos( math.radians( self.angle ) )
        self.x -= self.speed * math.sin( math.radians( self.angle ) )
        self.car.setPos(self.x, self.y)"""

    def steerRight(self):
        self.angle += self.speed * 0.8
        self.car.setRotation(self.angle)
    
    def steerLeft(self):
        self.angle -= self.speed * 0.8
        self.car.setRotation(self.angle)

    def accelerate(self):
        self.speed += self.ACCEL
        self.speed = np.clip(self.speed, 0, self.MAX_SPEED)

    def decelerate(self):
        self.speed -= self.ACCEL
        self.speed = np.clip(self.speed, -self.MAX_SPEED/2, self.MAX_SPEED)

    def update(self):
        self.speed *= self.FRICTION

        if self.speed < 0.1 and self.speed > -0.1:
            self.speed = 0

        self.moveForward()

class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        self.timerId = 0

        scene = QGraphicsScene(self)

        self.pixmap = QPixmap ("../resources/maps/level1/background.png")
        _ = scene.addPixmap(self.pixmap)
        self.resize(self.pixmap.size().width(), self.pixmap.size().height() )

        # create car
        self.car = Car(scene, 110, 400, 0)

        self.setScene( scene )
        self.setCacheMode( QGraphicsView.CacheBackground )
        self.setViewportUpdateMode( QGraphicsView.BoundingRectViewportUpdate )
        self.setRenderHint( QPainter.Antialiasing )
        self.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor( QGraphicsView.AnchorViewCenter )

        # keyboard status
        self.keyUp = False
        self.keyDown = False
        self.keyRight = False
        self.keyLeft = False

        # create timer
        self.startTimer(1000 / 60)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.keyUp = True
        if key == Qt.Key_Down:
            self.keyDown = True
        if key == Qt.Key_Right:
            self.keyRight = True
        if key == Qt.Key_Left:
            self.keyLeft = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.keyUp = False
        if key == Qt.Key_Down:
            self.keyDown = False
        if key == Qt.Key_Right:
            self.keyRight = False
        if key == Qt.Key_Left:
            self.keyLeft = False

    def timerEvent(self, event):
        if self.keyUp:
            self.car.accelerate()
        if self.keyDown:
            self.car.decelerate()
        if self.keyRight:
            self.car.steerRight()
        if self.keyLeft:
            self.car.steerLeft()

        self.car.update()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    widget = GraphWidget()
    widget.show()

    sys.exit(app.exec_())
import math
import random

from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color

from kivy.metrics import dp

class Particle:
    xMultiplier = 0

    def __init__(self, x, y, colorG, yMaxOffset, holderWidth):
        self.x = x
        self.y = y
        self.startPos = (x,y)
        self.colorG = colorG

        self.speed = random.random() * 40 + 80
        self.size = 10

        self.offsetX = random.random() * 10
        self.offsetY = random.random() * yMaxOffset

        self.y += self.offsetY

        self.rect = None

        self.xMultiplier = holderWidth

    def draw(self, canvas):
        with canvas:
            if self.rect is None:
                Color(rgba=(self.colorG,self.colorG,self.colorG,self.colorG))
                self.rect = Rectangle(pos=(self.x * self.xMultiplier, self.y), size=(dp(self.size), dp(self.size)))
            else:
                self.rect.pos = (self.x * self.xMultiplier, self.y)

    def update(self, canvas, dt, maxHeight):
        self.y += self.speed * dt
        self.x = self.startPos[0] + math.sin(self.y/10 + self.offsetX) / 100

        if self.y > maxHeight: # respawning the particle when goes out of the screen
            self.x = self.startPos[0]
            self.y = self.startPos[1] - self.size
            # this section is used to make sure the particle spawns below the screen

        self.draw(canvas)
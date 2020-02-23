import pygame
import sys
import config as con

from pygame import Rect
from collections import defaultdict


class GameObject:
    def __init__(self, x, y, w, h, speed=(0,0)):
        self.bounds = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)

    def update(self):
        """"""
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)


class Circle(GameObject):
    def __init__(self, x, y, color, speed_x, speed_y):
        GameObject.__init__(self, x - con.RADIUS, y - con.RADIUS, con.RADIUS * 2, con.RADIUS * 2)
        self.color = color
        self.speed = [speed_x, speed_y]
        self.space = False
        self.counter = 0
        self.down = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, con.RADIUS)

    def update(self):
        self.move(self.speed[0], self.speed[1])

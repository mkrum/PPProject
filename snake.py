import pygame
from math import sin, cos, radians


class Snake(pygame.sprite.Sprite):

    def __init__(self, gs, x, y, size):
        self.x = x
        self.y = y

        self.score = 0

        self.delay = 0
        self.pause = 3

        self.speed = 1
        self.x_modifier = self.speed
        self.y_modifier = 0
   
    def tick(self, gs):
        #update position
        if (self.delay == 0):
            self.x += self.y_modifier 
            self.y += self.x_modifier

        self.delay = (self.delay + 1) % self.pause

    def move_up(self):
        self.y_modifier = -1 * self.speed
        self.x_modifier = 0

    def move_down(self):
        self.y_modifier = self.speed
        self.x_modifier = 0

    def move_right(self):
        self.x_modifier = self.speed
        self.y_modifier = 0

    def move_left(self):
        self.x_modifier = -1 * self.speed
        self.y_modifier = 0


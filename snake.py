import pygame
from math import sin, cos, radians


class Snake(pygame.sprite.Sprite):

    def __init__(self, gs, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.score = 0

        self.speed = size
        self.x_modifier = self.speed
        self.y_modifier = 0

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
   

    def tick(self, gs):
        #update position
        self.x += self.x_modifier 
        self.y += self.y_modifier
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

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


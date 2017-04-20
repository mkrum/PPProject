import pygame
from math import sin, cos, radians


class Grid(pygame.sprite.Sprite):

    def __init__(self, gs, N_wide, N_height):
        self.box_width = gs.width / N_wide
        self.box_height = gs.height / N_height
        
        self.boxes = [ [] for _ in xrange(N_height) ]
        
        for i in range(N_height):
            y = i * self.box_height
            for j in range(N_wide):
                x = j * self.box_width
                self.boxes[i].append(pygame.Rect(x, y, self.box_width, self.box_height))

   


        
        

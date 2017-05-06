import pygame
from math import sin, cos, radians


class Snake(pygame.sprite.Sprite):

    def __init__(self, gs, x, y, size):
        self.x = x
        self.y = y

        self.gs = gs

        self.score = 0

        self.delay = 0
        self.pause = 3

        self.speed = 1
        self.x_modifier = self.speed
        self.y_modifier = 0
        self.sync = False
   
    def tick(self, gs):
        #update position
        if (self.delay == 0):
            self.x += self.y_modifier 
            self.y += self.x_modifier
            if self.sync:
                self.send_location(self.x, self.y)

        self.delay = (self.delay + 1) % self.pause

    def move_up(self):
        #self.send_move('up')
        self.up()

    def up(self):
        self.y_modifier = -1 * self.speed
        self.x_modifier = 0

    def move_down(self):
        #self.send_move('down')
        self.down()

    def down(self):
        self.y_modifier = self.speed
        self.x_modifier = 0

    def move_right(self):
        #self.send_move('right')
        self.right()

    def right(self):
        self.x_modifier = self.speed
        self.y_modifier = 0

    def move_left(self):
        #self.send_move('left')
        self.left()

    def left(self):
        self.x_modifier = -1 * self.speed
        self.y_modifier = 0

    def send_move(self, move):
        self.gs.connection.update(move)

    def receive_move(self, move):
        if move == 'up':
            self.up()
        elif move == 'down':
            self.down()
        elif move == 'left':
            self.left()
        elif move == 'right':
            self.right()

    def send_location(self, i, j):
        self.gs.connection.update("%s %s" % (str(i), str(j)))
        
    def receive_location(self, loc):
        print("~"+loc+"~")
        self.y = int(spl[1])

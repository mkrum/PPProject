import pygame
from math import sin, cos, radians
from gamegrid import Box

class Snake(pygame.sprite.Sprite):

    def __init__(self, gs, x, y, size):
        self.x = x
        self.y = y
        self.path = []
            
        self.gs = gs

        self.score = 0

        self.delay = 0
        self.pause = 3

        self.speed = 1
        self.x_modifier = self.speed
        self.y_modifier = 0
        self.sync = False
        self.message = ''
   
    def tick(self, gs):
        #update position
        if (self.message != ''):
            self.parse_message(self.message) 
            self.message = ''
        else:
            if (self.delay == 0):
                self.x += self.y_modifier 
                self.y += self.x_modifier

            self.delay = (self.delay + 1) % self.pause

    def move_up(self):
        self.send_move_location('up', self.x, self.y)
        self.up()

    def up(self):
        self.y_modifier = -1 * self.speed
        self.x_modifier = 0

    def move_down(self):
        self.send_move_location('down', self.x, self.y)
        self.down()

    def down(self):
        self.y_modifier = self.speed
        self.x_modifier = 0

    def move_right(self):
        self.send_move_location('right', self.x, self.y)
        self.right()

    def right(self):
        self.x_modifier = self.speed
        self.y_modifier = 0

    def move_left(self):
        self.send_move_location('left', self.x, self.y)
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
        self.gs.connection.transport.setTcpNoDelay(True)
        self.gs.connection.update("%s %s" % (str(i), str(j)))
        
    def receive_location(self, loc):
        spl = loc.split(" ")
        self.y = int(spl[1])
        self.x = int(spl[0])

    def send_move_location(self, move, i, j):
        self.gs.connection.update(move + " %s %s," % (str(i), str(j)))

    def receive_move_location(self, message, data):
        self.message = message
        self.data = data

    def parse_message(self, message):
        message = message.split(',')[-1]
        spl = message.split(" ")

        turn_point = (int(spl[1]), int(spl[2]))
        adjust = 0
                
        for i in self.path[::-1]:
            if i[0] != turn_point[0] and i[1] != turn_point[1]:
                self.path.remove(i)
                adjust += 1
                self.data[i[0]][i[1]] = Box.EMPTY
            else:
                break
        self.x = turn_point[0]
        self.y = turn_point[1]
                
        move = spl[0]
        for _ in range(adjust):
            if move == 'up':
                self.y -= 1
            elif move == 'down':
                self.y += 1
            elif move == 'left':
                self.x += 1
            elif move == 'right':
                self.x -= 1
    
            self.data[self.x][self.y] = Box.ENEMY_PATH

        if move == 'up':
            self.up()
        elif move == 'down':
            self.down()
        elif move == 'left':
            self.left()
        elif move == 'right':
            self.right()
        

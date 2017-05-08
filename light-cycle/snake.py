import pygame
from math import sin, cos, radians
from gamegrid import Box

class Snake(pygame.sprite.Sprite):

    def __init__(self, gs, x, y, size, num):
        self.num = num
        # the location and path of the snake
        self.x = x
        self.y = y
        self.path = []
            
        self.gs = gs
        
        # control how quickly snake moves
        self.delay = 0
        self.pause = 2
        self.speed = 1
        self.x_modifier = self.speed
        self.y_modifier = 0

        self.sync = False
        self.message = ''
   
    def tick(self, gs):
        #update position
        if (self.delay == 0):
            self.x += self.y_modifier 
            self.y += self.x_modifier

        self.delay = (self.delay + 1) % self.pause

    # helper functions to handle moving the snake and
    # updating its location in the other client

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
    
    # send this player's move and position to the other client
    def send_move_location(self, move, i, j):
        self.gs.connection.update('{} {} {},'.format(move, str(i), str(j)))

    # receive the opponent's move and position
    def receive_move_location(self, message, data):
        self.message = message
        self.data = data
        self.parse_message(message)

    # update the opponent's position and path
    def parse_message(self, message):
        message = message.split(',')[-2]
        spl = message.split(" ")

        turn_point = (int(spl[1]), int(spl[2]))
        adjust = 0
        self.data[turn_point[0]][turn_point[1]] = Box.EMPTY

        to_remove = []                
        adj_path = []
        delete = False

        for i in self.path:
            if delete:
                self.data[i[0]][i[1]] = Box.EMPTY
                continue
            
            if not (i[0] == turn_point[0] and i[1] == turn_point[1]):
                adj_path.append(i)
            else:
                adj_path.append(i)
                delete = True

        self.path = adj_path
        self.x = turn_point[0]
        self.y = turn_point[1]

        self.data[self.x][self.y] = Box.ENEMY_PATH
                
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

            self.path.append((self.x, self.y))
            self.data[self.x][self.y] = Box.ENEMY_PATH

        if move == 'up':
            self.up()
        elif move == 'down':
            self.down()
        elif move == 'left':
            self.left()
        elif move == 'right':
            self.right()
        

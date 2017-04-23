import pygame
from math import sin, cos, radians

class Box():
    EMPTY = 0
    MARKED = 1
    PATH = 2

class Grid(pygame.sprite.Sprite):

    def __init__(self, gs, N_wide, N_height):
        self.width = N_wide
        self.height = N_height
        self.box_width = gs.width / N_wide
        self.box_height = gs.height / N_height
        
        self.boxes = [ [] for _ in xrange(N_height) ]
        self.data = [ [] for _ in xrange(N_height) ]

        self.snake_path = []
        
        for i in range(self.height):
            y = i * self.box_height
            for j in range(self.width):
                x = j * self.box_width
                self.boxes[i].append(pygame.Rect(x, y, self.box_width, self.box_height))

                #placeholder
                self.data[i].append(Box.EMPTY)
                if(i + j < 3):
                    self.data[i][j] = Box.MARKED

   

    def tick(self, gs):
        #mark the spot of the current snake
        for i in range(self.height):
            for j in range(self.width):
                if (self.boxes[i][j].colliderect(gs.player.rect)):
                    if(self.data[i][j] == Box.MARKED):
                        self.snake_path.append([i, j])
                        if (len(self.snake_path) > 1):
                            self.fill_path()
                        self.snake_path = []
                    else:
                        self.data[i][j] = Box.PATH
                        self.snake_path.append([i, j])
                    break



    #there must be a better way to do this
    def fill_path(self):
        
        if (len(self.snake_path) < 2):
            return 

        #complete right angle
        end = list(self.snake_path[-1])
        dx = self.snake_path[0][0] - self.snake_path[1][0]
        dy = self.snake_path[0][1] - self.snake_path[1][1]

        move = list(self.snake_path[0])
        move[0] += dx
        move[1] += dy
        print(move)
        print(end) 
        new_point = list(move)
        self.snake_path.append(new_point)
        print(self.snake_path)

        while (move[0] != end[0]):
            if (end[0] > move[0]):
                move[0] += 1
            else:
                move[0] -= 1

            if (self.data[move[0]][move[1]] == Box.MARKED):
                new_point = list(move)
                self.snake_path.append(new_point)
            else:
                break

        while (move[1] != end[1]):
            if (end[1] > move[1]):
                move[1] += 1
            else:
                move[1] -= 1

            if (self.data[move[0]][move[1]] == Box.MARKED):
                new_point = list(move)
                self.snake_path.append(new_point)
            else:
                break

        move = list(self.snake_path[0])
        move[0] += dx
        move[1] += dy

        while (move[1] != end[1]):
            if (end[1] > move[1]):
                move[1] += 1
            else:
                move[1] -= 1

            if (self.data[move[0]][move[1]] == Box.MARKED):
                new_point = list(move)
                self.snake_path.append(new_point)
            else:
                break

        while (move[0] != end[0]):
            if (end[0] > move[0]):
                move[0] += 1
            else:
                move[0] -= 1

            if (self.data[move[0]][move[1]] == Box.MARKED):
                new_point = list(move)
                self.snake_path.append(new_point)
            else:
                break


        print(self.snake_path)
        self.i_ranges = {}
        self.j_ranges = {}

        for (i, j) in self.snake_path:
            self.data[i][j] = Box.MARKED
            try:
                self.i_ranges[i].append(j)
                self.j_ranges[j].append(i)
            except:
                self.i_ranges[i] = [j]
                self.j_ranges[j] = [i]



        for k in self.i_ranges.keys():
            l = self.i_ranges[k]
            
            new_list = []
            for i in range(len(l)):
                #get points right next to each other
                if l < len(l) - 1 and abs(l[i] - l[i + 1]) == 1:
                    continue
                if l > 0 and abs(l[i] - l[i - 1]) == 1:
                    continue

                new_list.append(l[i])

            self.i_ranges[k] = sorted(new_list)
        
        for k in self.j_ranges.keys():
            l = self.j_ranges[k]
            new_list = []
            for i in range(len(l)):
                #get points right next to each other
                if l < len(l) - 1 and abs(l[i] - l[i + 1]) == 1:
                    continue
                if l > 0 and abs(l[i] - l[i - 1]) == 1:
                    continue

                new_list.append(l[i])

            self.j_ranges[k] = sorted(new_list)
        
        
        for i in self.i_ranges.keys():
            for j in self.j_ranges.keys():
                
                for k in range(len(self.i_ranges[i]) - 1):
                    if (j >= self.i_ranges[i][k] and j <= self.i_ranges[i][ k + 1 ]):
                        self.data[i][j] = Box.MARKED

                for k in range(len(self.j_ranges[j]) - 1):
                    if (i >= self.j_ranges[j][k] and i <= self.j_ranges[j][ k + 1 ]):
                        self.data[i][j] = Box.MARKED


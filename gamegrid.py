import pygame
from math import sin, cos, radians
from Queue import Queue

class Box():
    EMPTY = 0
    MARKED = 1
    PATH = 2

class Grid(pygame.sprite.Sprite):

    def __init__(self, gs, N_wide, N_height):
        self.width = N_wide
        self.height = N_height
        self.box_width = gs.box_size
        self.box_height = gs.box_size
        
        self.data = [ [] for _ in xrange(N_height) ]

        self.snake_path = []
        
        for i in range(self.height):
            for j in range(self.width):
                #placeholder
                self.data[i].append(Box.EMPTY)
                if(i + j < 3):
                    self.data[i][j] = Box.MARKED

   

    def tick(self, gs):
        #mark the spot of the current snake
        i = gs.player.x
        j = gs.player.y

        if(self.data[i][j] == Box.MARKED):
            self.snake_path.append([i, j])
            if (len(self.snake_path) > 1):
                self.fill_path()
            self.snake_path = []
        else:
            self.data[i][j] = Box.PATH
            gs.connection.update(i, j, Box.PATH)
            self.snake_path.append([i, j])



    #there must be a better way to do this
    def fill_path(self):
        
        if (len(self.snake_path) < 2):
            return 

        #complete right angle
        end = list(self.snake_path[-1])

        #Check if the beginning and end is parallel
        dx = self.snake_path[0][0] - self.snake_path[1][0]
        dy = self.snake_path[0][1] - self.snake_path[1][1]
        
        move = list(self.snake_path[0])
        
        move[0] += dx
        move[1] += dy
        new_point = list(move)
        self.snake_path.append(new_point)
        add_points = self.find_path(new_point, end)
        
        for p in add_points:
            self.snake_path.append(p)

        self.i_ranges = {}
        self.j_ranges = {}

        for (i, j) in self.snake_path:
            self.data[i][j] = Box.MARKED
            gs.connection.update(i, j, Box.MARKED)

            try:
                self.i_ranges[i].append(j)
                self.j_ranges[j].append(i)
            except:
                self.i_ranges[i] = [j]
                self.j_ranges[j] = [i]



        for k in self.i_ranges.keys():
            l = sorted(self.i_ranges[k])
            
            new_list = []
            for i in range(len(l)):
                #get points right next to each other
                if i < len(l) - 1 and abs(l[i] - l[i + 1]) == 1:
                    continue
                if i > 0 and abs(l[i] - l[i - 1]) == 1:
                    continue

                new_list.append(l[i])

            self.i_ranges[k] = sorted(new_list)
        
        for k in self.j_ranges.keys():
            l = sorted(self.j_ranges[k])
            new_list = []
            for i in range(len(l)):
                #get points right next to each other
                if i < len(l) - 1 and abs(l[i] - l[i + 1]) == 1:
                    continue
                if i > 0 and abs(l[i] - l[i - 1]) == 1:
                    continue

                new_list.append(l[i])

            self.j_ranges[k] = sorted(new_list)
        
        for i in self.i_ranges.keys():
            for j in self.j_ranges.keys():

                for k in range(len(self.i_ranges[i]) - 1):
                    if (j > self.i_ranges[i][k] and j < self.i_ranges[i][ k + 1 ]):
                        if (self.data[i][j] == Box.EMPTY):
                            self.fill_shape((i, j), self.snake_path) 
                            return

                for k in range(len(self.j_ranges[j]) - 1):
                    if (i > self.j_ranges[j][k] and i < self.j_ranges[j][ k + 1 ]):
                        if (self.data[i][j] == Box.EMPTY):
                            self.fill_shape((i, j), self.snake_path) 
                            return

    def get_valid_edges(self, p1, visited, box_type):
        edges = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    p = list(p1)
                    p[0] += i
                    p[1] += j
                    try:
                        if (self.data[p[0]][p[1]] == box_type):
                            if ((p[0], p[1]) not in visited):
                                edges.append(p)
                                visited.add((p[0], p[1]))
                    except:
                        pass

        return edges

    #modified Dijkstra
    def find_path(self, start, end):

        dist = dict()
        previous = dict()
        visited = set()

        for i in range(self.width):
            for j in range(self.height):
                dist[(i, j)] = float("inf")
                previous[(i, j)] = None

        dist[(start[0], start[1])] = 0
        q = Queue()

        q.put(start)
        visited.add((start[0], start[1]))

        while not q.empty():
            current = q.get()

            if current[0] == end[0] and current[1] == end[1]:
                return self.build_path(previous, end)

            for edge in self.get_valid_edges(current, visited, Box.MARKED):
                newDist = dist[(current[0], current[1])] + 1

                try:
                    if newDist < dist[(edge[0], edge[1])]:
                        dist[(edge[0], edge[1])] = newDist
                        previous[(edge[0], edge[1])] = current

                    q.put(edge)
                except:
                    pass


    def build_path(self, previous, end):
        points = []
        current = previous[(end[0], end[1])]

        while current != None:
            points.append(current)
            current = previous[(current[0], current[1])]

        return points

    def fill_shape(self, point, path):
        q = Queue()
        visited = set()
        q.put(point)
        
        while not q.empty():
            current = q.get()
            self.data[current[0]][current[1]] = Box.MARKED
            gs.connection.update(current[0], current[1], Box.MARKED)
            
            for adj in self.get_valid_edges(current, visited, Box.EMPTY):
                q.put(adj)

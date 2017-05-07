import pygame
from math import sin, cos, radians
from Queue import Queue

# enum for different options for Box type
class Box():
    EMPTY = 0
    MARKED = 1
    PATH = 2
    ENEMY_PATH = 3
    ENEMY = 4
    ENEMY_MARKED = 5

class Grid(pygame.sprite.Sprite):

    def __init__(self, gs, N_wide, N_height):
        self.width = N_wide
        self.height = N_height
        self.box_width = gs.box_size
        self.box_height = gs.box_size
        
        self.data = [ [] for _ in xrange(N_height) ]

        
        for i in range(self.height):
            for j in range(self.width):
                #placeholder
                self.data[i].append(Box.EMPTY)
                if(i + j < 3):
                    self.data[i][j] = Box.MARKED

        self.old_i = {}
        self.old_j = {}
   

    def tick(self, gs, snake, path_value, marked_value, enemy_path_value):
        #mark the spot of the current snake

        i = snake.x
        j = snake.y

        try:
            if i == self.old_i[snake] and j == self.old_j[snake]:
                return
        except:
            self.old_i[snake] = i
            self.old_j[snake] = j

        if(self.data[i][j] == marked_value):
            snake.path.append([i, j])
            if (len(snake.path) > 1):
                self.fill_path(gs, snake.path, marked_value)
            snake.path = []

        #check if you hit your own path
        elif (self.data[i][j] == path_value):
            # gs.game_over_screen('lose')
            pass
        elif (self.data[i][j] == enemy_path_value):
            gs.game_over_screen('win', 'lose')
        #check bounds
        elif (i < 0 or j < 0 or i > gs.grid_size or j > gs.grid_size):
            gs.game_over_screen('lose', 'win')
        else:
            self.data[i][j] = path_value
            # gs.connection.update(i, j, Box.PATH)
            snake.path.append([i, j])

        self.old_i[snake] = i
        self.old_j[snake] = j
        
    # when a snake makes it back to its own squares,
    # fill the area formed by the path
    # there must be a better way to do this
    def fill_path(self, gs, snake_path, marked_value):
        
        if (len(snake_path) < 2):
            return 

        #complete right angle
        end = list(snake_path[-1])

        #Check if the beginning and end is parallel
        dx = snake_path[0][0] - snake_path[1][0]
        dy = snake_path[0][1] - snake_path[1][1]
        
        move = list(snake_path[0])
        
        move[0] += dx
        move[1] += dy
        new_point = list(move)
        snake_path.append(new_point)
        add_points = self.find_path(new_point, end, marked_value)
        
        if not add_points:
            return

        for p in add_points:
            snake_path.append(p)
        i_ranges = {}
        j_ranges = {}

        for (i, j) in snake_path:

            #check if its a new block, if so, increment score
            if (self.data[i][j] != Box.MARKED):
                gs.player.score += 1

            self.data[i][j] = marked_value
            # gs.connection.update(i, j, Box.MARKED)

            try:
                i_ranges[i].append(j)
                j_ranges[j].append(i)
            except:
                i_ranges[i] = [j]
                j_ranges[j] = [i]

        for k in i_ranges.keys():
            l = sorted(i_ranges[k])
            
            new_list = []
            for i in range(len(l)):
                # get points right next to each other
                if i < len(l) - 1 and abs(l[i] - l[i + 1]) == 1:
                    continue
                if i > 0 and abs(l[i] - l[i - 1]) == 1:
                    continue

                new_list.append(l[i])

            i_ranges[k] = sorted(new_list)
        
        for k in j_ranges.keys():
            l = sorted(j_ranges[k])
            new_list = []
            for i in range(len(l)):
                # get points right next to each other
                if i < len(l) - 1 and abs(l[i] - l[i + 1]) == 1:
                    continue
                if i > 0 and abs(l[i] - l[i - 1]) == 1:
                    continue

                new_list.append(l[i])

            j_ranges[k] = sorted(new_list)
        
        for i in i_ranges.keys():
            for j in j_ranges.keys():

                for k in range(len(i_ranges[i]) - 1):
                    if (j > i_ranges[i][k] and j < i_ranges[i][ k + 1 ]):
                        if (self.data[i][j] == Box.EMPTY):
                            self.fill_shape((i, j), snake_path, gs, marked_value) 
                            return

                for k in range(len(j_ranges[j]) - 1):
                    if (i > j_ranges[j][k] and i < j_ranges[j][ k + 1 ]):
                        if (self.data[i][j] == Box.EMPTY):
                            self.fill_shape((i, j), snake_path, gs, marked_value) 
                            return

    def get_valid_edges(self, p1, visited, not_box_types):
        edges = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    p = list(p1)
                    p[0] += i
                    p[1] += j
                    try:
                        if (self.data[p[0]][p[1]] not in not_box_types):
                            if ((p[0], p[1]) not in visited):
                                edges.append(p)
                                visited.add((p[0], p[1]))
                    except:
                        pass

        return edges

    # modified Dijkstra
    def find_path(self, start, end, marked_value):

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

            for edge in self.get_valid_edges(current, visited, [Box.EMPTY, Box.PATH, Box.ENEMY_PATH]):
                newDist = dist[(current[0], current[1])] + 1

                try:
                    if newDist < dist[(edge[0], edge[1])]:
                        dist[(edge[0], edge[1])] = newDist
                        previous[(edge[0], edge[1])] = current

                    q.put(edge)
                except:
                    pass

        return None

    def build_path(self, previous, end):
        points = []
        current = previous[(end[0], end[1])]

        while current != None:
            points.append(current)
            current = previous[(current[0], current[1])]

        return points

    def fill_shape(self, point, path, gs, marked_value):
        q = Queue()
        visited = set()
        q.put(point)
        
        while not q.empty():
            current = q.get()

            if (self.data[current[0]][current[1]] != marked_value):
                gs.player.score += 1

            self.data[current[0]][current[1]] = marked_value 
            
            for adj in self.get_valid_edges(current, visited, [Box.MARKED]):
                q.put(adj)

    def update(self, i, j, value):
        self.data[i][j] = value



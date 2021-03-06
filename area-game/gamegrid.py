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
        self.gs = gs
        
        self.data = [ [] for _ in xrange(N_height) ]

        
        for i in range(self.height):
            for j in range(self.width):
                self.data[i].append(Box.EMPTY)

        self.old_i = {}
        self.old_j = {}

        self.buffer_path = []
   

    def tick(self, gs, snake, path_value, marked_value, enemy_path_value, enemy_marked):
        #mark the spot of the current snake

        i = snake.x
        j = snake.y

        try:
            if i == self.old_i[snake] and j == self.old_j[snake]:
                return
        except:
            self.old_i[snake] = i
            self.old_j[snake] = j

        # bug: opponent goes out of bounds of list
        try:
            x = self.data[i][j]
        except:
            print('i: {} j: {} snake: {}'.format(i, j, snake.num))
            return

        if self.data[i][j] == marked_value:
            snake.path.append([i, j])
            if (len(snake.path) > 1):
                self.fill_path(gs, snake.path, marked_value, enemy_marked, snake)
            snake.path = []
        # check if you hit your own path.
        # only check win conditions for player, not for opponent
        elif (self.data[i][j] == path_value) and snake.num == 0:
            gs.connection.update('win')
            gs.game_over_screen('lose')
            print('you lost by hitting your own path')
        elif (self.data[i][j] == enemy_path_value) and snake.num == 0:
            gs.connection.update('lose')
            gs.game_over_screen('win')
            print('you won by hitting enemy path')
        # check bounds - give a slight buffer
        elif (i <= 2 or j <= 2 or i >= gs.grid_size-2 or j >= gs.grid_size-2) and snake.num == 0:
            gs.connection.update('win')
            gs.game_over_screen('lose')
            print('you lost by going out of bounds')
        else:
            self.data[i][j] = path_value
            # gs.connection.update(i, j, Box.PATH)
            snake.path.append([i, j])

        self.old_i[snake] = i
        self.old_j[snake] = j
        
    # when a snake makes it back to its own squares,
    # fill the area formed by the path
    # there must be a better way to do this
    def fill_path(self, gs, snake_path, marked_value, enemy_marked, snake):
        
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
        add_points = self.find_path(new_point, end, marked_value, enemy_marked)
        
        if not add_points:
            return
        for p in add_points:
            snake_path.append(p)
        
        #the total shape is too small, dont try to fill it
        print('~')
        print(snake_path)



        #if its player one, signal the draw
        if marked_value == Box.MARKED:
            self.draw_path(snake_path, marked_value, enemy_marked, snake)
            message = 'draw'
            for z in snake_path:
                message += ' %s %s' % (str(z[0]), str(z[1]))
            message += ','
            gs.connection.update(message)
        else:
            self.buffer_path = snake_path
            self.b_marked_value = marked_value
            self.b_enemy_marked = enemy_marked
            self.b_snake = snake

    def get_valid_edges(self, p1, visited, box_type):
        edges = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    p = list(p1)
                    p[0] += i
                    p[1] += j
                    try:
                        if (self.data[p[0]][p[1]] in box_type):
                            if ((p[0], p[1]) not in visited):
                                edges.append(p)
                                visited.add((p[0], p[1]))
                    except:
                        pass

        return edges


    # modified Dijkstra
    def find_path(self, start, end, marked_value, enemy_marked):

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

            for edge in self.get_valid_edges(current, visited, [marked_value]):
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

    def fill_shape(self, point, path, gs, marked_value, enemy_marked, snake):
        q = Queue()
        visited = set()
        q.put(point)
        
        while not q.empty():
            current = q.get()

            if (self.data[current[0]][current[1]] != marked_value):
                snake.score += 1
                if self.data[current[0]][current[1]] == enemy_marked:
                    # deduct the other snake's score
                    if snake.num == gs.player.num:
                        opp = gs.opponent
                    else:
                        opp = gs.player
                    opp.score -= 1

            self.data[current[0]][current[1]] = marked_value 
            
            for adj in self.get_valid_edges(current, visited, [Box.EMPTY, enemy_marked]):
                q.put(adj)

    def update(self, i, j, value):
        self.data[i][j] = value

    def draw_buffer_path(self):
        self.draw_path(self.buffer_path, self.b_marked_value, self.b_enemy_marked, self.b_snake)

    def draw_path(self, path, marked_value, enemy_marked, snake):

        if not path:
            return 

        if len(path) < 2:
            return 

        i_ranges = {}
        j_ranges = {}

        for (i, j) in path:

            #check if its a new block, if so, increment score
            if (self.data[i][j] != marked_value):
                snake.score += 1
                if self.data[i][j] == enemy_marked:
                    # deduct the other snake's score
                    if snake.num == self.gs.player.num:
                        opp = gs.opponent
                    else:
                        opp = gs.player
                    opp.score -= 1

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
                            self.fill_shape((i, j), self.buffer_path, self.gs,
                                    marked_value, enemy_marked, snake) 
                            return

                for k in range(len(j_ranges[j]) - 1):
                    if (i > j_ranges[j][k] and i < j_ranges[j][ k + 1 ]):
                        if (self.data[i][j] == Box.EMPTY):
                            self.fill_shape((i, j), self.buffer_path, self.gs,
                                    marked_value, enemy_marked, snake) 
                            return

import pygame
from math import sin, cos, radians

# enum for different options for Box type
class Box():
    EMPTY = 0
    MARKED = 1
    PATH = 2
    ENEMY_PATH = 3
    ENEMY = 4
    ENEMY_MARKED = 5
    BORDER = 6

class Grid(pygame.sprite.Sprite):

    def __init__(self, gs, N_wide, N_height):
        self.width = N_wide
        self.height = N_height
        self.box_width = gs.box_size
        self.box_height = gs.box_size
        
        self.data = [ [] for _ in range(N_height) ]

        
        for i in range(self.height):
            for j in range(self.width):
                # to start, just add the border around the boundary and empty squares
                if (i < 3 or i >= self.height - 3) or (j < 3 or j >= self.height - 3):
                    self.data[i].append(Box.BORDER)
                else:
                    self.data[i].append(Box.EMPTY)

        self.old_i = {}
        self.old_j = {}
   

    def tick(self, gs, snake, path_value, enemy_path_value):
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
        
        # only check win conditions for player, not for opponent

        # check if you hit your own path.
        if (self.data[i][j] == path_value) and snake.num == 0:
            # let the other client know they won
            gs.connection.update('win')
            # go to the ending screen
            gs.game_over_screen('lose')
            print('you lost by hitting your own path')
        elif (self.data[i][j] == enemy_path_value) and snake.num == 0:
            gs.connection.update('win')
            gs.game_over_screen('lose')
            print('you lost by hitting the enemy path')
        # check bounds - give a slight buffer
        elif (i <= 3 or j <= 3 or i >= gs.grid_size-3 or j >= gs.grid_size-3) and snake.num == 0:
            gs.connection.update('win')
            gs.game_over_screen('lose')
            print('you lost by going out of bounds')
        else:
            # player did not lose, keep going
            self.data[i][j] = path_value
            snake.path.append([i, j])

        self.old_i[snake] = i
        self.old_j[snake] = j

import pygame
import sys
from threading import Thread
from snake import Snake
from gamegrid import Grid, Box
from twisted.internet import reactor

class GameSpace:

    def main(self):
        # part one
        self.started = False
        self.finished = False
        
        pygame.init()
        self.size = self.width, self.height = 600, 600 

        self.grid_size = 600

        self.black = 0, 0, 0 #RGB
        self.screen = pygame.display.set_mode(self.size)

        self.boxes_per_row = 60

        self.boxes = [ [] for _ in range(self.boxes_per_row) ]

        self.box_size = 10
        self.x_offset = 0
        self.y_offset = 0
        
        for i in range(self.boxes_per_row):
            y = i * self.box_size
            for j in range(self.boxes_per_row):
                x = j * self.box_size
                self.boxes[i].append(pygame.Rect(x, y, self.box_size, self.box_size))


        self.mono = pygame.font.SysFont("monospace", 15)     

        # part two

        self.grid = Grid(self, self.grid_size, self.grid_size)
        self.clock = pygame.time.Clock()

        # draw initial screen
        self.screen.fill(self.black)
        # from the pygame Chimp example:
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render('Waiting for second player.', 1, (255, 255, 255))
            textpos = text.get_rect(centerx=int(self.width/2),
                    centery=int(self.height/2))
            self.screen.blit(text, textpos)
            pygame.display.flip()

    def set_players(self, num):
        if (int(num)):
            self.player = Snake(self, 0, 0, self.box_size)
            self.opponent = Snake(self, 10, 10, self.box_size)
        else:
            self.player = Snake(self, 10, 10, self.box_size)
            self.opponent = Snake(self, 0, 0, self.box_size)

        self.player.sync = True

    def game_space_tick(self):
        # part three
        # self.clock.tick(60)

        if not self.started or self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    reactor.stop()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.finished:
                    reactor.stop()
            return

        self.player.tick(self)
        self.opponent.tick(self)

        self.grid.tick(self, self.player, Box.PATH, Box.MARKED, Box.ENEMY_PATH)
        self.grid.tick(self, self.opponent, Box.ENEMY_PATH, Box.ENEMY_MARKED, Box.PATH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(1)

            if event.type == pygame.KEYDOWN: 
                if event.key == ord("s"):
                    self.player.move_down()

                if event.key == ord("w"):
                    self.player.move_up()

                if event.key == ord("d"):
                    self.player.move_right()

                if event.key == ord("a"):
                    self.player.move_left()
        
        if self.finished:
            return

        self.screen.fill(self.black)

        self.update_offset()
        for i in range(self.boxes_per_row):
            for j in range(self.boxes_per_row):
                
                i_adj = i + self.x_offset
                j_adj = j + self.y_offset

                if (self.grid.data[i_adj][j_adj] == Box.MARKED):
                    pygame.draw.rect(self.screen, (255, 0, 0), self.boxes[i][j])
                elif (self.grid.data[i_adj][j_adj] == Box.PATH):
                    pygame.draw.rect(self.screen, ((255/2), 0, 0), self.boxes[i][j])
                elif (self.grid.data[i_adj][j_adj] == Box.EMPTY):
                    pygame.draw.rect(self.screen, (0, 0, 255), self.boxes[i][j])
                elif (self.grid.data[i_adj][j_adj] == Box.ENEMY):
                    pygame.draw.rect(self.screen, (0, 0, 255/3), self.boxes[i][j])

            pygame.draw.rect(self.screen, (0, 255, 0),
                    self.boxes[self.player.x - self.x_offset][self.player.y - self.y_offset])

            label = self.mono.render('Score: {}'
                    .format((str(self.player.score))), 1, (255,255,0))

            self.screen.blit(label, (10, 10))
        pygame.display.flip()
        
    def update_offset(self):
        x = self.player.x
        y = self.player.y

        if (x < self.boxes_per_row/2):
            self.x_offset = 0
        elif (x > self.grid_size - self.boxes_per_row):
            self.x_offset = self.grid_size - self.boxes_per_row
        else:
            self.x_offset = x - self.boxes_per_row/2

        if (y < self.boxes_per_row/2):
            self.y_offset = 0
        elif (y > self.grid_size - self.boxes_per_row):
            self.y_offset = self.grid_size - self.boxes_per_row
        else:
            self.y_offset = y - self.boxes_per_row/2

    def game_over_screen(self, result):
        self.connection.update(result)
        self.finished = True
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over - You {}!'.format(result), 1, (255, 10, 10))
        textpos = text.get_rect(centerx=int(self.width/2),
                                centery=int(self.height/2))
        self.screen.blit(text, textpos)
        pygame.display.flip()

    def win_screen(self):
        self.connection.update('lose')
        self.finished = True
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over - You Win!', 1, (255, 10, 10))
        textpos = text.get_rect(centerx=int(self.width/2),
                                centery=int(self.height/2))
        self.screen.blit(text, textpos)
        pygame.display.flip()

    def kill_other_snake(self):
        self.win_screen()

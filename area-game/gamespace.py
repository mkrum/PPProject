import pygame
import sys
from snake import Snake
from gamegrid import Grid, Box
from twisted.internet import reactor

class GameSpace:

    def main(self):
        # set up game space
    
        # the game has neither started nor finished
        self.started = False
        self.finished = False
        
        pygame.init()
        self.size = self.width, self.height = 600, 600 

        self.grid_size = 600

        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)

        self.boxes_per_row = 60

        self.boxes = [ [] for _ in range(self.boxes_per_row) ]

        self.box_size = 10
        self.x_offset = 0
        self.y_offset = 0

        self.winning_score = 1000
        
        for i in range(self.boxes_per_row):
            y = i * self.box_size
            for j in range(self.boxes_per_row):
                x = j * self.box_size
                self.boxes[i].append(pygame.Rect(x, y, self.box_size, self.box_size))

        # monospaced font
        self.mono = pygame.font.SysFont("monospace", 15)     

        # intialize the game grid of squares
        self.grid = Grid(self, self.grid_size, self.grid_size)

        # draw initial screen
        self.screen.fill(self.black)
        
        # put up screen waiting for other player
        # from the pygame Chimp example:
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render('Waiting for second player.', 1, (255, 255, 255))
            textpos = text.get_rect(centerx=int(self.width/2),
                    centery=int(self.height/2))
            self.screen.blit(text, textpos)
            pygame.display.flip()

    def set_players(self, num):
        # use num to distinguish between two client connections
        if int(num):
            # get the starting snakes
            self.player = Snake(self, 290, 290, self.box_size, 0)
            self.opponent = Snake(self, 310, 310, self.box_size, 1)
            
            # draw the starting squares for each player
            for i in range(10):
                for j in range(10):
                    self.grid.data[305 + i][305 + j] = Box.ENEMY_MARKED
                    self.grid.data[285 + i][285 + j] = Box.MARKED
        # do the opposite for the other player
        else:
            self.player = Snake(self, 310, 310, self.box_size, 0)
            self.opponent = Snake(self, 290, 290, self.box_size, 1)

            for i in range(10):
                for j in range(10):
                    self.grid.data[305 + i][305 + j] = Box.MARKED
                    self.grid.data[285 + i][285 + j] = Box.ENEMY_MARKED

    # reactor.LoopingCall calls this function 60 times per second
    def game_space_tick(self):
        # if the game has not started or finished, then allow the player
        # to exit, but nothing more
        if not self.started or self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if reactor.running:
                        reactor.stop()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.finished:
                    if reactor.running:
                        reactor.stop()
            return

        # call tick on each game object
        self.player.tick(self)
        self.opponent.tick(self)

        self.grid.tick(self, self.player, Box.PATH, Box.MARKED,
                Box.ENEMY_PATH, Box.ENEMY_MARKED)
        self.grid.tick(self, self.opponent, Box.ENEMY_PATH, Box.ENEMY_MARKED,
                Box.PATH, Box.MARKED)

        # if the game ended after tick, stop.
        if self.finished:
            return
        
        # handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if reactor.running:
                    reactor.stop()

            if event.type == pygame.KEYDOWN: 
                if event.key == ord("s"):
                    self.player.move_down()

                if event.key == ord("w"):
                    self.player.move_up()

                if event.key == ord("d"):
                    self.player.move_right()

                if event.key == ord("a"):
                    self.player.move_left()

        # update display
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

            label = self.mono.render('Your Score: {}, Opponent Score: {}'
                    .format(str(self.player.score), str(self.opponent.score)),
                    1, (255,255,255))

            self.screen.blit(label, (10, 10))
        pygame.display.flip()
    
    # scrolling view
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

    # update the other client that the game has ended
    def game_over_screen(self, result):
        self.text_screen('Game Over - You {}! Click to quit.'.format(result))

    # end of game screen: black background, white text in middle
    def text_screen(self, text):
        self.finished = True
        self.screen.fill(self.black)
        font = pygame.font.Font(None, 36)
        text = font.render(text, 1, (255, 255, 255))
        textpos = text.get_rect(centerx=int(self.width/2),
                                centery=int(self.height/2))
        self.screen.blit(text, textpos)
        pygame.display.flip()

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
        
        for i in range(self.boxes_per_row):
            y = i * self.box_size
            for j in range(self.boxes_per_row):
                x = j * self.box_size
                self.boxes[i].append(pygame.Rect(x, y, self.box_size, self.box_size))

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
            self.player = Snake(self, 305, 270, self.box_size, 0)
            self.opponent = Snake(self, 295, 330, self.box_size, 1)
            self.opponent.x_modifier *= -1
            
        # do the opposite for the other player
        else:
            self.player = Snake(self, 295, 330, self.box_size, 0)
            self.player.x_modifier *= -1
            self.opponent = Snake(self, 305, 270, self.box_size, 1)

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

        self.grid.tick(self, self.player, Box.PATH, Box.ENEMY_PATH)
        self.grid.tick(self, self.opponent, Box.ENEMY_PATH, Box.PATH)

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

                if (self.grid.data[i_adj][j_adj] == Box.PATH):
                    pygame.draw.rect(self.screen, ((255/2), 0, 0), self.boxes[i][j])
                elif (self.grid.data[i_adj][j_adj] == Box.EMPTY):
                    pygame.draw.rect(self.screen, (0, 0, 255), self.boxes[i][j])
                elif (self.grid.data[i_adj][j_adj] == Box.BORDER):
                    pygame.draw.rect(self.screen, (255, 255, 255), self.boxes[i][j])
                elif (self.grid.data[i_adj][j_adj] == Box.ENEMY_PATH):
                    pygame.draw.rect(self.screen, (255, 255, 0), self.boxes[i][j])


            pygame.draw.rect(self.screen, (0, 255, 0),
                    self.boxes[self.player.x - self.x_offset][self.player.y - self.y_offset])

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

import pygame
import sys
from snake import Snake
from gamegrid import Grid, Box
from connection import Connection

class GameSpace:

    def main(self):
        # part one
        pygame.init()
        self.size = self.width, self.height = 600, 600 

        self.grid_size = 600

        self.black = 0, 0, 0 #RGB
        self.screen = pygame.display.set_mode(self.size)

        self.screen_width = 60

        self.boxes = [ [] for _ in xrange(self.screen_width) ]

        self.box_size = 10
        self.x_offset = 0
        self.y_offset = 0
        
        for i in range(self.screen_width):
            y = i * self.box_size
            for j in range(self.screen_width):
                x = j * self.box_size
                self.boxes[i].append(pygame.Rect(x, y, self.box_size, self.box_size))

        # part two
        self.player = Snake(self, 0, 0, self.box_size)
        self.grid = Grid(self, self.grid_size, self.grid_size)
        self.connection = Connection(self.grid)
        self.clock = pygame.time.Clock()

        # part three
        while 1:

            self.clock.tick(60)

            self.grid.tick(self)#, self.player)
            self.player.tick(self)

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


            self.screen.fill(self.black)

            self.update_offset()
            for i in range(self.screen_width):
                for j in range(self.screen_width):
                    
                    i_adj = i + self.x_offset
                    j_adj = j + self.y_offset

                    if (self.grid.data[i_adj][j_adj] == Box.MARKED):
                        pygame.draw.rect(self.screen, (255, 0, 0), self.boxes[i][j])
                    elif (self.grid.data[i_adj][j_adj] == Box.PATH):
                        pygame.draw.rect(self.screen, ((255/2), 0, 0), self.boxes[i][j])
                    elif (self.grid.data[i_adj][j_adj] == Box.EMPTY):
                        pygame.draw.rect(self.screen, (0, 0, 255), self.boxes[i][j])


            pygame.draw.rect(self.screen, (0, 255, 0), self.boxes[self.player.x - self.x_offset][self.player.y - self.y_offset])
            pygame.display.flip()

        
    def update_offset(self):
        x = self.player.x
        y = self.player.y

        if (x < self.screen_width/2):
            self.x_offset = 0
        elif (x > self.grid_size - self.screen_width):
            self.x_offset = self.grid_size - self.screen_width
        else:
            self.x_offset = x - self.screen_width/2

        if (y < self.screen_width/2):
            self.y_offset = 0
        elif (y > self.grid_size - self.screen_width):
            self.y_offset = self.grid_size - self.screen_width
        else:
            self.y_offset = y - self.screen_width/2
        
if __name__ == '__main__':
    gs = GameSpace()
    gs.main()

    

import pygame
import sys
from snake import Snake
from gamegrid import Grid, Box

class GameSpace:

    def main(self):
        # part one
        pygame.init()
        self.size = self.width, self.height = 600, 600 
        self.black = 0, 0, 0 #RGB
        self.screen = pygame.display.set_mode(self.size)

        self.box_size = 10

        # part two
        self.player = Snake(self, 0, 0, self.box_size)
        self.grid = Grid(self, self.width/self.box_size, self.height/self.box_size)
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
            pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect)

            for i in range(self.width/self.box_size):
                for j in range(self.height/self.box_size):

                    if (self.grid.data[i][j] == Box.MARKED):
                        pygame.draw.rect(self.screen, (255, 0, 0), self.grid.boxes[i][j])
                    elif (self.grid.data[i][j] == Box.PATH):
                        pygame.draw.rect(self.screen, ((255/2), 0, 0), self.grid.boxes[i][j])
                    elif (self.grid.data[i][j] == Box.EMPTY):
                        pygame.draw.rect(self.screen, (0, 0, 255), self.grid.boxes[i][j])

            pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect)
            pygame.display.flip()


if __name__ == '__main__':
    gs = GameSpace()
    gs.main()

    

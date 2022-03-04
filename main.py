import pygame
import sys
from settings import *
from level import Level

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and title
pygame.display.set_caption(
    "Targaryen Adventure: From Valyria, With Fire and Blood")
caption_img = pygame.image.load('dragon.png')
pygame.display.set_icon(caption_img)


# game class
class Game:
    def __init__(self):

        # pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # run the level
        self.level = Level()

    # run method
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.level.run()
            pygame.display.update()
            self.clock.tick(fps)


if __name__ == '__main__':
    game = Game()
    game.run()

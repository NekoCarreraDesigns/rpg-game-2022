import pygame
import sys
from settings import *

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and title
pygame.display.set_caption(
    "Targaryen Adventure: From Valyria, With Fire and Blood")
caption_img = pygame.image.load('dragon.png')
pygame.display.set_icon(caption_img)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    pygame.display.update()

# imports for the rpg game
import pygame
from settings import *

# Tile class to display the static sprites for the game


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            './level graphics/graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

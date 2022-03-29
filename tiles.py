# imports for the rpg game
import pygame
from settings import *

# Tile class to display the static sprites for the game


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = hitbox_offset[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(
                topleft=(pos[0], pos[1] - tile_size))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)

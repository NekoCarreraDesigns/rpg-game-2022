import pygame
from settings import *
from enemy import Enemy


class Monster(Enemy):
    def __init__(self, monster_name, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics for enemies
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)

import pygame
from settings import *
from tiles import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):
        # display the game
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(world_map):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'x':
                    Tile((x, y), [self.visible_sprites])
                if col == 'P':
                    self.player = Player(
                        (x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[0] // 2
        self.offset = pygame.math.Vector2(0, 0)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx + self.half_width
        self.offset.y = player.rect.centery + self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

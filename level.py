# imports for rpg game
import pygame
from settings import *
from tiles import Tile
from player import Player
from debug import debug
from random import choice
from support import import_csv_layout, import_folder
from weapon import Weapon

# Level class to run the logic of the game, contains sprites, and methods to display sprites


class Level:
    def __init__(self):
        # display the game
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

# method to create the map of the game

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./level graphics/world_map/world_map_playerblocks.csv'),
            'grass': import_csv_layout('./level graphics/world_map/world_map_grass.csv'),
            'objects': import_csv_layout('./level graphics/world_map/world_map_objects.csv')
        }

        graphics = {
            'grass': import_folder('./level graphics/graphics/grass'),
            'objects': import_folder('./level graphics/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * tile_size
                        y = row_index * tile_size
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [
                                 self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'objects', surf)

        self.player = Player(
            (2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack)

# method for adding the weapon animations
    def create_attack(self):
        Weapon(self.player, [self.visible_sprites])

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)

# This is the class for camera movement, and to display the character offset of the
# background, inherits sprites, from level and Player.


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load(
            './level graphics/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

# draw method for the camera class

    def custom_draw(self, player):
        # getting the offset for the player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

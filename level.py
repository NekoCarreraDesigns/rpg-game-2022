# imports for rpg game
import pygame
from settings import *
from tiles import Tile
from player import Player
from random import choice
from support import import_csv_layout, import_folder
from weapon import Weapon
from ui import UI
from monster import Monster

# Level class to run the logic of the game, contains sprites, and methods to display sprites


class Level:
    def __init__(self):
        # display the game
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

# method to create the map of the game

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./level graphics/world_map/world_map_playerblocks.csv'),
            'grass': import_csv_layout('./level graphics/world_map/world_map_grass.csv'),
            'objects': import_csv_layout('./level graphics/world_map/world_map_objects.csv'),
            'enemies': import_csv_layout('./level graphics/world_map/world_map_enemies.csv')
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
                        if style == 'enemies':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Monster(monster_name, (x, y), [
                                        self.visible_sprites])

# method for adding the weapon animations

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

# method for magic ability
    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)


# method for destroying the weapon after its animation

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


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

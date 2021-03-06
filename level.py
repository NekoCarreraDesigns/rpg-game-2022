# imports for rpg game
import pygame
from particles import AnimationPlayer
from settings import *
from tiles import Tile
from player import Player
from random import choice, randint
from support import *
from weapon import Weapon
from ui import UI
from monster import Monster
from magic import MagicPlayer
from upgrade import Upgrade


# Level class to run the logic of the game, contains sprites, and methods to display sprites


class Level:
    def __init__(self):
        # display the game
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

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
                            Tile((x, y),
                                 [self.visible_sprites,
                                     self.obstacle_sprites,
                                     self.attackable_sprites],
                                 'grass',
                                 random_grass_image)
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
                                Monster(monster_name,
                                        (x, y),
                                        [self.visible_sprites,
                                         self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_exp)

# method for adding the weapon animations

    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

# method for magic ability
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [
                self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites])


# method for destroying the weapon after its animation


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

# method for player attack logic

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, True)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            offset = pygame.math.Vector2(0, 75)
                            pos = target_sprite.rect.center
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = True
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(
            particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


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

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

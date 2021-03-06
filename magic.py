from numpy import tile
import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('./level graphics/audio/heal.wav'),
            'flame': pygame.mixer.Sound('./level graphics/audio/Fire.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles(
                'aura', player.rect.center, groups)
            self.animation_player.create_particles(
                'heal', player.rect.center + pygame.math.Vector2(0, -40), groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(5):
                if direction.x:
                    offset_x = (direction.x * i) * tile_size
                    x = player.rect.centerx + offset_x + \
                        randint(-tile_size // 3, tile_size // 3)
                    y = player.rect.centery + \
                        randint(-tile_size // 3, tile_size // 3)
                    self.animation_player.create_particles(
                        'flame', (x, y), groups)
                else:
                    offset_y = (direction.y * i) * tile_size
                    x = player.rect.centerx + \
                        randint(-tile_size // 3, tile_size // 3)
                    y = player.rect.centery + offset_y + \
                        randint(-tile_size // 3, tile_size // 3)
                    self.animation_player.create_particles(
                        'flame', (x, y), groups)

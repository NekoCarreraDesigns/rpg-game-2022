import pygame
from settings import *


class UI:
    def __init__(self):
        # general attributes
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)

        # health bar and energy bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, health_bar_width, bar_height)
        self.energy_bar_rect = pygame.Rect(
            10, 34, energy_bar_width, bar_height)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw background
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface,
                         ui_border_color, bg_rect, 3)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, text_color)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, ui_bg_color,
                         text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, ui_border_color,
                         text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, item_box_size, item_box_size)
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,
                             ui_border_color_active, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)  # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, health_color)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, energy_color)

        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        # self.selection_box(80, 635)  # magic

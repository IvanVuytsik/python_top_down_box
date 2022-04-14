import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10,10, HEALTH_BAR_W, BAR_H)
        self.energy_bar_rect = pygame.Rect(10,30, ENERGY_BAR_W, BAR_H)

        # convert dict to list
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        #-------------------------psi-----------------------
        self.psi_graphics = []
        for psi in psi_data.values():
            path = psi['graphic']
            psi = pygame.image.load(path).convert_alpha()
            self.psi_graphics.append(psi)


    def show_essence(self, essence):
        text_surf = self.font.render(str(int(essence)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))
        # rect bg
        pygame.draw.rect(self.display_surface, UI_BG, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER, text_rect.inflate(10, 10), 3)


    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 60
        text_rect = text_surf.get_rect(bottomright=(x, y))
        # rect bg
        pygame.draw.rect(self.display_surface, UI_BG, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER, text_rect.inflate(10, 10), 3)


    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG, bg_rect)

        # ratio
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER, bg_rect, 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 600, has_switched)
        weapon_img = self.weapon_graphics[weapon_index]
        weapon_surf = pygame.transform.scale(weapon_img, (TILESIZE, HALF_TILE))
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def psi_overlay(self, psi_index, has_switched):
        bg_rect = self.selection_box(80, 620, has_switched)
        psi_img = self.psi_graphics[psi_index]
        psi_surf = pygame.transform.scale(psi_img, (TILESIZE, HALF_TILE))
        psi_rect = psi_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(psi_surf, psi_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_essence(player.essence)
        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.psi_overlay(player.psi_index, not player.can_switch_psi)


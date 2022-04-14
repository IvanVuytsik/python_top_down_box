import pygame
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.direction = player.status.split('_')[0]    # get front/back/right/left

        # images
        full_path = f'./graphics/weapons/{player.weapon}/{self.direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()


            #pygame.Surface((32, 16))

        if self.direction == 'right':
           self.rect = self.image.get_rect(center=player.rect.midright - pygame.math.Vector2(-8, -8))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(center=player.rect.midleft - pygame.math.Vector2(8, -8))
        elif self.direction == 'front':
            self.rect = self.image.get_rect(center=player.rect.center - pygame.math.Vector2(0, -24))
        elif self.direction == 'back':
            self.rect = self.image.get_rect(center=player.rect.center - pygame.math.Vector2(0, 24))
        else:
           self.rect = self.image.get_rect(center=(player.rect.centerx, player.rect.centery - 10))




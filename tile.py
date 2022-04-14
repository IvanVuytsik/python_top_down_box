import pygame
from settings import *
from support import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if self.sprite_type == 'obj_2x':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-16, -16)

class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, animation_type):
        super().__init__(groups)
        self.animated_data = {
            'portal': import_folder('./graphics/animated_tiles/portal'),
        }

        self.sprite_type = sprite_type

        self.frame_index = 0
        self.animation_speed = 0.25

        self.frames = self.animated_data[animation_type]
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-16, -16)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
           self.frame_index = 0
        else:
           self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()




import pygame
from support import *

class ParticlesAnimation():
    def __init__(self):
        self.frames = {
        'flame': import_folder('./graphics/particles/flame'),
        'aura': import_folder('./graphics/particles/aura'),
        'heal': import_folder('./graphics/particles/heal'),
        'summon': import_folder('./graphics/particles/summon'),

        #attacks
        'slash': import_folder('./graphics/particles/slash'),
        'darkness': import_folder('./graphics/particles/darkness'),
        'thunder': import_folder('./graphics/particles/thunder'),

        #deaths
        'blood': import_folder('./graphics/particles/blood'),

        #env
        'smoke': self.reflect_images(import_folder('./graphics/particles/smoke'))
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_smoke_particles(self, pos, groups):
        animation_frames = self.frames['smoke']
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, particle_type, pos, groups):
        animation_frames = self.frames[particle_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'psi'
        self.frame_index = 0
        self.animation_speed = 0.25
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
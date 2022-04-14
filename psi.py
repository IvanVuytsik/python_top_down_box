import pygame
from settings import *
import random
from enemy import *

class PsiAnimation:
    def __init__(self, particles_animation):
        self.particles_animation = particles_animation
        self.sounds = {
            'heal': pygame.mixer.Sound('./sounds/effects/healing.wav'),
            'flame': pygame.mixer.Sound('./sounds/effects/fire_burn.wav')
        }


    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
           self.sounds['heal'].set_volume(0.5)
           self.sounds['heal'].play()
           player.health += strength
           player.energy -= cost
           if player.health >= player.stats['health']:
              player.health = player.stats['health']
           self.particles_animation.create_particles('aura', player.rect.center, groups)
           self.particles_animation.create_particles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
           self.sounds['flame'].play()
           player.energy -= cost

           if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
           elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
           elif player.status.split('_')[0] == 'front': direction = pygame.math.Vector2(0, 1)
           else: direction = pygame.math.Vector2(0,-1)

           for i in range(1,6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    self.particles_animation.create_particles('flame', (x, y), groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    self.particles_animation.create_particles('flame', (x, y), groups)


    def summon(self, player, cost, groups):
        if player.energy >= cost:
           player.energy -= cost

        if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
        elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
        elif player.status.split('_')[0] == 'front': direction = pygame.math.Vector2(0, 1)
        else: direction = pygame.math.Vector2(0,-1)

        if direction.x:
            offset_x = direction.x * TILESIZE
            x = player.rect.centerx + offset_x
            y = player.rect.centery
            self.particles_animation.create_particles('summon', (x, y), groups)
        else:
            offset_y = direction.y * TILESIZE
            x = player.rect.centerx
            y = player.rect.centery + offset_y
            self.particles_animation.create_particles('summon', (x, y), groups)




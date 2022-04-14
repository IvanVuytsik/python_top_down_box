import random
import math
import pygame
import pygame.time

from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, death_particle, add_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphics
        self.import_graphics(monster_name)
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index] #pygame.Surface((64,64))

        # animation speed
        #if self.status == 'attack':
        self.animation_speed = 0.15

        #------------------------------------------
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-HALF_TILE, -16)
        self.obstacle_sprites = obstacle_sprites
        #--------------------------------------------

        #stats
        self.monster_name = monster_name
        monster_info = enemy_data[self.monster_name]
        self.health = monster_info['health']
        self.essence = monster_info['essence']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.exp = self.essence // 2

        #player_interaction
        self.can_attack = True
        self.attack_timer = None
        self.attack_cooldown = 600
        self.damage_player = damage_player
        self.death_particle = death_particle
        self.add_exp = add_exp

        #attack damage timer
        self.vulnerable = True
        self.hit_time = None
        self.no_hit_duration = 300

        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.attack_sound.set_volume(0.5)
        self.sound_timer = 0

    def import_graphics(self, name):
        full_path = f'./graphics/characters/{name}/'
        self.animations = {'idle': [], 'move': [],'attack': []}
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(full_path + animation)

    def get_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude() #convert vec to distance (single number)
        if distance > 0:
           direction = (player_vec - enemy_vec).normalize() #sets vet len to 1
        else:
           direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_timer = pygame.time.get_ticks()
            self.sound_timer += 1
            if self.sound_timer == 20:
               self.attack_sound.play()
               self.damage_player(self.attack_damage, self.attack_type)
               self.sound_timer = 0

        elif self.status == 'move':
            self.direction = self.get_distance_direction(player)[1] #direction
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
               self.can_attack = False
            self.frame_index = 0

        #pickimage
        #self.image = animation[int(self.frame_index)]
        if self.direction.x >= 0: self.view = False
        else: self.view = True
        self.image = pygame.transform.flip(animation[int(self.frame_index)], self.view, False)
        self.rect = self.image.get_rect(center=self.hitbox.center)

        #flickering
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_timer >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.no_hit_duration:
               self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
           self.direction = self.get_distance_direction(player)[1]
           if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
           else:
                self.health -= player.get_full_psi_damage()

           self.hit_time = pygame.time.get_ticks()
           self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.death_particle(self.rect.center, 'blood')
            self.add_exp(self.exp)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= - self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)

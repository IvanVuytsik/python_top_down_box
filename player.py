import pygame
from settings import *
from os import walk
from debug import debug
from entity import Entity
from support import *

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_psi):
        super().__init__(groups)
        self.basic_image = pygame.image.load('./graphics/img/mage_icon.png').convert_alpha()
        self.image = pygame.transform.scale(self.basic_image, (TILESIZE, TILESIZE)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-HALF_TILE, -16)

        # graphics setup
        self.import_character_animations()
        self.status = 'front'

        self.attack = False
        self.attack_cooldown = 200
        self.attack_time = None

        self.casting = False
        self.casting_cooldown = 400
        self.casting_time = None

        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        #---------------psi----------------
        self.create_psi = create_psi
        self.psi_index = 0
        self.psi = list(psi_data.keys())[self.psi_index]
        self.can_switch_psi = True
        self.psi_switch_time = None

        self.switch_duration_cooldown = 200

        #--------statistics--------------
        self.stats = {'health': 100, 'energy': 100, 'attack': 5, 'psi': 5, 'speed': 4}
        self.max_stats = {'health': 300, 'energy': 300, 'attack': 100, 'psi': 100, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 300, 'psi': 300, 'speed': 500}


        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.essence = 0
        self.speed = self.stats['speed']
        self.exp = 0

        #damage params
        self.vulnerable = True
        self.hurt_time = None
        self.no_hit_duration = 500

        #sounds
        self.weapon_attack_sound = pygame.mixer.Sound('./sounds/effects/flame.wav')
        self.weapon_attack_sound.set_volume(0.5)


    def import_character_animations(self):
        character_path = './graphics/characters/player/'
        self.animations = {'back': [], 'front': [], 'left': [], 'right': [],
                           'back_idle': [], 'front_idle': [], 'left_idle': [], 'right_idle': [],
                           'back_attack': [], 'front_attack': [], 'left_attack': [], 'right_attack': [],
                           'back_cast': [], 'front_cast': [], 'left_cast': [], 'right_cast': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
           self.frame_index = 0

        #pickimage
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        #flickering
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
           self.energy += 0.05
        else:
           self.energy = self.stats['energy']

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
           if not 'idle' in self.status and not 'attack' in self.status and not 'cast' in self.status: #has 'str' in list
              self.status += '_idle'

        if self.attack and not self.casting:
               self.direction.x = 0
               self.direction.y = 0
               if not 'attack' in self.status:
                   if 'idle' in self.status:
                       self.status = self.status.replace('_idle', '_attack')
                   else:
                       self.status += '_attack'

        elif self.casting and not self.attack:
            self.direction.x = 0
            self.direction.y = 0
            if not 'cast' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_cast')
                else:
                    self.status += '_cast'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
            if 'cast' in self.status:
                self.status = self.status.replace('_cast', '')


    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if not self.attack:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'back'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'front'
            else:
                self.direction.y = 0
            #-----------------------
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            #------------weaponchange---------
            if keys[pygame.K_q] and self.can_switch_weapon:
               self.can_switch_weapon = False
               self.weapon_switch_time = pygame.time.get_ticks()
               if self.weapon_index < len(list(weapon_data.keys())) - 1:
                   self.weapon_index += 1
               else:
                   self.weapon_index = 0

               self.weapon = list(weapon_data.keys())[self.weapon_index]

            #------------psichange---------
            if keys[pygame.K_e] and self.can_switch_psi:
                self.can_switch_psi = False
                self.psi_switch_time = pygame.time.get_ticks()
                if self.psi_index < len(list(psi_data.keys())) - 1:
                    self.psi_index += 1
                else:
                    self.psi_index = 0

                self.psi = list(psi_data.keys())[self.psi_index]

            #--------------action-------------
            if mouse_buttons[0] and self.attack == False:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            if mouse_buttons[2] and self.casting == False:
                self.casting = True
                self.casting_time = pygame.time.get_ticks()
                style = list(psi_data.keys())[self.psi_index]
                strength = list(psi_data.values())[self.psi_index]['strength'] + self.stats['psi']
                cost = list(psi_data.values())[self.psi_index]['cost']
                self.create_psi(style, strength, cost)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        #--------------------------------------------------------
        if self.attack:
           if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
              self.attack = False
              self.destroy_attack()

        if self.casting:
            current_time = pygame.time.get_ticks()
            if current_time - self.casting_time >= self.casting_cooldown:
               self.casting = False
        #-----------------------------------------------------------------
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
               self.can_switch_weapon = True
        #------------------------------------------------------------------
        if not self.can_switch_psi:
            if current_time - self.psi_switch_time >= self.switch_duration_cooldown:
                self.can_switch_psi = True
        #------------------------------------------------------------------
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.no_hit_duration:
               self.vulnerable = True

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']

        return base_damage + weapon_damage

    def get_full_psi_damage(self):
        base_damage = self.stats['psi']
        psi_damage = psi_data[self.psi]['strength']

        return base_damage + psi_damage
    #---------------------------------------------------------------------------
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.energy_recovery()
        self.move(self.stats['speed'])

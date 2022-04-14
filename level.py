import random
import pygame
from settings import *
from upgrade import *
from tile import *
from player import Player
from debug import debug
from random import *
from csv import reader
from os import walk
from enemy import Enemy

from weapon import *
from ui import *
from support import *
from psi import *
from particles import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        #sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.target_sprites = pygame.sprite.Group()

        #projectiles
        self.projectiles_group = pygame.sprite.Group()

        #create map
        self.create_map()

        #ui
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        #particles
        self.particles_animation = ParticlesAnimation()
        self.psi_animation = PsiAnimation(self.particles_animation)
    #--------------------------------MapFunctions----------------------------------
    def import_csv_layout(self, path):
        layout_map = []
        with open(path) as level_map:
            layout = reader(level_map, delimiter=',')
            for row in layout:
                layout_map.append(list(row))
            return layout_map

    #-------------------------------------------------------------------------------
    def create_map(self):
        layouts = {
            'blocks': self.import_csv_layout('./worldmap/maps/map_0/map_0_block.csv'),
            'obj_1x': self.import_csv_layout('./worldmap/maps/map_0/map_0_objects_1x.csv'),
            'obj_2x': self.import_csv_layout('./worldmap/maps/map_0/map_0_objects_2x.csv'),
            'characters': self.import_csv_layout('./worldmap/maps/map_0/map_0_characters.csv'),
            'interactive': self.import_csv_layout('./worldmap/maps/map_0/map_0_interactive.csv'),
        }

        graphics = {
            'blocks': import_folder('./worldmap/tiles/blocks'),
            'obj_1x': import_folder('./worldmap/tiles/obj_1x'),
            'obj_2x': import_folder('./worldmap/tiles/obj_2x'),
            'interactive': import_folder('./worldmap/tiles/interactive'),
        }

        #print(graphics)
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'blocks':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'obj_1x':
                            surf = graphics['obj_1x'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.target_sprites], 'obj_1x', surf)
                        if style == 'obj_2x':
                            surf = graphics['obj_2x'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'obj_2x', surf)
                        if style == 'interactive':
                            if col == '1': #portal
                                AnimatedTile((x, y), [self.visible_sprites], 'interactive', 'portal')
                            else:
                                surf = graphics['interactive'][int(col)]
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'interactive', surf)

                        if style == 'characters':
                            if col == '0':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_psi)
                            else:
                                if col == '1': monster_name = 'swordsman'
                                elif col == '2': monster_name = 'crossbowman'
                                elif col == '3': monster_name = 'linebreaker'
                                elif col == '4': monster_name = 'helbardier'
                                elif col == '5': monster_name = 'wizard'
                                elif col == '6': monster_name = 'knight'
                                else:
                                    monster_name = 'dummy'
                                #-------------------------------------------------
                                self.enemy = Enemy(monster_name, (x, y), [self.visible_sprites,
                                                            self.target_sprites],
                                                            self.obstacle_sprites,
                                                            self.damage_player,
                                                            self.generate_death_particle,
                                                            self.add_xp
                                )


    #------------------------------------------------------------------------------
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
           self.current_attack.kill()
        self.current_attack = None

    def create_psi(self, style, strength, cost):
        if style == 'heal':
           self.psi_animation.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.psi_animation.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        if style == 'summon':
            self.psi_animation.summon(self.player, cost, [self.visible_sprites])
            Enemy('shadow', (self.player.rect.x + self.player.direction.x * TILESIZE,
                            self.player.rect.y + self.player.direction.y * TILESIZE),
                  [self.visible_sprites,self.target_sprites],
                  self.obstacle_sprites,
                  self.damage_player,
                  self.generate_death_particle,
                  self.add_xp
                  )

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.target_sprites, False)
                if collision_sprites:
                    for target in collision_sprites:
                        if target.sprite_type == 'obj_1x':
                           pos = target.rect.center
                           #offset = pygame.math.Vector2(0, 50)
                           for particle in range(randint(1, 3)):
                               offset = randint(-20, 20)
                               self.particles_animation.create_smoke_particles((pos[0]+offset, pos[1]+offset), self.visible_sprites)
                           target.kill()
                        else:
                           target.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, animation_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.particles_animation.create_particles(animation_type, self.player.rect.center, self.visible_sprites)

    def generate_death_particle(self, pos, particle_type):
        self.particles_animation.create_particles(particle_type, pos, self.visible_sprites)

    def add_xp(self, amount):
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

#------------------------------------------------------------------------------
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #offset
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # [0,0]

        #floor
        self.floor_surf = pygame.image.load('./worldmap/maps/map_0/map_0.png')
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #draw floor
        self.floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, self.floor_offset_pos)

        #getting the offset
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery): #list(sprites) / key y pos of each sprite
            self.offset_pos = sprite.rect.topleft - self.offset #rect - vector offset based on char rect
            if self.offset_pos[0] < WIDTH and self.offset_pos[0] > -TILESIZE \
                    and self.offset_pos[1] > -TILESIZE and self.offset_pos[1] < HEIGHT:
               self.display_surface.blit(sprite.image, self.offset_pos) #img / rect

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type=='enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

        #debug rect draw
        #debug(player.rect, 1000, 10)
        #debug(player.status, 1000, 40)


from support import *

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HALF_TILE = TILESIZE // 2

HITBOX_OFFSET = {
    'player': -HALF_TILE,
}

BAR_H = 20
HEALTH_BAR_W = 200
ENERGY_BAR_W = 200
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/Audiowide-Regular.ttf'
UI_FONT_SIZE = 20

#colors
BLACK = (0, 0, 0)
WATER_COLOR = '#71ddee'
UI_BG = '#8a7d76'
UI_BG_MENU = '#111111' #9a9a9a
UI_BORDER = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_ACTIVE = 'gold'

#upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


weapon_data = {
    'staff': {'cooldown': 200, 'damage': 20, 'graphic': './graphics/weapons/staff/icon.png'},
    }

psi_data = {
    'flame': {'strength': 10, 'cost': 20, 'graphic': './graphics/psi/flame/flame.png'},
    'heal': {'strength': 25, 'cost': 20, 'graphic': './graphics/psi/heal/heal.png'},
    'summon': {'strength': 20, 'cost': 25, 'graphic': './graphics/psi/summon/summon_portal.png'},
    }

enemy_data = {
    'swordsman': {'health': 150, 'essence': 10, 'damage': 20, 'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300, 'attack_sound': './sounds/effects/slash.wav'},
    'crossbowman': {'health': 100, 'essence': 10, 'damage': 15, 'attack_type': 'slash', 'speed': 2, 'resistance': 3, 'attack_radius': 250, 'notice_radius': 300,'attack_sound': './sounds/effects/pierce.wav'},
    'helbardier': {'health': 120, 'essence': 10, 'damage': 20, 'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 300,'attack_sound': './sounds/effects/pierce.wav'},
    'linebreaker': {'health': 200, 'essence': 30, 'damage': 25, 'attack_type': 'slash', 'speed': 2, 'resistance': 1, 'attack_radius': 60, 'notice_radius': 300,'attack_sound': './sounds/effects/bash.wav'},
    'wizard': {'health': 100, 'essence': 60, 'damage': 30, 'attack_type': 'darkness', 'speed': 3, 'resistance': 3, 'attack_radius': 250, 'notice_radius': 300,'attack_sound': './sounds/effects/energy.wav'},
    'knight': {'health': 300, 'essence': 50, 'damage': 30, 'attack_type': 'slash', 'speed': 4, 'resistance': 1, 'attack_radius': 50, 'notice_radius': 300,'attack_sound': './sounds/effects/slash.wav'},
    'shadow': {'health': 200, 'essence': 10, 'damage': 30, 'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300, 'attack_sound': './sounds/effects/slash.wav'},
}



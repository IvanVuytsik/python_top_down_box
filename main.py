import pygame, sys
import random
from settings import *
from debug import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Spells_and_Monsters')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()

        main_theme = pygame.mixer.Sound('./sounds/theme.mp3')
        main_theme.set_volume(0.05)
        main_theme.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill('black')

            # run levels
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__=='__main__':
    game = Game()
    game.run()
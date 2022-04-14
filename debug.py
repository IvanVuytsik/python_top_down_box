import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, x = 10, y = 10):
    display_surface = pygame.display.get_surface()

    surf = font.render(str(info), True, (255, 255, 255))
    rect = surf.get_rect(topleft=(x, y))

    pygame.draw.rect(display_surface, (0, 0, 0), rect)

    display_surface.blit(surf, rect)
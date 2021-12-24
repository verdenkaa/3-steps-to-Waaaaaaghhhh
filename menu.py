import pygame
import os

class Menu():
    pass


def draw_menu(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    running = False
                    os.system('python persons.py')             



if __name__ == '__main__':
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3-step to Waagh!')
    draw_menu(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
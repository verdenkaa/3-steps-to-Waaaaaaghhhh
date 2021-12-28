import pygame
import os
import sys
import pygame as pg

class Menu_sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 250))
        self.image = load_image('fon.jpg', 500, 500)
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)


def load_image(name, h, w, colorkey=None):
    image = pygame.image.load(f"Sprites/{name}")
    image = pygame.transform.scale(image, (h, w))
    return image


def but_cl():
    pg.mixer.music.load('Sounds/button-pressing.mp3')
    pg.mixer.music.play()
    pg.mixer.music.set_volume(2)


def menu_game():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pos()[0] > 63 and pygame.mouse.get_pos()[0] < 417:
                    if pygame.mouse.get_pos()[1] > 205 and pygame.mouse.get_pos()[1] < 250:
                        running = False
                        but_cl()
                        os.system('python persons.py')
                        pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
                        pg.mixer.music.play()
                        pg.mixer.music.set_volume(0.5)
                if pygame.mouse.get_pos()[0] > 85.5 and pygame.mouse.get_pos()[0] < 394.5:
                    if pygame.mouse.get_pos()[1] > 105 and pygame.mouse.get_pos()[1] < 150:
                        #but_cl()
                        print('Разроботчики добавят эту функцию в следующих версиях)')
                if pygame.mouse.get_pos()[0] > 149.5 and pygame.mouse.get_pos()[0] < 340.5:
                    if pygame.mouse.get_pos()[1] > 305 and pygame.mouse.get_pos()[1] < 350:
                        #but_cl()
                        print('Разроботчики добавят эту функцию в следующих версиях)')


if __name__ == '__main__':
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3-step to Waagh!')

    all_sprites = pygame.sprite.Group()
    menu = Menu_sprite()
    all_sprites.add(menu)
    all_sprites.draw(screen)

    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render("Сюжетный режим", True, (255, 0, 0))
    text_comp_w = text_comp.get_width() #309
    text_comp_h = text_comp.get_height() #35
    screen.blit(text_comp, (95.5, 115))
    pygame.draw.rect(screen, (255, 0, 0), (95.5 - 10, 115 - 10,
                                           text_comp_w + 20, text_comp_h + 20), 1)

    font_inf = pygame.font.Font(None, 50)
    text_inf = font_inf.render("Бесконечный режим", True, (255, 0, 0))
    text_inf_w = text_inf.get_width() #354
    text_inf_h = text_inf.get_height() #35
    screen.blit(text_inf, (73, 215))
    pygame.draw.rect(screen, (255, 0, 0), (73 - 10, 215 - 10,
                                           text_inf_w + 20, text_inf_h + 20), 1)

    font_pref = pygame.font.Font(None, 50)
    text_pref = font_pref.render("Настройки", True, (255, 0, 0))
    text_pref_w = text_pref.get_width() #181
    text_pref_h = text_pref.get_height() #35
    screen.blit(text_pref, (159.5, 315))
    pygame.draw.rect(screen, (255, 0, 0), (159.5 - 10, 315 - 10,
                                           text_pref_w + 20, text_pref_h + 20), 1)

    pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.5)

    fps = 120
    clock = pygame.time.Clock()
    clock.tick(fps)

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        menu_game()
    pygame.quit()
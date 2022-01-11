import pygame
import os
import pygame as pg
import sys
from random import randint

class Menu_sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((640, 360))
        self.image = load_image('campaign_map.jpg', 1280, 720)
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)


def load_image(name, h, w, colorkey=None):
    image = pygame.image.load(f"Sprites/{name}")
    image = pygame.transform.scale(image, (h, w))
    return image

def load_ork(name, colorkey=None):
    fullname = 'Sprites/' + name

    print(fullname)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def but_cl():
    button_sound = pg.mixer.Sound('Sounds/button-pressing.mp3')
    button_sound.play()


def this_mission():
    missia = open('mission_number.txt', 'r')
    num_company = int(missia.readlines()[0])
    missia.close()
    return num_company


def dr_pole():
    all_sprites = pygame.sprite.Group()
    menu = Menu_sprite()
    all_sprites.add(menu)
    all_sprites.draw(screen)

    ork_base = load_image('ork_face.png', 40, 40)
    ork_base_img = pygame.transform.scale(ork_base, (40, 40))
    screen.blit(ork_base_img, (coord[0], coord[1]))
    pygame.display.update()


def monolog():
    ork = load_ork(f'{orks[num_ork]}/Body.png')
    ork = pygame.transform.scale(ork, (130, 200))
    screen.blit(ork, (0, 390))

    fraze = open('suget.txt', 'r')
    ork_dialog = fraze.readlines()[this_mission()]
    fraze.close()
    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render(ork_dialog, True, (255, 0, 0))
    text_comp_w = text_comp.get_width()
    kol_str = text_comp_w // 500
    for j in range(kol_str):
        font_comp = pygame.font.Font(None, 50)
        text_comp = font_comp.render(ork_dialog[(len(ork_dialog) // kol_str) * j:(len(ork_dialog) // kol_str) * (j + 1)], True, (255, 0, 0))
        text_comp_w = text_comp.get_width()
        screen.blit(text_comp, (150, 400 + (j * 34)))
    if text_comp_w % 500 != 0:
        font_comp = pygame.font.Font(None, 50)
        text_comp = font_comp.render(ork_dialog[(len(ork_dialog) // kol_str) * kol_str:], True, (255, 0, 0))
        text_comp_w = text_comp.get_width()
        screen.blit(text_comp, (150, 400 + (kol_str * 34)))
    pygame.draw.rect(screen, (255, 0, 0), (140, 390, 650, 400 + (kol_str * 34)), 1)
    pygame.display.update()


def menu_game():
    running = True
    monolog()
    dialog = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                but_cl()
                if dialog:
                    dr_pole()
                    dialog = False
                if not dialog:
                    if pygame.mouse.get_pos()[0] > coord[0] and pygame.mouse.get_pos()[0] < (coord[0] + 40):
                        if pygame.mouse.get_pos()[1] > coord[1] and pygame.mouse.get_pos()[1] < (coord[1] + 40):
                            #здесь переход на игру
                            missia = open('mission_number.txt', 'r')
                            num_company = int(missia.readlines()[0]) + 1 #заменить после добавления игры и проверки на прохождение на num_company = int(missia.readlines()[0])
                            missia.close()
                            missia = open('mission_number.txt', 'w') #удалить после добавления игры и проверки на прохождение
                            missia.write(str(num_company))#удалить после добавления игры и проверки на прохождение
                            missia.close()#удалить после добавления игры и проверки на прохождение
                            running = False
                            if num_company != 4:
                                menu_game()
                            else:
                                #здесь вставка на самолёт
                                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()


if __name__ == '__main__':
    pygame.init()
    size = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3-step to Waagh!')

    orks = ['Nob', 'Flash', 'Tank', 'Meh']

    ork_type = open('player_ork.txt', 'r')
    num_ork = orks.index(ork_type.readlines()[0])
    ork_type.close()

    coord = [randint(900, 1050), randint(250, 400)]

    dr_pole()

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
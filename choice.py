import pygame
import os
import pygame as pg
import sys

class Сhoice_sprite(pygame.sprite.Sprite):
    def __init__(self, name, image_s_x, image_s_y, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((center_x, center_y))
        self.image = load_image2(name, image_s_x, image_s_y)
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)


def draw_cursor(screen, posit):
    screen.blit(cursor_image, posit)


def load_image2(name, h, w, colorkey=None):
    image = pygame.image.load(f"Sprites/{name}")
    image = pygame.transform.scale(image, (h, w))
    return image


def load_ork(name, colorkey=None):
    fullname = 'Sprites/' + name

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

def start(num_ork):
    global orks

    all_sprites = pygame.sprite.Group()
    menu = Сhoice_sprite('fon.jpg', 500, 500, 250, 250)
    all_sprites.add(menu)
    all_sprites.draw(screen)

    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render("Ваш орк: ('|_|')", True, (255, 0, 0))
    text_comp_w = text_comp.get_width() #242
    text_comp_h = text_comp.get_height() #35
    screen.blit(text_comp, (0, 10))
    pygame.draw.rect(screen, (255, 0, 0), (0, 10 - 10,
                                           260, text_comp_h + 20), 1)

    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render("Следующий", True, (255, 0, 0))
    text_comp_w = text_comp.get_width() #218
    text_comp_h = text_comp.get_height() #35
    screen.blit(text_comp, (270, 90))
    pygame.draw.rect(screen, (0, 0, 0), (270 - 10, 90 - 10,
                                           text_comp_w + 20, text_comp_h + 20), 2)

    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render("Прошлый", True, (255, 0, 0))
    text_comp_w = text_comp.get_width() #168
    text_comp_h = text_comp.get_height() #35
    screen.blit(text_comp, (300, 180))
    pygame.draw.rect(screen, (0, 0, 0), (270 - 10, 180 - 10,
                                           text_comp_w + 70, text_comp_h + 20), 2)

    font_comp = pygame.font.Font(None, 39)
    text_comp = font_comp.render("Немного информации о вашем орке:", True, (255, 0, 0))
    text_comp_w = text_comp.get_width() #478
    text_comp_h = text_comp.get_height() #35
    screen.blit(text_comp, (0, 300))
    pygame.draw.rect(screen, (255, 0, 0), (0, 300 - 10,
                                           488, text_comp_h + 20), 1)

    text = open('Text/orks_info.txt', 'r', encoding='utf-8')
    ork_info = text.readlines()[num_ork].split('\n')[0]
    text.close()
    font_comp = pygame.font.Font(None, 20)
    text_comp = font_comp.render(ork_info, True, (255, 0, 0))
    text_comp_w = text_comp.get_width()
    text_comp_h = text_comp.get_height()
    kol_str = text_comp_w // 500
    for i in range(kol_str):
        font_comp = pygame.font.Font(None, 17)
        text_comp = font_comp.render(ork_info[(len(ork_info) // kol_str) * i:(len(ork_info) // kol_str) * (i + 1)], True, (255, 0, 0))
        text_comp_w = text_comp.get_width()
        text_comp_h = text_comp.get_height()
        screen.blit(text_comp, (0, 370 + (i * 15)))
    if text_comp_w % 500 != 0:
        font_comp = pygame.font.Font(None, 17)
        text_comp = font_comp.render(ork_info[(len(ork_info) // kol_str) * kol_str:], True, (255, 0, 0))
        text_comp_w = text_comp.get_width()
        text_comp_h = text_comp.get_height()
        screen.blit(text_comp, (0, 370 + (kol_str * 15)))

    ork = load_ork(f'{orks[num_ork]}/Body.png')
    play_ork = open('Text/player_ork.txt', 'w')
    play_ork.write(orks[num_ork])
    play_ork.close()
    ork = pygame.transform.scale(ork, (130, 200))
    screen.blit(ork, (70, 80))
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3-step to Waagh! Choose your Orks!')

    cursor_image = load_image2('cursor.png', 25, 25)
    pygame.mouse.set_visible(False)

    orks = ['Nob', 'Flash', 'Tank', 'Meh']

    pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.25)

    ork_type = open('Text/player_ork.txt', 'r')
    start(orks.index(ork_type.readlines()[0]))
    ork_type.close()

    fps = 120
    clock = pygame.time.Clock()
    clock.tick(fps)

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        ork_type = open('Text/player_ork.txt', 'r')
        num_ork = orks.index(ork_type.readlines()[0])
        ork_type.close()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] > 260 and pygame.mouse.get_pos()[0] < 498:
                        if pygame.mouse.get_pos()[1] > 80 and pygame.mouse.get_pos()[1] < 135:
                            but_cl()
                            num_ork += 1
                            if num_ork > len(orks) - 1:
                                num_ork = 0
                            start(num_ork)
                            pygame.display.update()
                    if pygame.mouse.get_pos()[0] > 260 and pygame.mouse.get_pos()[0] < 498:
                        if pygame.mouse.get_pos()[1] > 170 and pygame.mouse.get_pos()[1] < 225:
                            but_cl()
                            num_ork -= 1
                            if num_ork < 0:
                                num_ork = 3
                            start(num_ork)
                            pygame.display.update()
            start(num_ork)
            draw_cursor(screen, pygame.mouse.get_pos())
            pygame.display.flip()

    pygame.quit()
import pygame
import os
import pygame as pg
import sys


class Menu_sprite(pygame.sprite.Sprite):
    def __init__(self):
        # класс для создания фона в виде спрайта
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 250))
        self.image = load_image('fon.jpg', 500, 500)
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)


def draw_cursor(screen, posit):
    # эта функция требуется для отрисовки курсора
    screen.blit(cursor_image, posit)


def load_image(name, h, w, colorkey=None):
    # этой функцией мы загружаем изображения
    image = pygame.image.load(f"Sprites/{name}")
    image = pygame.transform.scale(image, (h, w))
    return image


def but_cl():
    # этой функцией мы воспроизводим звук нажатия мышки
    button_sound = pg.mixer.Sound('Sounds/button-pressing.mp3')
    button_sound.play()


def menu_game():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                but_cl()
                if pygame.mouse.get_pos()[0] > 63:
                    if pygame.mouse.get_pos()[0] < 417:
                        if pygame.mouse.get_pos()[1] > 205:
                            if pygame.mouse.get_pos()[1] < 250:
                                # здесь мы проверяем координаты
                                # В данных координатах находится
                                # кнопка "Бесконеный режим"
                                running = False
                                pg.mixer.music.pause()
                                game = open('Text/game_regim.txt', 'w')
                                game.write('Infinity')
                                game.close()
                                os.startfile('persons')
                                sys.exit()
                if pygame.mouse.get_pos()[0] > 85.5:
                    if pygame.mouse.get_pos()[0] < 394.5:
                        if pygame.mouse.get_pos()[1] > 105:
                            if pygame.mouse.get_pos()[1] < 150:
                                # здесь мы проверяем координаты
                                # В данных координатах находится
                                # кнопка "Сюжетный режим"
                                running = False
                                pg.mixer.music.pause()
                                os.startfile('campaign')
                                sys.exit()
                if pygame.mouse.get_pos()[0] > 149.5:
                    if pygame.mouse.get_pos()[0] < 340.5:
                        if pygame.mouse.get_pos()[1] > 305:
                            if pygame.mouse.get_pos()[1] < 350:
                                # здесь мы проверяем координаты
                                # В данных координатах находится
                                # кнопка "Персонажи"
                                running = False
                                pg.mixer.music.pause()
                                os.startfile('choice')
                                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # При нажатии на Escape выходим из приложения
                    running = False
                    sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # При движении мыши будет перерисовываться курсор
                draw_cursor(screen, pygame.mouse.get_pos())
                pygame.display.flip()
                draw_menu()


def draw_menu():
    # здесь происходит отрисовка интерфейса
    all_sprites = pygame.sprite.Group()
    menu = Menu_sprite()
    all_sprites.add(menu)
    all_sprites.draw(screen)
    # отрисовываем фон

    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render("Сюжетный режим", True, (255, 0, 0))
    text_comp_w = text_comp.get_width()
    text_comp_h = text_comp.get_height()
    screen.blit(text_comp, (95.5, 115))
    rect_button = (95.5 - 10, 115 - 10, text_comp_w + 20, text_comp_h + 20)
    pygame.draw.rect(screen, (255, 0, 0), rect_button, 1)
    # рисуем кнопку сюжетного режима

    font_inf = pygame.font.Font(None, 50)
    text_inf = font_inf.render("Бесконечный режим", True, (255, 0, 0))
    text_inf_w = text_inf.get_width()
    text_inf_h = text_inf.get_height()
    screen.blit(text_inf, (73, 215))
    rect_button = (73 - 10, 215 - 10, text_inf_w + 20, text_inf_h + 20)
    pygame.draw.rect(screen, (255, 0, 0), rect_button, 1)
    # рисуем кнопку бесконечного режима

    font_pref = pygame.font.Font(None, 50)
    text_pref = font_pref.render("Персонажи", True, (255, 0, 0))
    text_pref_w = text_pref.get_width()
    text_pref_h = text_pref.get_height()
    screen.blit(text_pref, (159.5, 315))
    rect_button = (159.5 - 10, 315 - 10, text_pref_w + 20, text_pref_h + 20)
    pygame.draw.rect(screen, (255, 0, 0), rect_button, 1)
    # рисуем кнопку выбора орка


if __name__ == '__main__':
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3-step to Waagh!')
    # меняем размер окна и его заголовок

    cursor_image = load_image('cursor.png', 25, 25)
    pygame.mouse.set_visible(False)
    # отключаем системный курсор

    draw_menu()

    pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.5)
    # включение фоновой музыки

    fps = 240
    clock = pygame.time.Clock()
    clock.tick(fps)

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        menu_game()
    pygame.quit()

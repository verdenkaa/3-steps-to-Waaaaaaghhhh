import pygame
import os
import pygame as pg
import sys
from random import randint


class Menu_sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # инициализируем спрайты
        self.image = pygame.Surface((640, 360))
        self.image = load_image('campaign_map.jpg', 1280, 720)
        # загружаем фон с помощью функции load_image
        self.rect = self.image.get_rect()
        # определяем размеры
        self.rect.center = (640, 360)
        # указываем центр изображения


def load_image(name, h, w, colorkey=None):
    image = pygame.image.load(f"Sprites/{name}")
    # загружаем изображение из папки спрайт
    image = pygame.transform.scale(image, (h, w))
    # масштабируем
    return image


def load_ork(name, colorkey=None):
    fullname = 'Sprites/' + name

    image = pygame.image.load(fullname)
    # загружаем изображение
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    # проверка на colorkey
    return image


def but_cl():
    button_sound = pg.mixer.Sound('Sounds/button-pressing.mp3')
    # загружаем звук нажатия на кнопку
    button_sound.play()
    # проигрываем звук


def this_mission():
    missia = open('Text/mission_number.txt', 'r')
    # открываем файл с номером миссии
    num_company = int(missia.readlines()[0])
    # записываем номер компании в num_company
    missia.close()
    # закрываем файл
    return num_company
    # возвращаем номер компании


def dr_pole():
    all_sprites = pygame.sprite.Group()
    # делаем группу спрайтов
    menu = Menu_sprite()
    # создаём фон
    all_sprites.add(menu)
    # добавляем фон в группу спрайтов
    all_sprites.draw(screen)
    # отрисовываем спрайты на экране

    ork_base = load_image('ork_face.png', 40, 40)
    # закружаем точку миссии в виде лица орка
    ork_base_img = pygame.transform.scale(ork_base, (40, 40))
    # масштабируем точку
    screen.blit(ork_base_img, (coord[0], coord[1]))
    # отрисовка точки миссии
    pygame.display.update()
    # обновляем экран для отображения элементов


def monolog(missia_n):
    ork = load_ork(f'{orks[num_ork]}/Body.png')
    # загружаем вашего орка
    ork = pygame.transform.scale(ork, (130, 200))
    # масштабируем его
    screen.blit(ork, (0, 390))
    # отрисовываем его

    fraze = open('Text/suget.txt', 'r', encoding='utf-8')
    # читаем сюжетные фразы
    ork_dialog = fraze.readlines()[this_mission()][:-1]
    # убираем '\n'
    fraze.close()
    font_comp = pygame.font.Font(None, 50)
    # выбираем шрифт
    text_comp = font_comp.render(ork_dialog, True, (255, 0, 0))
    # делаем текст с данным шрифтом
    text_comp_w = text_comp.get_width()
    # получаем его длину
    kol_str = text_comp_w // 700
    # смотрим сколько строк перенесётся
    for j in range(kol_str):
        # запускаем цикл для отрисовки каждого из перенесённых текстов
        font_comp = pygame.font.Font(None, 50)
        # выбираем шрифт
        text_del = len(ork_dialog) // kol_str
        razdel_text = ork_dialog[text_del * j:text_del * (j + 1)]
        text_comp = font_comp.render(razdel_text, True, (255, 0, 0))
        # делаем текст с созданным ранее шрифтом, разделяя его
        text_comp_w = text_comp.get_width()
        # получаем длину текста
        screen.blit(text_comp, (150, 400 + (j * 34)))
        # отрисовываем его
    if text_comp_w % 700 != 0:
        # проверка на наличие оставшихся строк
        font_comp = pygame.font.Font(None, 50)
        # выбираем шрифт
        text_del = len(ork_dialog) // kol_str
        razd_text = ork_dialog[text_del * kol_str:]
        text_comp = font_comp.render(razd_text, True, (255, 0, 0))
        # делаем текст с созданным ранее шрифтом, разделяя его
        text_comp_w = text_comp.get_width()
        # получаем длину текста
        screen.blit(text_comp, (150, 400 + (kol_str * 34)))
        # отрисовываем его
    if missia_n == 3:
        pygame.draw.rect(screen, (255, 0, 0),
                         (140, 390, 920, 68 + (kol_str * 34)), 1)
        # отрисовываем окно диалога
    else:
        pygame.draw.rect(screen, (255, 0, 0),
                         (140, 390, 820, 68 + (kol_str * 34)), 1)
        # отрисовываем окно диалога
    pygame.display.update()
    # обновляем экран


def draw_game():
    running = True
    num_company = this_mission()
    # проверяем номер миссии
    monolog(num_company)
    # отрисовываем диалог
    if num_company == 3:
        # проверка на прохождение всех миссий
        pg.mixer.music.pause()
        # останавливаем музыку
        missia = open('Text/mission_number.txt', 'w')
        # открываем файл
        missia.write('0')
        # обнуляем количество пройденных миссий, т.к. сюжет пройден
        missia.close()
        # закрываем файл
        pygame.time.wait(5000)
        # даём время игроку для прочтения
        os.startfile('fly')
        # запускаем ехе с самолётом
        sys.exit()
        # закрываем кампанию
    dialog = True
    # включаем режим диалога

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                os.startfile('menu')
                # при выходе из игры открываем меню
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                but_cl()
                # воспроизводим звук нажатия мыши
                if event.button == 1:
                    # проверка на нажатие левой кнопки мыши
                    if dialog:
                        # проверка на режим диалога
                        dr_pole()
                        # перерисовываем поле для удаления диалога
                        dialog = False
                        # убираем режим диалога
                if pygame.mouse.get_pos()[0] > coord[0]:
                    if pygame.mouse.get_pos()[0] < (coord[0] + 40):
                        # проверка на координаты точки по х
                        if pygame.mouse.get_pos()[1] > coord[1]:
                            if pygame.mouse.get_pos()[1] < (coord[1] + 40):
                                # проверка на координаты точки по у
                                game = open('Text/game_regim.txt', 'w')
                                # в файле режима игры записываем режим кампании
                                game.write('Campaign')
                                game.close()
                                pg.mixer.music.pause()
                                # ставим музыку на паузу
                                os.startfile('persons')
                                # запускаем игру
                                sys.exit()
                                # выключаем окно
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # при нажатии на escape окно закрывается
                    running = False
                    os.startfile('menu')
                    sys.exit()


if __name__ == '__main__':
    pygame.init()
    # инициализируем pygame
    size = 1280, 720
    # устанавливаем размер окна
    screen = pygame.display.set_mode(size)
    # меняем размер окна
    pygame.display.set_caption('3-step to Waagh!')
    # меняем имя окна

    orks = ['Nob', 'Flash', 'Tank', 'Meh']
    # список орков

    ork_type = open('Text/player_ork.txt', 'r')
    # узнаем орка, которого выбрал игрок
    num_ork = orks.index(ork_type.readlines()[0])
    ork_type.close()

    coord = [randint(900, 1050), randint(250, 400)]
    # создаём координаты для точки

    dr_pole()
    # рисуем поле

    pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
    # проигрываем фоновую музыку
    pg.mixer.music.play(-1)
    # проигрываем музыку с параметром -1 для постоянного проигрывания
    pg.mixer.music.set_volume(0.5)
    # меняем громкость музыки до комфортного

    fps = 120
    # максимально кол-во фпс
    clock = pygame.time.Clock()
    clock.tick(fps)

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        draw_game()
    pygame.quit()

import pygame
import os
import pygame as pg
import sys


class Сhoice_sprite(pygame.sprite.Sprite):
    def __init__(self, name, image_s_x, image_s_y, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        #инициализируем спрайты
        self.image = pygame.Surface((center_x, center_y))
        self.image = load_image2(name, image_s_x, image_s_y)
        #загружаем фон с помощью функции load_image
        self.rect = self.image.get_rect()
        #определяем размеры
        self.rect.center = (center_x, center_y)
        #указываем центр изображения


def draw_cursor(screen, posit):
    screen.blit(cursor_image, posit)
    #рисуем курсо на экране


def load_image2(name, h, w, colorkey=None):
    image = pygame.image.load(f"Sprites/{name}")
    #загружаем изображение
    image = pygame.transform.scale(image, (h, w))
    #масштабируем
    return image
    #возвращаем


def load_ork(name, colorkey=None):
    fullname = 'Sprites/' + name

    image = pygame.image.load(fullname)
    #загружаем изображение орка из папки со спрайтами
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
    #возвращаем изображение


def but_cl():
    button_sound = pg.mixer.Sound('Sounds/button-pressing.mp3')
    #загружаем звук нажатия
    button_sound.play()
    #проигрываем звук


def start(num_ork):
    global orks
    #делаем переменную орк глобальной

    all_sprites = pygame.sprite.Group()
    #создаём группу спрайтов
    
    menu = Сhoice_sprite('fon.jpg', 500, 500, 250, 250)
    #загружаем фон
    all_sprites.add(menu)
    #добавляем спрайт меню к группе спрайтов
    all_sprites.draw(screen)
    #отрисовываем спрайты на экран

    font_comp = pygame.font.Font(None, 50)
    #делаем шрифт
    text_comp = font_comp.render("Ваш орк: ('|_|')", True, (255, 0, 0))
    #делаем текст для панели информации
    text_comp_w = text_comp.get_width()
    #получаем ширину текста для панели информации
    text_comp_h = text_comp.get_height()
    #получаем высоту текста для панели информации
    screen.blit(text_comp, (0, 10))
    #отрисовываем текст
    pygame.draw.rect(screen, (255, 0, 0), (0, 10 - 10, 260, text_comp_h + 20), 1)
    #рисуем окантовку
    
    text_comp = font_comp.render("Следующий", True, (255, 0, 0))
    #делаем текст для кнопки
    text_comp_w = text_comp.get_width()
    #получаем ширину текста для кнопки
    text_comp_h = text_comp.get_height()
    #получаем высоту текста для кнопки
    screen.blit(text_comp, (270, 90))
    #отрисовываем текст
    pygame.draw.rect(screen, (0, 0, 0), (270 - 10, 90 - 10,
                                         text_comp_w + 20, text_comp_h + 20), 2)
    #рисуем окантовку кнопки
    
    text_comp = font_comp.render("Прошлый", True, (255, 0, 0))
    #делаем текст для кнопки
    text_comp_w = text_comp.get_width()
    #получаем ширину текста для кнопки
    text_comp_h = text_comp.get_height()
    #получаем высоту текста для кнопки
    screen.blit(text_comp, (300, 180))
    #отрисовываем текст
    pygame.draw.rect(screen, (0, 0, 0), (270 - 10, 180 - 10,
                                         text_comp_w + 70, text_comp_h + 20), 2)
    #рисуем окантовку кнопки

    font_comp = pygame.font.Font(None, 39)
    text_comp = font_comp.render(
        "Немного информации о вашем орке:", True, (255, 0, 0))
    #делаем текст для панели информации
    text_comp_w = text_comp.get_width()
    #получаем ширину текста для панели информации
    text_comp_h = text_comp.get_height()
    #получаем высоту текста для панели информации
    screen.blit(text_comp, (0, 300))
    #отрисовываем текст
    pygame.draw.rect(screen, (255, 0, 0), (0, 300 - 10,
                                           488, text_comp_h + 20), 1)
    #рисуем окантовку панели информации

    text = open('Text/orks_info.txt', 'r', encoding='utf-8')
    #открываем файл с информацией об орках
    ork_info = text.readlines()[num_ork].split('\n')[0]
    #записываем информацию об орке в переменную
    text.close()
    #закрываем файл
    font_comp = pygame.font.Font(None, 20)
    #устанавливаем шрифт
    text_comp = font_comp.render(ork_info, True, (255, 0, 0))
    #создаем текст
    text_comp_w = text_comp.get_width()
    #получаем ширину текста
    kol_str = text_comp_w // 500
    #получаем количество разделённых строк
    for i in range(kol_str):
        font_comp = pygame.font.Font(None, 17)
        #устанавливаем шрифт
        text_comp = font_comp.render(ork_info[(len(
            ork_info) // kol_str) * i:(len(ork_info) // kol_str) * (i + 1)], True, (255, 0, 0))
        #создаем текст
        screen.blit(text_comp, (0, 370 + (i * 15)))
        #отрисовываем текст
    if text_comp_w % 500 != 0:
        font_comp = pygame.font.Font(None, 17)
        #устанавливаем шрифт
        text_comp = font_comp.render(
            ork_info[(len(ork_info) // kol_str) * kol_str:], True, (255, 0, 0))
        #создаем текст
        screen.blit(text_comp, (0, 370 + (kol_str * 15)))
        #отрисовываем текст

    ork = load_ork(f'{orks[num_ork]}/Body.png')
    #запускаем функцию для отрисовки орка
    play_ork = open('Text/player_ork.txt', 'w')
    #открываем файл для записи имени орка
    play_ork.write(orks[num_ork])
    #записываем имя другого орка
    play_ork.close()
    #закрываем файл
    ork = pygame.transform.scale(ork, (130, 200))
    #масштабируем орка
    screen.blit(ork, (70, 80))
    #отрисовываем его
    pygame.display.update()
    #обновляем экран


if __name__ == '__main__':
    pygame.init()
    #инициализируем pygame
    size = width, height = 500, 500
    #устанавливаем размер окна
    screen = pygame.display.set_mode(size)
    #меняем размер окна
    pygame.display.set_caption('3-step to Waagh! Choose your Orks!')
    #меняем оглавление окна

    cursor_image = load_image2('cursor.png', 25, 25)
    #загружаем курсор
    pygame.mouse.set_visible(False)
    #отключаем видимость системного курсора

    orks = ['Nob', 'Flash', 'Tank', 'Meh']
    #список орков

    pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
    #загружаем фоновую музыку
    pg.mixer.music.play(-1)
    #запускаем ее в бескнонечном проигрывании
    pg.mixer.music.set_volume(0.25)
    #меняем громкость до комфортной

    ork_type = open('Text/player_ork.txt', 'r')
    #читаем орка, которого игрок выбрал до этого
    start(orks.index(ork_type.readlines()[0]))
    #отрисовываем интерфейс
    ork_type.close()
    #закрываем файл

    fps = 120
    #указываем максимальны фпс
    clock = pygame.time.Clock()
    clock.tick(fps)

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        ork_type = open('Text/player_ork.txt', 'r')
		#читаем орка, которого игрок выбрал до этого
        num_ork = orks.index(ork_type.readlines()[0])
        #узнаем его номер в списке
        ork_type.close()
        #закрываем файл

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
					#при выходе из игры возвращаем игрока в меню
                    running = False
                    os.startfile('menu')
                    sys.exit()
                    #закрываем окно
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
						#на клавишу escape закрываем окно и включаем меню
                        running = False
                        os.startfile('menu')
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] > 260 and pygame.mouse.get_pos()[
                            0] < 498:
								#проверка на координаты точки по х
                        if pygame.mouse.get_pos()[1] > 80 and pygame.mouse.get_pos()[
                                1] < 135:
									#проверка на координаты точки по у
                            but_cl()
                            #воспроизводим звук нажатия на мышь
                            num_ork += 1
                            #увеличиваем номер орка, т.к. в этих координатах находится кнопка следующий
                            if num_ork > len(orks) - 1:
								#если номер орка больше чем максимальный индекс списка
                                num_ork = 0
                                #устанавливаем номер орка = 0
                            start(num_ork)
                            #перерисовываем экран
                    if pygame.mouse.get_pos()[0] > 260 and pygame.mouse.get_pos()[
                            0] < 498:
								#проверка на координаты точки по х
                        if pygame.mouse.get_pos()[1] > 170 and pygame.mouse.get_pos()[
                                1] < 225:
									#проверка на координаты точки по у
                            but_cl()
                            #воспроизводим звук нажатия на мышь
                            num_ork -= 1
                            #уменьшаем номер орка, т.к. в этих координатах находится кнопка предыдущий
                            if num_ork < 0:
								#если номер орка меньше чем 0
                                num_ork = 3
                                #устанавливаем номер орка = 3
                            start(num_ork)
                            #перерисовываем экран
            start(num_ork)
            #обновляем экран
            draw_cursor(screen, pygame.mouse.get_pos())
            #рисуем наш курсор
            pygame.display.flip()

    pygame.quit()

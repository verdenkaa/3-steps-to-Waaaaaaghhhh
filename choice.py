import pygame
import os
import pygame as pg
import sys

class choice_sprite(pygame.sprite.Sprite):
    def __init__(self, name, image_s_x, image_s_y, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((center_x, center_y))
        self.image = load_image2(name, image_s_x, image_s_y)
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)


def load_image2(name, h, w, colorkey=None):
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

def start(num_ork, num_snarad):
    global orks
    global snarad
    all_sprites = pygame.sprite.Group()
    menu = choice_sprite('fon.jpg', 500, 500, 250, 250)
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

    font_comp = pygame.font.Font(None, 50)
    text_comp = font_comp.render("Ваш снаряд:", True, (255, 0, 0))
    text_comp_w = text_comp.get_width() #242
    text_comp_h = text_comp.get_height() #35
    screen.blit(text_comp, (0, 300))
    pygame.draw.rect(screen, (255, 0, 0), (0, 300 - 10,
                                           260, text_comp_h + 20), 1)

    ork = load_ork(f'{orks[num_ork]}/Body.png')
    f = open('player_ork.txt', 'w')
    f.write(orks[num_ork])
    f.close()
    ork = pygame.transform.scale(ork, (60, 100))
    screen.blit(ork, (70, 130))
    pygame.display.update()

    snar = load_ork(snarad[num_snarad] + '.png')
    f = open('player_snar.txt', 'w')
    f.write(snarad[num_snarad])
    f.close()
    snar = pygame.transform.scale(snar, (50, 30))
    screen.blit(snar, (70, 400))
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3-step to Waagh! Choose your Orks!')

    orks = ['Nob', 'Flash', 'Tank', 'Meh']
    snarad = ['bolt']

    pg.mixer.music.load('Sounds/doom_02. Rip & Tear.mp3')
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.25)

    start(0, 0)

    fps = 120
    clock = pygame.time.Clock()
    clock.tick(fps)

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        num_ork = 0
        num_snarad = 0

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] > 260 and pygame.mouse.get_pos()[0] < 498:
                        if pygame.mouse.get_pos()[1] > 80 and pygame.mouse.get_pos()[1] < 135:
                            but_cl()
                            num_ork += 1
                            if num_ork > len(orks) - 1:
                                num_ork = 0
                            start(num_ork, num_snarad)
                            pygame.display.update()
                    if pygame.mouse.get_pos()[0] > 260 and pygame.mouse.get_pos()[0] < 498:
                        if pygame.mouse.get_pos()[1] > 170 and pygame.mouse.get_pos()[1] < 225:
                            but_cl()
                            num_ork -= 1
                            if num_ork < 0:
                                num_ork = 3
                            start(num_ork, num_snarad)
                            pygame.display.update()

    pygame.quit()
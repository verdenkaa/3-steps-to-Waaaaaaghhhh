import pygame
import os
import sys
import math
import random

def load_image(name, h, w, colorkey=None):
    image = pygame.image.load(f"Sprites/{name}")
    image = pygame.transform.scale(image, (h, w))
    return image

def intround(x, left, right):
    if x > right:
        return right
    elif x < left:
        return left
    else:
        return x



class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("Sprites/Ork-Body.png")
        #self.image = pygame.transform.scale(self.image, (150, 150))
        self.shooting = False
        self.image = load_image("Ork-Body.png", 150, 150)
        self.rect = self.image.get_rect()
        self.position = (500 / 2, 500 / 2)
        self.rect.center = self.position
        self.image2 = load_image("Ork-Legs.png", 100, 70)
        self.rect2 = self.image.get_rect()
        self.rect2.center = self.position[0] + 5, self.position[1] + 100
        self.rot_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.cadr = 0


    def update(self):
        screen.blit(self.image2, self.rect2)
        mouse_pos = pygame.mouse.get_pos()
        rx, ry = self.rect.center
        angle = math.degrees(math.atan2(ry - mouse_pos[1],
                                    mouse_pos[0] - rx))
        if abs(angle) <= 60 and abs(angle) >= 0:
            self.rot_image = pygame.transform.rotate(self.image, angle)
        rot_image_rect = self.rot_image.get_rect(center = self.rect.center)
        rot_image_rect.y += int(-0.5 * intround(angle, -60, 60))
        rot_image_rect.x += int(-0.5 * intround(angle, -60, 60))
        #if not pygame.sprite.collide_mask(self, floor):
            #self.rect = self.rect.move(0, 1)
            #self.rect2 = self.rect2.move(0, 1)
        screen.blit(self.rot_image, rot_image_rect.topleft)
        print(self.cadr)
        if self.shooting and self.cadr > 5:
            Bolt(rx, ry, mouse_pos[0], mouse_pos[1], angle)
            self.cadr = 0
        else:
            self.cadr += 1

class Floor(pygame.sprite.Sprite):
    image = load_image("floor.jpg", 1000, 50)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height


class Bolt(pygame.sprite.Sprite):
    image = load_image("bolt.png", 30, 10)

    def __init__(self, x, y, x2, y2, angle):
        super().__init__(all_sprites)
        self.x2 = x2 - 150
        self.y2 = y2 - 170
        self.angle = angle
        self.image = Bolt.image
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = 1

        
    def update(self):
        self.rect = self.rect.move(self.x2 // 100 * self.i, self.y2 // 100 * self.i)
        self.i += 1

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("WAAAAAAAAGHHHH!!!")
    all_sprites = pygame.sprite.Group()
    player = Player()
    floor = Floor()
    #legs = Legs()
    #all_sprites.add(floor)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.shooting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                player.shooting = False
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_SPACE:
                    #player.jump()
                    #print(12)

        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        player.update()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
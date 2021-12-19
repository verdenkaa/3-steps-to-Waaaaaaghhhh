import pygame
import os
import sys
import math

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
        self.image = load_image("Ork-Body.png", 150, 150)
        self.rect = self.image.get_rect()
        self.position = (500 / 2, 500 / 2)
        self.rect.center = self.position
        self.image2 = load_image("Ork-Legs.png", 100, 70)
        self.rect2 = self.image.get_rect()
        self.rect2.center = self.position[0] + 5, self.position[1] + 100
        self.rot_image = self.image

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
        screen.blit(self.rot_image, rot_image_rect.topleft)
        #print(angle)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("WAAAAAAAAGHHHH!!!")
    all_sprites = pygame.sprite.Group()
    player = Player()
    #legs = Legs()
    #all_sprites.add(legs)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        #all_sprites.update()
        #all_sprites.draw(screen)
        player.update()
        pygame.display.flip()
    pygame.quit()
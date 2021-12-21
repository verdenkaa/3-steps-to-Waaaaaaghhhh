import pygame
import math
import random
import pygame as pg

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



class Nobz(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shooting = False
        self.go = False
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
        self.fly = False
        self.ammo = 30
        self.trat = 1
        self.dakka = False

        self.f = pygame.font.Font(None, 40)
        
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

        if not pygame.sprite.collide_mask(self, floor):
            self.rect = self.rect.move(0, 7)
            self.rect2 = self.rect2.move(0, 7)

        self.textR = self.f.render(str(round(self.ammo)), False, (255, 0, 0))
        self.text = self.textR.get_rect()
        self.text.center = (40, 40)
        screen.blit(self.textR, self.text)

        screen.blit(self.rot_image, rot_image_rect.topleft)
        #print(mouse_pos[0], self.rect.center[1])
        if (self.shooting and self.cadr > 5 and (abs(angle) <= 60 and abs(angle) >= 0) and self.ammo > self.trat) or (self.dakka and self.shooting and self.cadr > 1):
            Bolt(rx, ry, mouse_pos[0], mouse_pos[1], angle)
            self.cadr = 0
            self.ammo -= self.trat
        elif self.cadr > 5:
            self.cadr = 5
            if self.ammo < 30 and self.cadr >= 5:
                self.ammo += 0.2
        else:
            self.cadr += 1

        if self.go:
            self.rect = self.rect.move(self.go, 0)
            self.rect2 = self.rect2.move(self.go, 0)

        if self.fly:
            self.rect = self.rect.move(0, self.fly)
            self.rect2 = self.rect2.move(0, self.fly)
            fly.play()
            

class Floor(pygame.sprite.Sprite):
    image = load_image("floor.jpg", 1000, 50)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Bolt(pygame.sprite.Sprite):
    image = load_image("bolt.png", 30, 10)

    def __init__(self, x, y, x2, y2, angle):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.angle = angle
        self.image = Bolt.image
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #self.rect = self.rect.move(self.x2 - self.x, self.y2 - self.y)
        #self.rect.x = x
        #self.rect.y = y
        #print(x, y)
        self.i = 1
        bolter.play()

        
    def update(self):
        if self.i == 300:
            return False
        #print(self.x2, self.y2)
        self.rect = self.rect.move((self.x2 - self.x) // 20, (self.y2 - self.y) // 20)
        #pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x2, self.y2))
        self.i += 1

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("WAAAAAAAAGHHHH!!!")
    all_sprites = pygame.sprite.Group()
    Nobz = Nobz()
    floor = Floor()
    all_sprites.add(floor)
    bolter = pg.mixer.Sound('Sounds/boltshoot2.wav')
    fly = pg.mixer.Sound('Sounds/fly.mp3')
    NoDakka = pygame.USEREVENT + 0
    pygame.font.init()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Nobz.shooting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                Nobz.shooting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    Nobz.go = 4
                elif event.key == pygame.K_a:
                    Nobz.go = -4
                elif event.key == pygame.K_SPACE:
                    Nobz.fly = -10
                elif event.key == pygame.K_e:
                    Nobz.dakka = True
                    Nobz.trat = 0
                    pygame.time.set_timer(NoDakka, 3000)
            
            if event.type == NoDakka:
                Nobz.dakka = False
                Nobz.trat = 1
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    Nobz.go = 0
                elif event.key == pygame.K_a:
                    Nobz.go = 0
                elif event.key == pygame.K_SPACE:
                    Nobz.fly = False

        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        Nobz.update()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()

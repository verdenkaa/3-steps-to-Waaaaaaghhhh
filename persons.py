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



class Player():
    
    def __init__(self, patron, person, Bx, By, Lx, Ly, ammo, maxammo, legsmove=100):
        #pygame.sprite.Sprite.__init__(self)
        self.shooting = False
        self.go = False
        self.image = load_image(f"/{person}/Body.png", Bx, By)
        self.rect = self.image.get_rect()
        self.position = (500 / 2, 500 / 2)
        self.rect.center = self.position
        self.image2 = load_image(f"/{person}/Legs.png", Lx, Ly)
        self.rect2 = self.image.get_rect()
        self.rect2.center = self.position[0] + 5, self.position[1] + legsmove
        self.rot_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.cadr = 0
        self.fly = False
        self.ammo = ammo
        self.maxammo = maxammo
        self.trat = 1
        self.dakka = False
        self.f = pygame.font.Font(None, 40)
        self.patron = patron
        self.soundShoot1 = pg.mixer.Sound('Sounds/boltshoot.mp3')
        self.plusammo = 0.5
        self.cadrtoshoot = 5
        self.todakka = 0
        self.t = True
        self.timer = 200
        
    def load_image(name, h, w, colorkey=None):
        image = pygame.image.load(f"Sprites/{name}")
        image = pygame.transform.scale(image, (h, w))
        return image

    def intround(self, x, left, right):
        #print(x, left, right)
        if x > right:
            return abs(right)
        elif x < left:
            return abs(left)
        else:
            return x

    def goFunc(self):
        self.rect = self.rect.move(self.go, 0)
        self.rect2 = self.rect2.move(self.go, 0)

    def flyFunc(self):
        self.rect = self.rect.move(0, self.fly)
        self.rect2 = self.rect2.move(0, self.fly)
        fly.play()

    def shootFunc(self, rx, ry, mouse_pos0, mouse_pos1, angle):
        self.patron(rx, ry, mouse_pos0, mouse_pos1, angle, self.soundShoot1)
        self.cadr = 0
        self.ammo -= self.trat
        if self.dakka and self.ammo < 30:
            self.ammo += self.plusammo


    def update(self):
        screen.blit(self.image2, self.rect2)
        mouse_pos = pygame.mouse.get_pos()
        rx, ry = self.rect.center

        angle = math.degrees(math.atan2(ry - mouse_pos[1],
                                    mouse_pos[0] - rx))

        if -50 <= angle <= 60:
            self.rot_image = pygame.transform.rotate(self.image, angle)

        rot_image_rect = self.rot_image.get_rect(center = self.rect.center)
        #print(intround(angle, -60, 60))
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
        
        if self.dakka and self.t:
                dk = pg.mixer.Sound(f'Sounds/Dakka/{random.randint(1, 7)}.mp3')
                dk.play()
                self.t = False
        elif not(self.dakka or self.t):
            self.t = True
        
        if (self.dakka  and self.cadr > self.cadrtoshoot // 2 and (-50 <= angle <= 60)) or (self.shooting and self.cadr > self.cadrtoshoot and (-50 <= angle <= 60) and self.ammo > self.trat):
            self.shootFunc(rx, ry, mouse_pos[0], mouse_pos[1], angle)
        elif self.cadr > self.cadrtoshoot:
            self.cadr = self.cadrtoshoot
            if self.ammo < self.maxammo and self.cadr >= self.cadrtoshoot:
                self.ammo += self.plusammo
        else:
            self.cadr += 1

        if self.go:
            self.goFunc()

        if self.fly:
            self.flyFunc()


        
            

class Nobz(Player):

    def __init__(self, patron):
        super().__init__(patron, "Nob", 150, 150, 100, 70, 20, 20)
        self.ammo = 20
        self.maxammo = 20


class Flash(Player):

    def __init__(self, patron):
        super().__init__(patron, "Flash", 170, 170, 130, 100, 60, 60, legsmove=70)
        self.plusammo = 0.2
        self.trat = 2

    def shootFunc(self, rx, ry, mouse_pos0, mouse_pos1, angle):
        self.patron(rx, ry, mouse_pos0, mouse_pos1, angle, self.soundShoot1)
        self.patron(rx, ry + random.randint(-40, 40), mouse_pos0, mouse_pos1 + random.randint(-40, 40), angle, self.soundShoot1)
        self.cadr = 0
        self.ammo -= self.trat
        if self.dakka and self.ammo < 60:
            self.ammo += self.plusammo

    
class Tank(Player):

    def __init__(self, patron):
        super().__init__(patron, "Tank", 150, 150, 100, 120, 30, 30, legsmove=30)
        self.ammo = 5
        self.maxammo = 5
        self.plusammo = 0.05
        self.cadrtoshoot = 30
        self.soundShoot1 = pg.mixer.Sound('Sounds/zap.mp3')


class Meh(Player):

    def __init__(self, patron):
        super().__init__(patron, "Meh", 180, 150, 100, 120, 30, 30, legsmove=50)
        self.ammo = 12
        self.maxammo = 12
        self.plusammo = 0.05
        self.cadrtoshoot = 20
        self.soundShoot1 = pg.mixer.Sound('Sounds/blast.mp3')


class Snarad(pygame.sprite.Sprite):
    

    def __init__(self, x, y, x2, y2, angle, sound, dlin, shir, speed, im="bolt.png"):
        super().__init__(all_sprites)
        self.im = im
        image = load_image(self.im, dlin, shir)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.angle = angle
        self.image = image
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #self.rect = self.rect.move(self.x2 - self.x, self.y2 - self.y)
        #self.rect.x = x
        #self.rect.y = y
        #print(x, y)
        self.i = 1
        self.speed = 10
        sound.set_volume(0.5)
        sound.play()

        
    def update(self):
        if self.i == 300:
            return None
        self.rect = self.rect.move((self.x2 - self.x) // self.speed, (self.y2 - self.y) // self.speed)
        #pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x2, self.y2))
        self.i += 1


class Bolt(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 30, 10, 20, "bolt.png")
        self.speed = 10
        
class Zap(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound, ):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 40, 10, 25, "zap.png")
        self.speed = 5

class Blast(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound, ):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 25, 20, 100, "blast.png")
        self.speed = 30

class MiniBolt(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 20, 7, 20, "bolt.png")
        self.speed = 8

class Floor(pygame.sprite.Sprite):
    image = load_image("floor.jpg", 1000, 50)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("WAAAAAAAAGHHHH!!!")
    all_sprites = pygame.sprite.Group()
    Nobz = Meh(Blast)
    floor = Floor()
    all_sprites.add(floor)
    bolter = pg.mixer.Sound('Sounds/boltshoot2.wav')
    fly = pg.mixer.Sound('Sounds/fly.mp3')
    NoDakka = pygame.USEREVENT + 0
    CanUseDakka = pygame.USEREVENT + 0
    CanDakka = True
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
                elif event.key == pygame.K_e and not(Nobz.dakka):
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

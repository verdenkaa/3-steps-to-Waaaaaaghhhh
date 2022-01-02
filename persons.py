import pygame
import math
import random
import pygame as pg
import sys

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
        self.position = 100, 500
        self.image = load_image(f"/{person}/Body.png", Bx, By)
        self.rect = self.image.get_rect()
        self.mobs = set(['<Spore Sprite(in 1 groups)>', '<Ground1 Sprite(in 1 groups)>', '<Ground2 Sprite(in 1 groups)>', '<FlyEnemy Sprite(in 1 groups)>', '<Bio Sprite(in 1 groups)>'])
        self.rect.center = self.position[0] + 5, self.position[1] + legsmove
        self.healthImage = load_image("Health.png", 40, 40)
        
        self.rect.center = self.position
        self.image2 = load_image(f"/{person}/Legs.png", Lx, Ly)
        self.rect2 = self.image.get_rect()
        self.rect2.center = self.position[0] + 5, self.position[1] + legsmove
        self.rot_image = self.image
        #self.mask = pygame.mask.from_surface(self.image)
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
        self.health = 10
        
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
        all_sprites.add(self.patron(rx, ry, mouse_pos0, mouse_pos1, angle, self.soundShoot1))
        self.cadr = 0
        self.ammo -= self.trat
        if self.dakka and self.ammo < 30:
            self.ammo += self.plusammo


    
    def update(self):
        global end
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

        if not(pygame.sprite.collide_mask(self, floor)) and not(pygame.sprite.collide_mask(self, bunker)) and not(pygame.sprite.collide_mask(self, bunker2)):
            self.rect = self.rect.move(0, 7)
            self.rect2 = self.rect2.move(0, 7)

        self.textR = self.f.render(str(round(self.ammo)), False, (255, 0, 0))
        self.text = self.textR.get_rect()
        self.text.center = (40, 40)
        screen.blit(self.textR, self.text)

        screen.blit(self.rot_image, rot_image_rect.topleft)
        
        if self.dakka and self.t:
                dk = pg.mixer.Sound(f'Sounds/Dakka/{random.randint(1, 7)}.mp3')
                dk.set_volume(0.4)
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

        if self.go and not(self.dakka):
            self.goFunc()

        if self.fly and not(self.dakka):
            self.flyFunc()
        sprites = pygame.sprite.spritecollide(self, all_sprites, False)
        sp = set(map(str, sprites))
        #print(sp)
        
        if self.mobs & sp:
            self.health -= 1

        if self.health < 1:
            self.fLose = pygame.font.Font(None, 120)
            self.textRLose = self.fLose.render("Харошый пастук  был!", False, (255, 0, 0))
            self.textLose = self.textRLose.get_rect()
            self.textLose.center = (600, 400)
            screen.blit(self.textRLose, self.textLose)
            end = True
            #pygame.time.delay(20000)
            #sys.exit()
        else:
            x, y = 1240, 40
            Hrect = self.healthImage.get_rect()

            for _ in range(self.health):
                Hrect.center = x, y
                screen.blit(self.healthImage, Hrect)
                x -= 40


        
            

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
        self.health = 6

    def shootFunc(self, rx, ry, mouse_pos0, mouse_pos1, angle):
        all_sprites.add(self.patron(rx, ry, mouse_pos0, mouse_pos1, angle, self.soundShoot1))
        all_sprites.add(self.patron(rx, ry + random.randint(-40, 40), mouse_pos0, mouse_pos1 + random.randint(-40, 40), angle, self.soundShoot1))
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
        self.health = 2
        self.soundShoot1 = pg.mixer.Sound('Sounds/zap.mp3')


class Meh(Player):

    def __init__(self, patron):
        super().__init__(patron, "Meh", 180, 150, 100, 120, 30, 30, legsmove=50)
        self.ammo = 12
        self.maxammo = 12
        self.plusammo = 0.05
        self.cadrtoshoot = 20
        self.health = 8
        self.soundShoot1 = pg.mixer.Sound('Sounds/blast.mp3')


class Snarad(pygame.sprite.Sprite):
    

    def __init__(self, x, y, x2, y2, angle, sound, dlin, shir, im="bolt.png"):
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
        self.i = 1
        self.speed = 10
        sound.set_volume(0.2)
        sound.play()
        self.mobs = set(['<Spore Sprite(in 1 groups)>', '<Ground1 Sprite(in 1 groups)>', '<Floor Sprite(in 1 groups)>', '<Ground2 Sprite(in 1 groups)>'])

        
    def update(self):
        if pygame.sprite.collide_mask(self, bunker) or pygame.sprite.collide_mask(self, bunker2):
            self.kill()
        sp = set(map(str, pygame.sprite.spritecollide(self, all_sprites, False)))
        if self.mobs & sp:
            self.kill()
        if self.i > 70:
            self.kill()
        self.rect = self.rect.move((self.x2 - self.x) // self.speed, (self.y2 - self.y) // self.speed)
        #pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x2, self.y2))
        self.i += 1



class Bolt(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 30, 10, "bolt.png")
        self.speed = 10

   
class Zap(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound, ):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 40, 10, "zap.png")
        self.speed = 5
        self.mobs = set()


class Blast(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound, ):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 25, 20, "blast.png")
        self.speed = 30


class MiniBolt(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 20, 7, "bolt.png")
        self.speed = 8


class Bio(Snarad):

    def __init__(self, rx, ry, mouse_pos0, mouse_pos1, angle, sound):
        super().__init__(rx, ry, mouse_pos0, mouse_pos1, angle, sound, 20, 20, "bio.png")
        self.speed = 40
        self.mobs = set(['<Bunker Sprite(in 1 groups)>', '<Bunker2 Sprite(in 1 groups)>'])
    

    def update(self):
        if pygame.sprite.collide_mask(self, bunker) or pygame.sprite.collide_mask(self, bunker2):
            self.kill()
        sp = set(map(str, pygame.sprite.spritecollide(self, all_sprites, False)))
        if self.mobs & sp:
            bunker.Health -= 1
            self.kill()
        if self.i > 70:
            self.kill()
        self.rect = self.rect.move((self.x2 - self.x) // self.speed, (self.y2 - self.y) // self.speed)
        self.i += 1

class Floor(pygame.sprite.Sprite):
    image = load_image("floor.png", 1280, 50)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Bunker(pygame.sprite.Sprite):
    image = load_image("bunker.png", 300, 300)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Bunker.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height - 40
        self.rect.x += 30
        self.Health = 100
        self.f = pygame.font.Font(None, 40)

    def update(self):
        global end
        self.textR = self.f.render(str(round(self.Health)), False, (50, 200, 0))
        self.text = self.textR.get_rect()
        self.text.center = (100, 40)
        screen.blit(self.textR, self.text)
        if self.Health < 1:
            end = True
            self.fLose = pygame.font.Font(None, 120)
            self.textRLose = self.fLose.render("Вот аблом!", False, (255, 0, 0))
            self.textLose = self.textRLose.get_rect()
            self.textLose.center = (700, 400)
            screen.blit(self.textRLose, self.textLose)

class Bunker2(pygame.sprite.Sprite):
    image = load_image("bunker.png", 300, 300)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Bunker2.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height - 340
        self.rect.x += 30


class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        super().__init__(all_sprites)
        self.image = load_image(name, x, y)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = 1200, 700
        self.move = -3
        self.damage = 5
        self.health = 1
        self.dead = False
        self.t = False
        self.sounddead = pg.mixer.Sound('Sounds/Dead.mp3')
        self.sounddead.set_volume(0.2)
        self.points = 1
        

    def update(self):
        global score
        if self.dead:
            if self.dead != True:
                self.image = load_image(f"Tyranids/Dead/{self.dead // 3}.png", self.x, self.y)
                if self.dead < 21:
                    self.dead += 1
                else:
                    self.kill()
        else:
            self.rect = self.rect.move(self.move, 0)
            sp = tuple(map(str, pygame.sprite.spritecollide(self, all_sprites, False)))
            if '<Bolt Sprite(in 1 groups)>' in sp:
                self.health -= 1
            elif '<MiniBolt Sprite(in 1 groups)>' in sp:
                self.health -= 1
            elif '<Zap Sprite(in 1 groups)>' in sp:
                self.health -= 10
            elif '<Blast Sprite(in 1 groups)>' in sp:
                self.health -= 5

            if self.health < 1:
                self.move = 0
                score += self.points
                #self.image = load_image("Tyranids/Dead/1.png", self.x, self.y)
                if not self.dead:
                    self.sounddead.play()
                    self.dead = 3

            if self.rect.x <= 320:
                bunker.Health -= self.damage
                self.kill()


class Spore(Enemy):

    def __init__(self):
        super().__init__(f"Tyranids/Spore{random.randint(1, 3)}.png", 30, 70)
        self.move = -2
        self.rect.center = 1400, 650


class Ground1(Enemy):

    def __init__(self):
        super().__init__(f"Tyranids/Ground1.png", 130, 100)
        self.move = -3
        self.rect.center = 1400, 630
        self.health = 2
        self.points = 2


class Ground2(Enemy):

    def __init__(self):
        super().__init__(f"Tyranids/Ground2.png", 250, 150)
        self.move = -1
        self.rect.center = 1400, 605
        self.health = 5
        self.damage = 10
        self.points = 3


class FlyEnemy(Enemy):
    def __init__(self):
        super().__init__(f"Tyranids/Fly.png", 150, 150)
        self.health = 3
        self.rect.center = 1300, random.randint(200, 300)
        self.toammo = 0
        self.health = 2
        self.sound = pg.mixer.Sound(f'Sounds/bio.mp3')
        self.sound.set_volume(0.3)
        self.ponts = 4

    def update(self):
        if self.dead:
            if self.dead != True:
                self.image = load_image(f"Tyranids/Dead/{self.dead // 3}.png", self.x, self.y)
                self.rect = self.rect.move(0, 2)
                if self.dead < 21:
                    self.dead += 1
                else:
                    self.kill()
        else:
            self.rect = self.rect.move(self.move, 0)
            sp = tuple(map(str, pygame.sprite.spritecollide(self, all_sprites, False)))
            if '<Bolt Sprite(in 1 groups)>' in sp:
                self.health -= 1
            elif '<MiniBolt Sprite(in 1 groups)>' in sp:
                self.health -= 1
            elif '<Zap Sprite(in 1 groups)>' in sp:
                self.health -= 10
            elif '<Blast Sprite(in 1 groups)>' in sp:
                self.health -= 5

            if self.health < 1:
                self.move = 0
                #self.image = load_image("Tyranids/Dead/1.png", self.x, self.y)
                if not self.dead:
                    self.sounddead.play()
                    self.dead = 3

            if self.rect.x < 370:
                self.move = 0

            if self.toammo >= 80:
                self.toammo = 0
                angle = math.degrees(math.atan2(self.rect.x - Gamer.rect.x,
                                    self.rect.y - Gamer.rect.y))
                all_sprites.add(Bio(self.rect.x + 50, self.rect.y + 80, Gamer.rect2.x, Gamer.rect2.y, angle, self.sound))
            else:
                self.toammo += 1
                


if __name__ == '__main__':
    pygame.init()
    pg.mixer.music.load('Sounds/Theme.mp3')
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.3)
    image = pygame.image.load("Sprites/fon2.png")
    clock = pygame.time.Clock()
    size = width, height = 1280, 720
    image = pygame.transform.scale(image, size)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("WAAAAAAAAGHHHH!!!")
    all_sprites = pygame.sprite.Group()
    bosssound = pg.mixer.Sound('Sounds/BossWalk.mp3')
    bosssound.set_volume(0.6)
    gamephaz = 1
    end = False
    score = 0
    f = pygame.font.Font(None, 60)
    textR = f.render(str(round(score)), False, (200, 200, 200))
    text = textR.get_rect()
    text.center = (640, 40)

    ork_pl = open('player_ork.txt', 'r').readlines()[0]
    if ork_pl == 'Nob':
        Gamer = Nobz(Bolt)
    elif ork_pl == 'Flash':
        Gamer = Flash(MiniBolt)
    elif ork_pl == 'Tank':
        Gamer = Tank(Zap)
    elif ork_pl == 'Meh':
        Gamer = Meh(Blast)


    floor = Floor()
    bunker = Bunker()
    bunker2 = Bunker2()
    #Spor = Spore()
    all_sprites.add(floor, bunker, bunker2)
    fly = pg.mixer.Sound('Sounds/fly.mp3')
    NoDakka = pygame.USEREVENT + 0
    CanUseDakka = pygame.USEREVENT + 0
    CanDakka = True
    pygame.font.init()
    time = 1
    running = True
    while running:
        #print(clock.get_fps())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Gamer.shooting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                Gamer.shooting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    Gamer.go = 6
                elif event.key == pygame.K_a:
                    Gamer.go = -6
                elif event.key == pygame.K_SPACE:
                    Gamer.fly = -15
                elif event.key == pygame.K_e and not(Gamer.dakka):
                    Gamer.dakka = True
                    Gamer.trat = 0
                    pygame.time.set_timer(NoDakka, 3000)
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

            
            if event.type == NoDakka:
                Gamer.dakka = False
                Gamer.trat = 1
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    Gamer.go = 0
                elif event.key == pygame.K_a:
                    Gamer.go = 0
                elif event.key == pygame.K_SPACE:
                    Gamer.fly = False

        if time % 100 == 0:
            all_sprites.add(Spore())
        if time % 150 == 0:
            all_sprites.add(Ground1())
        if time % 300 == 0:
            all_sprites.add(Ground2())
        if time % 500 == 0:
            all_sprites.add(FlyEnemy())
        if time % 3000 == 0:
            if gamephaz == 1:
                gamephaz = 2
            elif gamephaz == 2:
                gamephaz = 5
            else:
                gamephaz = 10
            bosssound.play()
        time += gamephaz

        screen.blit(image, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        Gamer.update()

        textR = f.render(str(round(score)), False, (200, 200, 200))
        text = textR.get_rect()
        text.center = (640, 40)

        screen.blit(textR, text)
        pygame.display.flip()
        if end:
            pygame.time.delay(1500)
            sys.exit()
        clock.tick(50)
    pygame.quit()

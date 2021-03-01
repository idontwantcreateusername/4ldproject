import os
import sys
from math import atan, cos, sin, sqrt
import pygame
from pygame import sprite

bullets = pygame.sprite.Group


class Kitchen(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        sprite.Sprite.__init__(self)
        self.image = load_image("kitchen.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Hpscale(sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        sprite.Sprite.__init__(self)
        self.image = load_image("healscale.png")
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 1020
        self.hp = []
        c = 1
        for i in range(7):
            q = pygame.sprite.Sprite()
            q.image = load_image('healpoint.png')
            q.rect = q.image.get_rect()
            q.rect.x = 8 * c + self.rect.x + 56 * (c - 1)
            q.rect.y = self.rect.y + 8
            c += 1
            self.hp.append(q)


class Ct(sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        sprite.Sprite.__init__(self)
        self.image = load_image("t.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, text):
        self.font = pygame.font.SysFont("Arial", 15)
        self.textSurf = self.font.render(text, 1, (255, 255, 255))
        self.image.blit(self.textSurf, [817, 104])


class Dialog(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        sprite.Sprite.__init__(self)
        self.image = load_image("dialog.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def fill(self, text):
        if text == '':
            self.image = load_image('void.png')
        else:
            self.image = load_image("dialog.png")
            self.font = pygame.font.SysFont("Arial", 15)
            self.textSurf = self.font.render(text, 1, (255, 255, 255))
            self.image.blit(self.textSurf, [84, 812])


class Tent(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.opened = False
        self.image = load_image('tent.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.filled = True

    def open(self):
        self.opened = not self.opened
        if self.opened:
            self.image = load_image('tent_open.png')
            if self.filled:
                self.image = load_image('tent_eq.png')
        else:
            self.image = load_image('tent.png')

    def take(self):
        if self.filled:
            self.image = load_image('tent_open.png')
            self.filled = False


class Target(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image('target.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.counter = 0

    def harm(self):
        print('you did it')
        self.counter += 1
        print(self.counter)


class Border(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5977, 1754))
        self.image = load_image("border.png")
        self.rect = pygame.Rect(x, y, 5977, 1754)
        self.mask = pygame.mask.from_surface(self.image)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Hero1(sprite.Sprite):
    def __init__(self, x, y, n, reved, armor, wtype, weapon='default', *group):
        super().__init__(*group)
        self.up = False
        self.left = False
        self.reved = reved
        self.image = load_image(n + reved + '.png')
        self.name = n
        self.right = False
        self.down = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.wt = wtype
        self.rect.y = y
        self.reloading = False
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 7
        self.weapon = Weapon(self, wtype, weapon, '')
        self.righth = RightHand(self)
        self.lefth = LeftHand(self)
        self.armor = Armor(self, armor)
        self.st = 0

        self.disarmed = False

    def harm(self):
        self.hp -= 1
        print('ouch')

    def update(self, ac, time, startreloadingtime, border):

        if self.up:
            self.rect.y -= 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.y += 5
        if self.left:
            self.rect.x -= 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.x += 5
        if self.down:
            self.rect.y += 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.y -= 5
        if self.right:
            self.rect.x += 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.x -= 5
        if self.hp == 0:
            a = 0
        self.righth.update(self)
        self.lefth.update(self)
        self.armor.update(self)
        self.weapon.update(self)
        if self.up or self.left or self.right or self.down:
            self.image = load_image(self.name + str(ac // 4 + 1) + self.reved + '.png')
        else:
            self.image = load_image(self.name + self.reved + '.png')
        if self.reloading:

            if self.weapon.name[:5] == 'rifle':
                if ac > 14:
                    self.weapon.image = load_image('reloading' + str((ac - 14) // 7 + 1) + self.reved + '.png')
                else:
                    self.weapon.image = load_image('reloading' + str((ac - 1) // 7 + 1) + self.reved + '.png')
                self.lefth.image = load_image('void.png')
                self.righth.image = load_image('void.png')
                if time - startreloadingtime > 224:
                    self.reloading = False
                    self.weapon.condition = ''
            if self.weapon.name[:5] == 'cross':
                if time - startreloadingtime <= 14:
                    self.weapon.image = load_image(self.weapon.name + 'shooted' + self.reved + '.png')
                    self.righth.image = load_image(self.name[0] + self.weapon.name[:5] + self.reved + 'right1.png')
                else:
                    self.weapon.image = load_image(self.weapon.name + self.reved + '.png')
                    self.righth.image = load_image(self.name[0] + self.weapon.name[:5] + self.reved + 'right2.png')
                if time - startreloadingtime >= 26:
                    self.reloading = False
                    if self.weapon.name == 'crossbow':
                        self.weapon.crosscondition = ''
                    else:
                        self.weapon.condition = ''


class Npc(sprite.Sprite):
    def __init__(self, x, y, n, reved, armor, wtype, weapon='default', *group):
        super().__init__(*group)
        self.up = False
        self.left = False
        self.st = 0
        self.reved = reved
        self.image = load_image(n + reved + '.png')
        self.name = n
        self.right = False
        self.down = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.go = False
        self.weapon = weapon
        self.reloading = False
        self.follo = False
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 7
        self.weapon = Weapon(self, wtype, weapon, '')
        self.righth = RightHand(self)
        self.lefth = LeftHand(self)
        self.armor = Armor(self, armor)
        self.disarmed = False
        self.startreloadingtime = self.st

    def follow(self, hero):
        trip = True
        target_x = hero.rect.x - 300
        target_y = hero.rect.y
        target_x2 = hero.rect.x + 300
        if target_x < self.rect.x:
            dx = -1
            target_x = hero.rect.x + 300
            self.reved = 'reversed'
        elif target_x2 > self.rect.x:
            target_x = hero.rect.x - 300
            dx = 1
            self.reved = ''
        if target_y < self.rect.y:
            dy = -1
        else:
            dy = 1
        if target_y - 3 <= self.rect.y < target_y + 3 and target_x - 3 <= self.rect.x < target_x + 3:
            trip = False
            self.go = False

        if trip:
            self.go = True
            if target_x - 3 > self.rect.x or self.rect.x >= target_x + 3:
                self.rect.x = self.rect.x + 4 * dx

            if target_y - 3 > self.rect.y or self.rect.y > target_y + 3:
                self.rect.y = self.rect.y + 4 * dy

    def harm(self):
        self.hp -= 1
        # print(self.hp)

    def update(self, h, ac, time, border):
        if self.weapon.condition != '':
            self.reloading = True
        self.startreloadingtime = self.st
        if self.up:
            self.rect.y -= 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.y += 5
        if self.left:
            self.rect.x -= 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.x += 5
        if self.down:
            self.rect.y += 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.y -= 5
        if self.right:
            self.rect.x += 5
            if pygame.sprite.collide_mask(self, border):
                self.rect.x -= 5
        self.startreloadingtime = self.st
        if self.weapon.condition != '':
            self.reloading = True
        if self.follo:
            self.follow(h)
        self.righth.update(self)
        self.lefth.update(self)
        self.armor.update(self)
        self.weapon.update(self)
        if self.up or self.left or self.right or self.down or self.go:
            self.image = load_image(self.name + str(ac // 8 + 1) + self.reved + '.png')
        else:
            self.image = load_image(self.name + self.reved + '.png')
        if self.reloading:

            if self.weapon.name[:5] == 'rifle':
                if ac > 14:
                    self.weapon.image = load_image('reloading' + str((ac - 14) // 7 + 1) + self.reved + '.png')
                else:
                    self.weapon.image = load_image('reloading' + str((ac - 1) // 7 + 1) + self.reved + '.png')
                self.lefth.image = load_image('void.png')
                self.righth.image = load_image('void.png')
                if time - self.startreloadingtime > 224:
                    self.reloading = False
                    self.weapon.condition = ''
            if self.weapon.name[:5] == 'cross':
                if time - self.startreloadingtime <= 14:
                    self.weapon.image = load_image(self.weapon.name + 'shooted' + self.reved + '.png')
                    self.righth.image = load_image(self.name[0] + self.weapon.name[:5] + self.reved + 'right1.png')
                else:
                    self.weapon.image = load_image(self.weapon.name + self.reved + '.png')
                    self.righth.image = load_image(self.name[0] + self.weapon.name[:5] + self.reved + 'right2.png')
                if time - self.startreloadingtime >= 26:
                    self.reloading = False
                    if self.weapon.name == 'crossbow':
                        self.weapon.crosscondition = ''
                    else:
                        self.weapon.condition = ''


class Armor(sprite.Sprite):
    def __init__(self, hero, n, *group):
        super().__init__(*group)
        self.name = n
        self.image = load_image(n + hero.reved + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y

    def update(self, hero):
        self.image = load_image(self.name + hero.reved + '.png')
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y


class LeftHand(sprite.Sprite):
    def __init__(self, hero, *group):
        super().__init__(*group)
        self.image = load_image(hero.name[0] + hero.weapon.type + hero.reved + 'left.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, hero):
        self.image = load_image(hero.name[0] + hero.weapon.type + hero.reved + 'left.png')
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y


class RightHand(sprite.Sprite):
    def __init__(self, hero, *group):
        super().__init__(*group)
        self.image = load_image(hero.name[0] + hero.weapon.type + hero.reved + 'right.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, hero):
        self.image = load_image(hero.name[0] + hero.weapon.type + hero.reved + 'right.png')
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y


class Land(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5977, 1754))
        self.image.fill(pygame.Color(253, 236, 166))
        self.rect = pygame.Rect(x, y, 5977, 1754)


class Weapon(sprite.Sprite):
    def __init__(self, hero, type, name, condition, *group):
        super().__init__(*group)
        self.name = name
        self.rect = hero.rect
        self.type = type
        self.eldertype = type
        self.condition = condition
        self.crosscondition = condition
        self.image = load_image(name + self.condition + hero.reved + '.png')

    def update(self, hero):
        if hero.disarmed:
            self.image = load_image('void.png')
            self.type = 'default'
        elif hero.reloading:
            a = 0
        elif self.name == 'crossbow':
            self.image = load_image(self.name + self.crosscondition + hero.reved + '.png')
            self.type = self.eldertype
        else:
            self.image = load_image(self.name + self.condition + hero.reved + '.png')
            self.type = self.eldertype
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y

    def shoot(self, hero, targetx, targety, all_sprites, bullets, time):
        if not hero.reloading:
            if targetx < hero.rect.x:
                hero.reved = 'reversed'
            else:
                hero.reved = ''
            b = Bullet(hero, targetx, targety)
            all_sprites.add(b)
            if self.name == 'rifle':
                self.condition = 'shooted'
            else:
                self.crosscondition = 'shooted'
            bullets.append(b)
            hero.st = time + 5
            print('i shooted')
            if hero == Npc:
                hero.reloading = True

        # pygame.mixer.music.load(self.name + '.mp3')
        # pygame.mixer.music.play()
        # pygame.mixer.music.unload()


class Bullet(sprite.Sprite):
    def __init__(self, hero, targetx, targety, *group):
        super().__init__(*group)
        if hero.weapon.name[:5] == 'rifle':
            self.image = load_image('bullet.png')
        elif hero.weapon.name[:5] == 'cross':
            self.image = load_image('bolt.png')
        self.rect = self.image.get_rect()
        if hero.reved == "":
            self.rect.x = hero.rect.x + 350
            self.rect.y = hero.rect.y + 100
        else:
            self.rect.x = hero.rect.x - 150
            self.rect.y = hero.rect.y + 100

        print((targety - self.rect.x))
        print(targetx - self.rect.y)
        angle = atan((targety - self.rect.y) / (targetx - self.rect.x))
        if hero.reved != '':
            self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.rotate(self.image, -5)
        print(angle)
        self.vx = (targetx - self.rect.x) // 10
        self.vy = (targety - self.rect.y) // 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, targets):

        self.rect.x += self.vx
        self.rect.y += self.vy
        for i in targets:
            if pygame.sprite.collide_mask(self, i):
                i.harm()
                self.kill()
        if self.rect.x < -10 or self.rect.x > 8000 or self.rect.y < -10 or self.rect.y > 8000:
            self.kill()

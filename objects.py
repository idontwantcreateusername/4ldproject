import os
import sys
from math import atan, cos, sin, sqrt

import pygame
from pygame import sprite

bullets = pygame.sprite.Group


class Tent(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.opened = False
        self.image = load_image('tent.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def open(self):
        self.opened = not self.opened
        if self.opened:
            self.image = ''
            fill_tent(self)


class Target(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image('target.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Border(sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5977, 1754))
        self.image = load_image("border.png")
        self.rect = pygame.Rect(x, y, 5977, 1754)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Hero1(sprite.Sprite):
    def __init__(self, x, y, n, reved, weapon='default', *group):
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
        self.rect.y = y
        self.go = False
        self.weapon = weapon
        self.reloading = False

    def update(self):

        if self.up:
            self.rect.y -= 5
        if self.left:
            self.rect.x -= 5
        if self.down:
            self.rect.y += 5
        if self.right:
            self.rect.x += 5


class Npc(sprite.Sprite):
    def __init__(self, x, y, n, reved, weapon='default', *group):
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
        self.rect.y = y
        self.go = False
        self.weapon = weapon
        self.reloading = False
        self.follo = False

    def talk(self):
        a = 0

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

    def update(self, h):
        if self.follo:
            self.follow(h)


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
        self.image = load_image(hero.name[0] + hero.weapon + hero.reved + 'left.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y

    def update(self, hero):
        if hero.reloading:
            self.image = load_image('void.png')
        else:
            self.image = load_image(hero.name[0] + hero.weapon + hero.reved + 'left.png')
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y


class RightHand(sprite.Sprite):
    def __init__(self, hero, *group):
        super().__init__(*group)
        self.image = load_image(hero.name[0] + hero.weapon + hero.reved + 'right.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y

    def update(self, hero):
        if hero.reloading:
            self.image = load_image('void.png')
        else:
            self.image = load_image(hero.name[0] + hero.weapon + hero.reved + 'right.png')
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
        self.condition = condition
        self.image = load_image(name + self.condition + hero.reved + '.png')

    def update(self, hero, d):
        if d:
            self.image = load_image('void.png')
            hero.weapon = 'default'
        elif hero.reloading:
            a = 0
        else:
            self.image = load_image(self.name + self.condition + hero.reved + '.png')
            hero.weapon = self.type
        self.rect.x = hero.rect.x
        self.rect.y = hero.rect.y

    def shoot(self, hero, targetx, targety, all_sprites, bullets):
        b = Bullet(hero, targetx, targety)
        all_sprites.add(b)
        self.condition = 'shooted'
        bullets.append(b)
        if targetx < hero.rect.x:
            hero.reved = 'reversed'
        else:
            hero.reved = ''
        # pygame.mixer.music.load(self.name + '.mp3')
        # pygame.mixer.music.play()
        # pygame.mixer.music.unload()


class Bullet(sprite.Sprite):
    def __init__(self, hero, targetx, targety, *group):
        super().__init__(*group)
        self.image = load_image('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x + 150
        self.rect.y = hero.rect.y + 100
        angle = atan(targety - self.rect.y / targetx - self.rect.x)
        self.image = pygame.transform.rotate(self.image, angle)
        self.vx = (targetx - self.rect.x) // 10
        self.vy = (targety - self.rect.y) // 10

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy


def fill_tent(tent):
    a = 0

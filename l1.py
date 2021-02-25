import pygame
import sys
import os
from objects import *


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + 1920 / 2, -t + 1080 / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - 1920), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - 1080), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def upd(hero, lefthand, righthand, armor, weapon, ac):
    global startreloadingtime
    if hero.up or hero.left or hero.right or hero.down or hero.go:
        hero.image = load_image(hero.name + str(ac // 16 + 1) + hero.reved + '.png')
    else:
        hero.image = load_image(hero.name + hero.reved + '.png')

    if hero.reloading:
        if time - startreloadingtime > 224:
            hero.reloading = False
            weapon.condition = ''
        if weapon.name[:5] == 'rifle':
            if ac > 56:
                weapon.image = load_image('reloading' + str((ac - 57) // 28 + 1) + hero.reved + '.png')
            else:
                weapon.image = load_image('reloading' + str((ac - 1) // 28 + 1) + hero.reved + '.png')
            lefthand.image = load_image('void.png')
            righthand.image = load_image('void.png')

    #    if weapon.name[:5] == 'cross':
    #        if ac <= 56:
    #            weapon.image = weapon.name + 'shooted' + '.png'
    #            lefthand.image = hero.name[0] + weapon.name[:5] + 'left1.png'
    #            righthandhand.image = hero.name[0] + weapon.name[:5] + 'right1.png'
    #        else:
    #            weapon.image = weapon.name + '.png'
    #            lefthand.image = hero.name[0] + weapon.name[:5] + 'left2.png'
    #            righthandhand.image = hero.name[0] + weapon.name[:5] + 'right2.png'


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

fps = 60
all_sprites = pygame.sprite.Group()
animationlimit = 111
border = Border(0, -1238)
land = Land(0, 670)
all_sprites.add(land)
startreloadingtime = 0
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
image = load_image("galeon.png")
screen.blit(image, (0, 0))
clock = pygame.time.Clock()
pygame.init()
all_sprites.add(border)
cam = Camera(camera_configure, 5977, 1754)
level = pygame.sprite.Group()
mh = Hero1(960, 540, 'udp', '', 'cross')
target = Target(1080, 900)
cpt = Npc(2000, 540, 'ucpt', '')
lhcpt = LeftHand(cpt)
rhcpt = RightHand(cpt)
lhmh = LeftHand(mh)

weapon = Weapon(mh, 'cross', 'rifle', '')
rhmh = RightHand(mh)
all_sprites.add(target)
xplus = 0
yplus = 0

animationcount = 0
time = 0
npc = []
mhtent = Tent(480, 600)
cononetent = Tent(100, 1100)
conone = Npc(450, 300, 'uconone', '')
contwo = Npc(750, 300, 'ucontwo', 'reversed')
lhco = LeftHand(conone)
rhco = RightHand(conone)
lhct = LeftHand(contwo)
rhct = RightHand(contwo)
mharmor = Armor(mh, 'void')
all_sprites.add(mhtent, mh, mharmor, lhmh, weapon, rhmh, cpt, rhcpt, lhcpt, conone, contwo,
                lhco, lhct, rhct, rhco, cononetent)
disarmed = True
npc.append(cpt)
npc.append(conone)
npc.append(contwo)
running = True
bullets = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            mh.up = True
        if event.type == pygame.KEYUP and event.key == pygame.K_w:
            mh.up = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and mh.rect.y + 380 < 1754:
            mh.down = True
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            mh.down = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a and mh.rect.x > 0:
            mh.reved = 'reversed'
            mh.left = True
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            mh.left = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d and mh.rect.x + 300 < 5977:
            mh.reved = ''
            mh.right = True
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            mh.right = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and weapon.condition == 'shooted':
            mh.reloading = True
            startreloadingtime = time
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            for i in npc:
                if pygame.sprite.collide_rect(mh, i):
                    i.follo = not i.follo
        if event.type == pygame.MOUSEWHEEL:
            disarmed = not disarmed
        if event.type == pygame.MOUSEBUTTONDOWN and weapon.condition == '':
            weapon.shoot(mh, event.pos[0], event.pos[1], all_sprites, bullets)

    if animationcount == animationlimit:
        animationcount = 0
    screen.blit(image, (0, 0))
    upd(mh, lhmh, rhmh, '', weapon, animationcount)

    animationcount += 1
    clock.tick(fps)
    mh.update()
    cpt.update(mh)
    conone.update(mh)
    contwo.update(mh)
    upd(cpt, lhcpt, rhcpt, '', '', animationcount)
    upd(conone, lhco, rhco, '', '', animationcount)
    upd(contwo, lhct, rhct, '', '', animationcount)
    lhcpt.update(cpt)
    rhcpt.update(cpt)
    lhco.update(conone)
    rhct.update(conone)
    lhct.update(contwo)
    rhcpt.update(contwo)
    lhmh.update(mh)
    mhtent.update()
    mharmor.update(mh)
    border.update()
    weapon.update(mh, disarmed)
    rhmh.update(mh)
    land.update()
    cam.update(mh)
    for i in bullets:
        i.update()
    for e in all_sprites:
        screen.blit(e.image, cam.apply(e))
    time += 1
    pygame.display.flip()

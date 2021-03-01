import pygame
import sys
import os
from objects import *
import random


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


def talk(hero):
    global cptdia1, started, q1end, cptdia2
    if hero == cpt:
        if not started:
            di.fill('капитан Рамирез:\n проснулся наконец, ладно, последний день контракта, прощаю. марш к мишеням,'
                    ' твоя нижняя')
            started = True
            cptdia1 = True
        elif started and not q1end:
            print('otstan')
            di.fill('капитан Рамирез:\n лейтенант, выполняйте приказ!')
        elif q1end:
            print('done')
            di.fill('капитан Рамирез: отличная работа, лейтенант')
            cptdia2 = True


def answer():
    global cptdia1, cptdia2, inds
    if cptdia1:
        di.fill('лейтенант леманн:так точно')
        cptdia1 = False
    if cptdia2:
        di.fill('разведчик: КАПИТАН! НА БАЗУ ИДУТ АББОРИГЕНЫ!')
        inds = True
        cptdia2 = False
    else:
        di.fill('')


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

fps = 56
all_sprites = pygame.sprite.Group()
animationlimit = 27
border = Border(0, -1238)
land = Land(0, 670)
startreloadingtime = 0
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
image = load_image("galeon.png")
screen.blit(image, (0, 0))
clock = pygame.time.Clock()
pygame.init()
targets = []
cptdia1 = False
started = False
cptdia2 = False
all_sprites.add(border)
cam = Camera(camera_configure, 5977, 1754)
level = pygame.sprite.Group()
mh = Hero1(780, 850, 'udp', '', 'void', 'cross', 'rifle')
target = Target(4500, 900)
target2 = Target(4505, 1400)
cpt = Npc(3500, 540, 'ucpt', 'reversed', 'cptcuirass', 'cross', 'rifle')
lhcpt = LeftHand(cpt)
rhcpt = RightHand(cpt)
all_sprites.add(target)
q1end = False
xplus = 0
yplus = 0
di = Dialog(0, 0)
di.fill('')
animationcount = 0
time = 0
npc = []
inds = False
ct = Ct()
kitchen = Kitchen(1500, 800)
mhtent = Tent(480, 600)
cononetent = Tent(100, 1100)
contwotent = Tent(1000, 1050)
conthreetent = Tent(1700, 600)
cpttent = Tent(2300, 1065)
confourtent = Tent(2500, 550)
conone = Npc(450, 400, 'uconone', '', 'cuirass', 'cross', 'rifle')
conone.disarmed = True
contwo = Npc(750, 400, 'ucontwo', 'reversed', 'cuirass', 'cross', 'rifle')
conthree = Npc(3600, 900, 'uconthree', '', 'cuirass', 'cross', 'rifle')
ind = Npc(random.randint(-12, 0), random.randint(-12, 0), 'uconthree', '', 'void', 'cross', 'crossbow')
mhtent.open()
mh.disarmed = True
contwo.disarmed = True
all_sprites.add(mhtent, mh, mh.armor, mh.lefth, mh.weapon, mh.righth, cpt, cpt.armor, cpt.lefth, cpt.weapon, cpt.righth,
                cononetent, conone, conone.armor, conone.lefth, conone.weapon,
                conone.righth, contwo, contwo.armor, contwo.lefth, contwo.weapon, contwo.righth, contwotent,
                conthreetent, kitchen, cpttent, confourtent, conthree, conthree.armor, conthree.lefth,
                conthree.weapon, conthree.righth, target2)
disarmed = False
npc.append(cpt)
# npc.append(conone)
# npc.append(contwo)
running = True
mhhp = Hpscale()
bullets = []
cttext = 'возьмите снаряжение из палатки'
targets.append(target)
targets.append(target2)
targets.append(cpt)
targets.append(conone)
targets.append(contwo)
targets.append(mh)
# targets.append(lhcpt)
ftodo = True
stodo = True
ttodo = True
# targets.append(rhcpt)

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
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            answer()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d and mh.rect.x + 300 < 5977:
            mh.reved = ''
            mh.right = True
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            mh.right = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not mh.reloading:
            mh.reloading = True
            startreloadingtime = time
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            for i in npc:
                if pygame.sprite.collide_rect(mh, i):
                    talk(i)
            if pygame.sprite.collide_rect(mh, mhtent) and mhtent.filled:
                mh.disarmed = False
                mh.armor.name = 'cuirass'
                mhtent.take()
            elif pygame.sprite.collide_rect(mh, mhtent) and not mhtent.filled:
                mhtent.open()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            if mh.weapon.name == 'crossbow':
                mh.weapon.name = 'rifle'
            else:
                mh.weapon.name = 'crossbow'
        if event.type == pygame.MOUSEBUTTONDOWN and mh.weapon.condition == '' and mh.weapon.name == 'rifle':
            mh.weapon.shoot(mh, event.pos[0] - cam.state[0] + 1, event.pos[1] - cam.state[1], all_sprites, bullets,
                            time)
        if event.type == pygame.MOUSEBUTTONDOWN and mh.weapon.crosscondition == '' and mh.weapon.name == 'crossbow':
            mh.weapon.shoot(mh, event.pos[0] - cam.state[0] + 1, event.pos[1] - cam.state[1], all_sprites, bullets,
                            time)

    if animationcount == animationlimit:
        animationcount = 0
    screen.blit(image, (0, 0))
    animationcount += 1
    clock.tick(fps)

    mh.update(animationcount, time, startreloadingtime, border)
    cpt.update(mh, animationcount, time, border)
    conone.update(mh, animationcount, time, border)
    contwo.update(mh, animationcount, time, border)

    if conthree.weapon.condition == '':
        conthree.weapon.shoot(conthree, target.rect.x + 50, target.rect.y + 50, all_sprites, bullets, time)
        conthree.reloading = True
    mhtent.update()
    border.update()
    land.update()
    cam.update(mh)
    di.update(cam.state[0], cam.state[1])
    if target2.counter >= 10:
        q1end = True
        print('ready')

    for i in bullets:
        i.update(targets)
    q = pygame.sprite.Group()
    if inds and time % 4 == 0:
        cpt.down = True
        ind.weapon.shoot(ind, mh.rect.x + 50, mh.rect.y + 50, all_sprites, bullets, time)
        ind.weapon.shoot(ind, cpt.rect.x + 50, cpt.rect.y + 50, all_sprites, bullets, time)
        ind.weapon.shoot(ind, conone.rect.x + 50, conone.rect.y + 50, all_sprites, bullets, time)
        ind.weapon.shoot(ind, conthree.rect.x + 50, conthree.rect.y + 50, all_sprites, bullets, time)
        ind.weapon.shoot(ind, contwo.rect.x + 50, contwo.rect.y + 50, all_sprites, bullets, time)
    for i in all_sprites:
        w = i
        break
    while len(q) < len(all_sprites):
        w = pygame.sprite.Sprite()
        w.image = load_image('void.png')
        w.rect = pygame.Rect(0, 0, 600, 2000)
        for i in all_sprites:
            if pygame.Rect(i).bottom < pygame.Rect(w).bottom and i not in q:
                w = i
        q.add(w)
    screen.blit(land.image, cam.apply(land))
    for i in q:
        screen.blit(i.image, cam.apply(i))
    q.empty()
    mhhp.update()
    screen.blit(di.image, (0, 0))
    if not mh.disarmed and ftodo:
        
        cttext = 'закройте палатку'
        ftodo = False
    if not mhtent.opened and stodo:
        cttext = 'найдите капитана'
        ftodo = False
    if started and ttodo:
        cttext = 'попадите в мишень 4 раза'
        ttodo = False
    if not ttodo:
        cttext = 'доложите капитану'
    ct.kill()
    ct = Ct()
    screen.blit(mhhp.image, (mhhp.rect.x, mhhp.rect.y))
    screen.blit(ct.image, (ct.rect.x, ct.rect.y))
    font = pygame.font.SysFont("Arial", 15)
    textSurf = font.render(cttext, 1, (255, 255, 255))
    screen.blit(textSurf, [817, 104])
    ct.update(cttext)
    if mh.hp < 0:
        os.startfile('game.py')
    for i in range(mh.hp):
        screen.blit(mhhp.hp[i].image, (mhhp.hp[i].rect.x, mhhp.hp[i].rect.y))
    time += 1
    pygame.display.flip()

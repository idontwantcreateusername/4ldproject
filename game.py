#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from player import *
from blocks import *

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 400  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
FINISH_EVENT = pygame.USEREVENT + 1


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = Player(55, 400)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)

    level = [
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                    *                  ",
        "                                       ",
        "                    -                  ",
        "-                 -                   -",
        "-               -                     -",
        " ------------------------------------- "]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    finish = (0, 0)
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "*":
                finish = Block(x, y, "blocks/star.png")
                entities.add(finish)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT or e.type == FINISH_EVENT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True

            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_a:
                left = False
            if e.type == KEYUP and e.key == K_d:
                right = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение

        if sprite.collide_rect(hero, finish):
            pygame.event.post(pygame.event.Event(FINISH_EVENT))

        # entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()

import pygame
from player import *
from blocks import *
from hands import *
from health import *
from bullet import *

# Объявляем переменные
WIN_WIDTH = 1920  # Ширина создаваемого окна
WIN_HEIGHT = 1080  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
lives = 0
FINISH_EVENT = pygame.USEREVENT + 1

player_mini_img = [('%s/zip/healscale.png' % ICON_DIR, 0.1)]
player_mini_img2 = [('%s/hero/healpoint.png' % ICON_DIR, 0.1)]


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width // 0.5, height // 0.5)

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
    pygame.display.set_caption("Платформер")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание фона
    good = pygame.image.load('zip/endings/good.png')
    bag = pygame.image.load('zip/endings/bad.png')
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    spikes = pygame.sprite.Group()
    healthbar = []
    platforms = []  # то, во что мы будем врезаться или опираться

    level = [
        "                                                          ",
        "                                                          ",
        "                                                          ",
        "                                                          ",
        "                                                          ",
        "                                                          ",
        "                                                          ",
        "                                                          ",
        "                   -                                      ",
        "-                 -                                 *    -",
        "- h              -      ^^^^                             -",
        " -------------------------------------------------------- "]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    finish = (0, 0)
    spike = (0, 0)
    # hp = Health(x, y, 'zip/environment/healpoint.png')
    # entities.add(hp)
    health_x = x
    health_y = y
    # healthbar.append(hp)
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "*":
                finish = Block(x, y, "blocks/star.png")
                entities.add(finish)
            elif col == "^":
                spike = Spike(x, y)
                entities.add(spike)
                spikes.add(spike)
            elif col == "h":
                hero_x = x
                hero_y = y
                hero = Player(x, y)
                handr = Handr(x, y)
                handl = Handl(x, y)
                entities.add(hero)
                entities.add(handr)
                entities.add(handl)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    def win_screen():
        screen.blit(good, (0, 0))
        pygame.display.flip()
        waiting = True
        i = 0
        while waiting:
            timer.tick(60)
            i += 1
            if i == 600:
                raise SystemExit
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == KEYUP and e.key == K_ESCAPE:
                    raise SystemExit
                if e.type == QUIT or e.type == FINISH_EVENT:
                    raise SystemExit

    def lose_screen():
        screen.blit(bag, (0, 0))
        pygame.display.flip()
        waiting = True
        i = 0
        while waiting:
            i += 1
            if i == 600:
                raise SystemExit
            timer.tick(60)
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == KEYUP and e.key == K_ESCAPE:
                    raise SystemExit
                if e.type == QUIT or e.type == FINISH_EVENT:
                    raise SystemExit

    def death():
        global lives
        if lives == 0:
            lose_screen()
        # else:
        #   lives -= 1
        #  print('death')
        # hero.rect.x = hero_x
        # hero.rect.y = hero_y
        # handr.rect.x = hero_x
        # handr.rect.y = hero_y
        # handl.rect.x = hero_x
        # handl.rect.y = hero_y
        # hp.rect.x = health_x
        # hp.rect.y = health_y

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
            if e.type == KEYUP and e.key == K_ESCAPE:
                raise SystemExit

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        try:
            b.update(True, platforms)
        except:
            pass

        hero.update(left, right, up, platforms)  # передвижение
        handr.update(left, right, up, platforms)
        handl.update(left, right, up, platforms)
        # hp.rect.x = hero.rect.x + 125
        # hp.rect.y = hero.rect.y - 100

        if sprite.collide_rect(hero, finish):
            win_screen()

        if sprite.spritecollide(hero, spikes, False):
            death()

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()

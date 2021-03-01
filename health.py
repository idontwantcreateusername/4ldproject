from pygame import *
import os

PLATFORM_WIDTH = 108
PLATFORM_HEIGHT = 108
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами
MOVE_SPEED = 20
WIDTH = 296
HEIGHT = 380
COLOR = "#880000"
JUMP_POWER = 10
ANIMATION_DELAY = 0.1  # скорость смены кадров


class Health(sprite.Sprite):
    def __init__(self, x, y, img):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load(img)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.yvel = 0  # скорость вертикального перемещения
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

    def update(self, left, right, up):

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel

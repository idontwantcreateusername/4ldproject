import os
import sys

import pygame

if __name__ == '__main__':
    def inside(mouse, button):
        if button[0] < mouse[0] < button[2] and button[1] < mouse[1] < button[3]:
            return True
        else:
            return False
        # возвращаем true если мышь внутри кнопки
    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image


    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.blit(load_image('Без имени.png'), (0, 0))
    newgamecoords = 109, 907, 475, 1012
    loadgamecoords = 0, 0, 0, 0
    exitcoords = 1460, 912, 1820, 1010
    size = 0
    qw = False
    clock = pygame.time.Clock()
    position = -255, -255


    def draw():
        global size, position
        pygame.draw.circle(screen, (255, 255, 0), position, size)
        size += 1

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inside(event.pos, newgamecoords):
                    os.startfile('l1.py')
                    exit(0)
                    # запусткаем l1c1.py
                if inside(event.pos, loadgamecoords):
                    a = 0
                    # получаем из базы данных название сохранённого чекпоинта, загружаем его
                if inside(event.pos, exitcoords):
                    exit(0)

        if qw:
            draw()
        clock.tick(100)
        pygame.display.flip()
        if size == 600:
            qw = False

        pygame.display.flip()



    pygame.quit()

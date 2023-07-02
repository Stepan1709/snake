import pygame
from pygame import Color
from pygame import *
import random
from random import randrange
import math

pygame.init()

# размеры основных элементов
window_width = 1000
window_height = 800
sidebar_width = 200
size = 40

# основные цвета
head_color = Color(0, 255, 0)  # Зеленый цвет для головы
tail_color = Color(0, 0, 255)  # Синий цвет для хвоста
WHITE = (254, 254, 254)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

sc = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('AI-snake')
# pygame.display.set_icon()

# в игровом окне происходит игровой процесс
game_window = pygame.Surface((window_width - 200, window_height))
game_window.fill(BLACK)

# в сайдбаре находятся кнопки и настройки
sidebar = pygame.Surface((sidebar_width, window_height))
sidebar.fill(GRAY)

pygame.display.update()

# стартовые настройки игры
x, y = randrange(0, 800, size), randrange(0, 800, size)
apple = randrange(0, 800, size), randrange(0, 800, size)
while apple == (x, y):
    apple = randrange(0, 800, size), randrange(0, 800, size)
length = 1
snake = [(x, y)]
#directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
#dx, dy = random.choice(directions)
dx, dy = 0, 0
FPS = 5

clock = pygame.time.Clock()

game_buffer = pygame.Surface((window_width - 100, window_height))
game_buffer.fill(BLACK)

# основной цикл игры
running = True
while running:
    key_processed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # выход из приложения
        elif event.type == pygame.KEYDOWN and not key_processed:
            if event.key == pygame.K_w and dy != 1:  # Запрещаем движение вниз, если текущее направление вверх
                dx, dy = 0, -1
            elif event.key == pygame.K_s and dy != -1:  # Запрещаем движение вверх, если текущее направление вниз
                dx, dy = 0, 1
            elif event.key == pygame.K_a and dx != 1:  # Запрещаем движение вправо, если текущее направление влево
                dx, dy = -1, 0
            elif event.key == pygame.K_d and dx != -1:  # Запрещаем движение влево, если текущее направление вправо
                dx, dy = 1, 0

            key_processed = True

    x += dx * size
    y += dy * size
    snake.append((x, y))
    if length < len(snake):
        snake.pop(0)

    if snake[-1] == apple:
        apple = randrange(0, 800, size), randrange(0, 800, size)
        while apple in snake:
            apple = randrange(0, 800, size), randrange(0, 800, size)
        length += 1

    if snake[-1][0] >= 800 or snake[-1][0] < 0 or snake[-1][1] >= 800 or snake[-1][1] < 0:
        x, y = randrange(0, 800, size), randrange(0, 800, size)
        apple = randrange(0, 800, size), randrange(0, 800, size)
        while apple == (x, y):
            apple = randrange(0, 800, size), randrange(0, 800, size)
        length = 1
        snake = [(x, y)]
        dx, dy = 0, 0

    if snake[-1] in snake[0:-1]:
        x, y = randrange(0, 800, size), randrange(0, 800, size)
        apple = randrange(0, 800, size), randrange(0, 800, size)
        while apple == (x, y):
            apple = randrange(0, 800, size), randrange(0, 800, size)
        length = 1
        snake = [(x, y)]
        dx, dy = 0, 0

    # Очищаем буферный холст
    game_buffer.fill(BLACK)

    # Отрисовываем змейку и яблоко на буферном холсте
    start_index = length - 1
    end_index = 0
    for i, (x, y) in enumerate(snake):
        G = (0, randrange(200, 256), randrange(0, 56))
        pygame.draw.rect(game_buffer, G, (x + 1, y + 1, size - 2, size - 2))
    draw_apple = tuple(coord + 1 for coord in apple)
    pygame.draw.rect(game_buffer, RED, (*draw_apple, size - 2, size - 2))

    # Отображаем буферный холст на основном экране
    sc.fill(BLACK)
    sc.blit(game_buffer, (0, 0))
    sc.blit(sidebar, (window_width - sidebar_width, 0))

    pygame.display.flip()
    clock.tick(FPS)

    pygame.display.update()
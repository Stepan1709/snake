import pygame
from random import randrange

pygame.init()

# размеры основных элементов
window_width = 1000
window_height = 800
sidebar_width = 200
size = 40

# основные цвета
WHITE = (254, 254, 254)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
L_BLUE = (0, 255, 200)
RED = (255, 0, 0)

# основной дисплей приложения
sc = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('AI-snake')
# pygame.display.set_icon()

# в игровом окне происходит игровой процесс
game_window = pygame.Surface((window_width - 200, window_height))
game_window.fill(BLACK)

# в сайд баре находятся кнопки и настройки
sidebar = pygame.Surface((sidebar_width, window_height))
sidebar.fill(GRAY)

# буфер, в него копируются изображения со всех объектов, прежде чем показываются пользователю
game_buffer = pygame.Surface((window_width, window_height))
game_buffer.fill(BLACK)

# шрифт для вывода очков
font_score = pygame.font.Font(None, 34)

# pygame.display.update()

# стартовые настройки игры
x, y = randrange(0, 800, size), randrange(0, 800, size)
apple = randrange(0, 800, size), randrange(0, 800, size)
while apple == (x, y):
    apple = randrange(0, 800, size), randrange(0, 800, size)
length = 1
snake = [(x, y)]
# directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
# dx, dy = random.choice(directions)
dx, dy = 0, 0
FPS = 5

clock = pygame.time.Clock()

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

    # изменение направления движения за счет добавления новой пары координат (головы) в змейку и удаление старой пары
    # (хвост)
    x += dx * size
    y += dy * size
    snake.append((x, y))
    if length < len(snake):
        snake.pop(0)

    # если голова змеи совпадает с координатами яблока, она его ест и растет
    if snake[-1] == apple:
        apple = randrange(0, 800, size), randrange(0, 800, size)
        while apple in snake:
            apple = randrange(0, 800, size), randrange(0, 800, size)
        length += 1

    # если голова змейки выходит за пределы карты, то игра начинается заново
    if snake[-1][0] >= 800 or snake[-1][0] < 0 or snake[-1][1] >= 800 or snake[-1][1] < 0:
        x, y = randrange(0, 800, size), randrange(0, 800, size)
        apple = randrange(0, 800, size), randrange(0, 800, size)
        while apple == (x, y):
            apple = randrange(0, 800, size), randrange(0, 800, size)
        length = 1
        snake = [(x, y)]
        dx, dy = 0, 0

    # если координаты головы змейки совпадут с любой ее частью, то игра начинается заново
    if snake[-1] in snake[0:-1]:
        x, y = randrange(0, 800, size), randrange(0, 800, size)
        apple = randrange(0, 800, size), randrange(0, 800, size)
        while apple == (x, y):
            apple = randrange(0, 800, size), randrange(0, 800, size)
        length = 1
        snake = [(x, y)]
        dx, dy = 0, 0

    # Очищаем холсты
    game_buffer.fill(BLACK)
    game_window.fill(BLACK)
    sidebar.fill(GRAY)

    # Отрисовываем змейку и яблоко на холсте game_window
    start_index = length - 1
    end_index = 0
    for i, (x, y) in enumerate(snake):
        if snake[i] == snake[-1]:
            pygame.draw.rect(game_window, L_BLUE, (x + 1, y + 1, size - 2, size - 2))
        else:
            G = (0, randrange(200, 256), randrange(0, 56))
            pygame.draw.rect(game_window, G, (x + 1, y + 1, size - 2, size - 2))
    draw_apple = tuple(coord + 1 for coord in apple)
    pygame.draw.rect(game_window, RED, (*draw_apple, size - 2, size - 2))

    # Отрисовываем текст на холсте sidebar
    score_text = font_score.render(f"Score: {length - 1}", True, "yellow")
    sidebar.blit(score_text, (50, 10))

    # Отображаем холсты game_window и sidebar на буферный холст, а затем буфер на основной экран
    game_buffer.blit(game_window, (0, 0))
    game_buffer.blit(sidebar, (window_width - sidebar_width, 0))
    sc.blit(game_buffer, (0, 0))

    # обновляем изображение на экране
    pygame.display.flip()
    clock.tick(FPS)

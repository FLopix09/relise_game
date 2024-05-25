import pygame
import random
import time

pygame.init()

################ Стандартні налаштування ###################
win_width = 500
win_height = 500
FPS = 3

background = pygame.transform.scale(pygame.image.load('background.jpg'), (win_width, win_height))  # Завантаження фона

win = pygame.display.set_mode((win_width, win_height))  # Створення вікна
win.blit(background, (0, 0))


class Apple(pygame.sprite.Sprite):
    """Клас для яблука. З методом для випадкогово телепортування"""

    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def teleport(self):
        self.rect.x = random.randint(0, (win_width - self.rect.width) // self.rect.width) * self.rect.width
        self.rect.y = random.randint(0, (win_height - self.rect.height) // self.rect.height) * self.rect.height

    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Snake:
    """Клас для однієї частини змійки. Метод goto запам'ятовує останні координати і переміщує змійку на нові"""

    def __init__(self, x, y, size, color=(100, 100, 255)):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.color = color
        self.last_pos = [x, y]
        self.direction = 'right'
        self.step = 1

    def goto(self, x, y):
        self.last_pos = [self.rect.x, self.rect.y]
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)


SIZE = 25  # Розмір яблука, та однієї частини змійки
delay = 10  # Застримка в циклі

snakes = []  # Список частинок змійки

apple = Apple('apple.png', 0, 0, SIZE, SIZE)  # Створення яблука та телепортування його у випадкове місце
apple.teleport()

head = Snake(100, 100, SIZE, color=(100, 255, 255))  # Створення голови змійки та додавання її у список
snakes.append(head)

scores = 0  # Змінна для зберігання рахунку
f = pygame.font.SysFont("Arial", 30)
score_text = f.render(str(scores), True, (100, 100, 100))  # Написи для відображення рахунку
score_label = f.render("Рахунок:", True, (100, 100, 100))


def move(x, y):
    """Функція для переміщення кожної частини змійки на минуле положення частини яка була перед ними"""
    lx, ly = x, y
    for s in snakes:
        s.goto(lx, ly)
        lx, ly = s.last_pos[0], s.last_pos[1]


run = True
while run:  # Головний цикл програми
    pygame.time.delay(delay)  # Затримка (замість clock.tick)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:  # При натиску на кнопку змінюється напрям автоматичного руху
            if event.key == pygame.K_w:
                if head.direction != 'down':
                    head.direction = 'up'
                    break  # Цикл преривається задля усунення багу, коли за один крок циклу одночасно оброблювалось декілька натисків клавіш

            elif event.key == pygame.K_s:
                if head.direction != 'up':
                    head.direction = 'down'
                    break

            elif event.key == pygame.K_a:
                if head.direction != 'right':
                    head.direction = 'left'
                    break

            elif event.key == pygame.K_d:
                if head.direction != 'left':
                    head.direction = 'right'
                    break

    # Автоматичний рух за певним напрямком
    if head.direction == 'up':
        move(head.rect.x, head.rect.y - head.step)
    elif head.direction == 'down':
        move(head.rect.x, head.rect.y + head.step)
    elif head.direction == 'right':
        move(head.rect.x + head.step, head.rect.y)
    elif head.direction == 'left':
        move(head.rect.x - head.step, head.rect.y)

    # Перевірка на зіткнення з яблуком
    if apple.rect.colliderect(head.rect):
        scores += 1  # Зміна рахунку
        score_text = f.render(str(scores), True, (100, 100, 100))  # Зміна тексту з рахунком
        apple.teleport()  # Телепортування яблука у випадкову позицію

        # Додавання 20ти частнок змії при з'їданні яблука
        for _ in range(20):
            last_pos = snakes[-1].last_pos
            snakes.append(Snake(last_pos[0], last_pos[1], SIZE))

    win.blit(background, (0, 0))  # Малювання фону

    apple.draw()  # Малювання яблука

    win.blit(score_text, (100, 0))  # Малювання рахунку
    win.blit(score_label, (0, 0))

    for snake in snakes:  # Цикл для малювання кожної частини змійки та перевірка на з'їдання себе
        if head.rect.colliderect(snake.rect) and snakes.index(snake) >= head.size * 2:
            # З'їсти можна тільки частину тіла яка починається з певної довжини
            text = pygame.font.SysFont("Arial", 50).render("You lose!", True, (0, 0, 0))
            win.blit(text, (200, 200))
            snake.color = (255, 100, 100)  # Місце влучання офарбовуємо червоним
            run = False  # Заершуємо цикл
        snake.draw()

    # Перевірка на зіткнення з межами гри
    if head.rect.y + head.rect.height > win_height or head.rect.y < 0 or head.rect.x + head.rect.width > win_width or head.rect.x < 0:
        text = pygame.font.SysFont("Arial", 50).render("You lose!", True, (0, 0, 0))
        win.blit(text, (200, 200))
        run = False

    pygame.display.update()
time.sleep(3)  # Очікування для того щоб гра не відразу закрилась і користувач побачив як програв і з яким рахунком

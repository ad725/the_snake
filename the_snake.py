from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Список всех возможных направлений для случайного выбора
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Словарь управления движениями
MOVEMENT_KEYS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной класс, представляющий фигуры в игре"""

    def __init__(self):
        self.body_color = None
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Отрисовка фигур с переопределением в наследуемых классах"""
        pass


class Snake(GameObject):
    """Наследуемый класс змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice(ALL_DIRECTIONS)
        self.next_direction = self.direction
        self.length = 1

    def get_head_position(self):
        """Получить позицию головы змейки"""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Смена направления движения змейки"""
        opposite_directions = {
            UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT
        }
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction

    def move(self):
        """Движение змейки"""
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions[:-1]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс змейки"""
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice(ALL_DIRECTIONS)
        self.next_direction = self.direction
        self.length = 1

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def increase_length(self):
        """Увеличение длины змейки"""
        self.length += 1


class Apple(GameObject):
    """Наследуемый класс яблока"""

    def __init__(self, occupied_cells=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(occupied_cells or [])

    def draw(self):
        """Отрисовка на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_cells):
        """Генерация объекта на случайной позиции"""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)
            if position not in occupied_cells:
                return position


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in MOVEMENT_KEYS:
                game_object.update_direction(MOVEMENT_KEYS[event.key])


def main():
    """Главная функция игры"""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.increase_length()
            apple = Apple(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Список всех возможных направлений для случайного выбора
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Словарь управления движениями
MOVEMENT_KEYS = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT,
}

# Цвета игры
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BODY_COLOR = (255, 255, 0)

# Скорость движения змейки:
SPEED = 6

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=BORDER_COLOR):
        self.body_color = body_color
        self.position = CENTER_POSITION

    def draw_cell(self, position, border_color=BORDER_COLOR):
        """
        Отрисовка одной ячейки игрового объекта.

        Принимает позицию и цвет границы.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Отрисовка игрового объекта."""
        raise NotImplementedError(
            'Метод draw() должен быть реализован в наследнике'
        )


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTIONS)
        self.length = 1
        self.last_position = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """
        Обновляет направление змейки.

        Принимает новое направление змейки.
        """
        opposite_directions = {
            UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last_position = self.positions.pop()
        else:
            self.last_position = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTIONS)
        self.last_position = None
        self.length = 1

    def draw(self):
        """Отрисовывает змейку - только изменения."""
        if self.last_position is not None:
            rect = pg.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.draw_cell(self.get_head_position())

    def increase_length(self):
        """Увеличивает длину змейки."""
        self.length += 1


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, occupied_cells=None):
        super().__init__(APPLE_COLOR)
        occupied_cells = occupied_cells or [CENTER_POSITION]
        self.randomize_position(occupied_cells)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position)

    def randomize_position(self, occupied_cells):
        """
        Устанавливает случайную позицию для яблока.

        Принимает список занятых ячеек.
        """
        while self.position in occupied_cells:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key in MOVEMENT_KEYS:
                game_object.update_direction(MOVEMENT_KEYS[event.key])


def main():
    """Главная функция игры, содержащая основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    snake.draw()
    pg.display.update()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        head_position = snake.get_head_position()

        if head_position in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        elif head_position == apple.position:
            snake.increase_length()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

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
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=BODY_COLOR):
        self.body_color = body_color
        self.position = CENTER_POSITION

    def draw_cell(self, position, color=None):
        """
        Отрисовка одной ячейки игрового объекта.
        Принимает обязательный аргумент `позиция`
        и необязательный цвет ячейки.
        """
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка игрового объекта."""
        raise NotImplementedError(
            "Метод draw() должен быть реализован в наследнике"
        )


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTIONS)
        self.length = 1
        self.last_positions = []

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """
        Принимает новое направление змейки
        и обновляет направление змейки.
        """
        opposite_directions = {
            UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def move(self):
        """Перемещает змейку в текущем направлении."""
        self.last_positions = self.positions.copy()

        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [CENTER_POSITION]
        self.direction = choice(ALL_DIRECTIONS)
        self.length = 1
        self.last_positions = []

    def draw(self):
        """Отрисовывает змейку - только изменения."""
        positions_to_clear = [pos for pos in self.last_positions
                              if pos not in self.positions]

        positions_to_draw = []
        for i, pos in enumerate(self.positions):
            if i >= len(self.last_positions) or pos != self.last_positions[i]:
                positions_to_draw.append(pos)

        for pos in positions_to_clear:
            self.clear_cell(pos)

        for pos in positions_to_draw:
            self.draw_cell(pos)

    def draw_full(self):
        """Отрисовывает всю змейку."""
        for position in self.positions:
            self.draw_cell(position)

    def clear_cell(self, position):
        """Очищает ячейку, закрашивая её фоном."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def increase_length(self):
        """Увеличивает длину змейки."""
        self.length += 1


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, occupied_cells=None):
        super().__init__(APPLE_COLOR)
        if occupied_cells is None:
            occupied_cells = []
        self.randomize_position(occupied_cells)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position)

    def randomize_position(self, occupied_cells):
        """
        Устанавливает случайную позицию для яблока, избегая занятых клеток.
        Принимает список занятых змейкой ячеек.
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_cells:
                self.position = new_position
                break


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key in MOVEMENT_KEYS:
                game_object.update_direction(MOVEMENT_KEYS[event.key])


def main():
    """Главная функция игры, содержащая основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    snake.draw_full()
    pg.display.update()

    while True:
        handle_keys(snake)
        snake.move()

        head_position = snake.get_head_position()

        if head_position in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
            snake.draw_full()
            apple.draw()
        else:
            snake.draw()

        if head_position == apple.position:
            snake.increase_length()
            apple.randomize_position(snake.positions)
            snake.draw()
            apple.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

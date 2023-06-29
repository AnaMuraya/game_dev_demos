import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 0], [1, 1, 0]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 1], [1, 0, 0], [0, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1], [0, 0, 0]]  # J shape
]

# Tetromino colors
COLORS = [
    CYAN,
    YELLOW,
    MAGENTA,
    GREEN,
    RED,
    ORANGE,
    BLUE
]

# Tetromino class
class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def draw(self):
        for row in range(len(self.shape[self.rotation])):
            for col in range(len(self.shape[self.rotation][row])):
                if self.shape[self.rotation][row][col]:
                    pygame.draw.rect(window, self.color, (self.x + col, self.y + row, 1, 1))

# Game variables
grid = [[None] * 10 for _ in range(20)]
current_piece = None
fall_time = 0
fall_speed = 0.5

# Create a new tetromino
def new_piece():
    global current_piece
    shape = random.choice(SHAPES)
    x = (10 - len(shape[0])) // 2
    y = 0
    current_piece = Tetromino(x, y, shape)

# Check if a position is valid for the current piece
def is_valid_position():
    for row in range(len(current_piece.shape[current_piece.rotation])):
        for col in range(len(current_piece.shape[current_piece.rotation][row])):
            if current_piece.shape[current_piece.rotation][row][col]:
                if (
                    current_piece.x + col < 0
                    or current_piece.x + col >= 10
                    or current_piece.y + row >= 20
                    or grid[current_piece.y + row][current_piece.x + col]
                ):
                    return False
    return True

# Add the current piece to the grid
def add_to_grid():
    for row in range(len(current_piece.shape[current_piece.rotation])):
        for col in range(len(current_piece.shape[current_piece.rotation][row])):
            if current_piece.shape[current_piece.rotation][row][col]:
                grid[current_piece.y + row][current_piece.x + col] = current_piece.color

# Check if any rows are complete and clear them
def clear_rows():
    full_rows = [row for row in range(20) if all(grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [None] * 10)

# Game loop
running = True
clock = pygame.time.Clock()

new_piece()  # Create the initial piece

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_piece.rotate()
            elif event.key == pygame.K_LEFT:
                current_piece.move_left()
                if not is_valid_position():
                    current_piece.move_right()
            elif event.key == pygame.K_RIGHT:
                current_piece.move_right()
                if not is_valid_position():
                    current_piece.move_left()

    # Move the current piece down
    if pygame.time.get_ticks() - fall_time >= fall_speed * 1000:
        current_piece.move_down()
        if not is_valid_position():
            current_piece.move_up()
            add_to_grid()
            clear_rows()
            new_piece()

    # Clear the screen
    window.fill(BLACK)

    # Draw the grid
    for row in range(20):
        for col in range(10):
            if grid[row][col]:
                pygame.draw.rect(window, grid[row][col], (col, row, 1, 1))

    # Draw the current piece
    current_piece.draw()

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

# Quit the game
pygame.quit()

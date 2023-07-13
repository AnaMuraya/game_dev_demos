import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define player and maze variables
player_size = 20
player_color = GREEN
player_x = player_y = 0
maze_width = int(WIDTH / player_size)
maze_height = int(HEIGHT / player_size)
maze = []
for _ in range(maze_height):
    row = [random.choice([0, 1]) for _ in range(maze_width)]
    maze.append(row)

# Generate the maze exit position
exit_x = random.randint(0, maze_width - 1)
exit_y = random.randint(0, maze_height - 1)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        player_y -= player_size
    if keys[K_DOWN]:
        player_y += player_size
    if keys[K_LEFT]:
        player_x -= player_size
    if keys[K_RIGHT]:
        player_x += player_size

    # Check for collision with maze walls
    if player_x < 0 or player_x >= WIDTH or player_y < 0 or player_y >= HEIGHT:
        player_x = player_y = 0

    # Check if the player reached the exit
    if player_x == exit_x * player_size and player_y == exit_y * player_size:
        print("Congratulations! You reached the exit.")
        running = False

    # Draw the maze
    screen.fill(BLACK)
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * player_size, y * player_size, player_size, player_size))

    # Draw the exit
    pygame.draw.rect(screen, RED, (exit_x * player_size, exit_y * player_size, player_size, player_size))

    # Draw the player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    pygame.display.flip()

pygame.quit()

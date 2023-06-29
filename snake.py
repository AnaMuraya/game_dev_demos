import pygame
import random

pygame.init()

# Setup the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Setup the colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Snake initial position and properties
snake_size = 20
snake_speed = 10
snake_x = width // 2
snake_y = height // 2
snake_x_change = 0
snake_y_change = 0
snake_body = []
snake_length = 1

# Food properties
food_size = 20
food_x = random.randint(0, (width - food_size) // snake_size) * snake_size
food_y = random.randint(0, (height - food_size) // snake_size) * snake_size

# Game over flag
game_over = False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -snake_speed
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = snake_speed
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_y_change = -snake_speed
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = snake_speed
                snake_x_change = 0

    # Update snake position
    snake_x += snake_x_change
    snake_y += snake_y_change

    # Check for collision with boundaries
    if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
        game_over = True

    # Check for collision with food
    if snake_x == food_x and snake_y == food_y:
        food_x = random.randint(0, (width - food_size) // snake_size) * snake_size
        food_y = random.randint(0, (height - food_size) // snake_size) * snake_size
        snake_length += 1

    # Draw the background
    screen.fill(black)

    # Draw the snake
    snake_head = [snake_x, snake_y]
    snake_body.append(snake_head)
    if len(snake_body) > snake_length:
        del snake_body[0]

    for segment in snake_body:
        pygame.draw.rect(screen, green, (segment[0], segment[1], snake_size, snake_size))

    # Draw the food
    pygame.draw.rect(screen, red, (food_x, food_y, food_size, food_size))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(15)

# Quit the game
pygame.quit()

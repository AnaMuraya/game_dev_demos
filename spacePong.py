import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Laser settings
LASER_SPEED = 7

# Target settings
TARGET_WIDTH = 30
TARGET_HEIGHT = 30

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Pong")

# Load images
spaceship_img = pygame.image.load("glassAssets/animal1.png")
spaceship_img = pygame.transform.scale(spaceship_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# Initial positions of paddles
left_paddle_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
right_paddle_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2

# Initial position and direction of the laser beam
laser_x = WINDOW_WIDTH // 2
laser_y = WINDOW_HEIGHT // 2
laser_angle = random.uniform(-45, 45)  # Random initial angle between -45 and 45 degrees

# Targets list
targets = []

# Score
score = 0

# Game clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += PADDLE_SPEED

    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += PADDLE_SPEED

    # Move the laser beam
    laser_x += LASER_SPEED * math.cos(math.radians(laser_angle))
    laser_y -= LASER_SPEED * math.sin(math.radians(laser_angle))

    # Check if the laser beam goes beyond the display area
    if laser_x < 0:
        laser_x = 0
        laser_angle = 180 - laser_angle
    elif laser_x > WINDOW_WIDTH:
        laser_x = WINDOW_WIDTH
        laser_angle = 180 - laser_angle

    if laser_y < 0:
        laser_y = 0
        laser_angle = 360 - laser_angle
    elif laser_y > WINDOW_HEIGHT:
        laser_y = WINDOW_HEIGHT
        laser_angle = 360 - laser_angle

    # Check for collisions with the paddles
    if (
        laser_x < PADDLE_WIDTH
        and left_paddle_y < laser_y < left_paddle_y + PADDLE_HEIGHT
    ) or (
        laser_x > WINDOW_WIDTH - PADDLE_WIDTH
        and right_paddle_y < laser_y < right_paddle_y + PADDLE_HEIGHT
    ):
        laser_angle = 180 - laser_angle

    # Check for collisions with targets
    for target in targets:
        if target.collidepoint((laser_x, laser_y)):
            targets.remove(target)
            score += 1

    # Spawn new targets
    if len(targets) < 5 and random.random() < 0.02:
        target_x = random.randint(100, WINDOW_WIDTH - 100)
        target_y = random.randint(50, WINDOW_HEIGHT - 50)
        targets.append(pygame.Rect(target_x, target_y, TARGET_WIDTH, TARGET_HEIGHT))

    # Draw everything on the screen
    window.fill(BLACK)
    pygame.draw.rect(window, RED, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(
        window, GREEN, (WINDOW_WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    )
    pygame.draw.line(window, WHITE, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT))

    for target in targets:
        pygame.draw.rect(window, WHITE, target)

    pygame.draw.circle(window, WHITE, (int(laser_x), int(laser_y)), 5)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

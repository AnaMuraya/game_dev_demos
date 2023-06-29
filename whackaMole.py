import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

# Load the mole image
mole_image = pygame.image.load("assets/apple.jpg")
mole_image = pygame.transform.scale(mole_image, (100, 100))

# Game constants
MOLE_SIZE = mole_image.get_size()
MOLE_SPEED = 3
MOLE_APPEAR_DELAY = 1000  # Time delay between mole appearances (in milliseconds)
MOLE_VISIBLE_TIME = 50  # Duration for which the mole is visible (in milliseconds)
SCORE_FONT = pygame.font.Font(None, 36)

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Game variables
score = 0
mole_rect = mole_image.get_rect()
mole_rect.center = (WIDTH // 2, HEIGHT // 2)
mole_appear_time = pygame.time.get_ticks() + MOLE_APPEAR_DELAY
mole_visible = False
mole_visible_start_time = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mole_visible and mole_rect.collidepoint(event.pos):
                score += 1
                mole_visible = False

    # Update the game logic
    current_time = pygame.time.get_ticks()
    if current_time >= mole_appear_time:
        if not mole_visible:
            mole_visible = True
            mole_rect.center = (random.randint(0, WIDTH - MOLE_SIZE[0]), random.randint(0, HEIGHT - MOLE_SIZE[1]))
            mole_appear_time = current_time + MOLE_APPEAR_DELAY
            mole_visible_start_time = current_time
        elif current_time - mole_visible_start_time >= MOLE_VISIBLE_TIME:
            mole_visible = False

    # Update the screen
    screen.fill((255, 255, 255))

    if mole_visible:
        screen.blit(mole_image, mole_rect)

    score_text = SCORE_FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()

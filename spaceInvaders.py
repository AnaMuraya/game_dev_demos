import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_image = pygame.image.load("assets/apple.jpg")
enemy_image = pygame.image.load("assets/image1.jpg")
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
bullet_image = pygame.image.load("assets/image8.jpg")

# Player constants
player_width, player_height = player_image.get_size()
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

# Enemy constants
enemy_width, enemy_height = enemy_image.get_size()
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = 50
enemy_speed = 2

# Bullet constants
bullet_width, bullet_height = bullet_image.get_size()
bullet_x = 0
bullet_y = 0
bullet_speed = 5
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_x += player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    bullet_state = "fire"

    # Update the screen
    screen.fill((0, 0, 0))

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Draw the enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw the bullet
    if bullet_state == "fire":
        screen.blit(bullet_image, (bullet_x, bullet_y))
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_state = "ready"

    # Collision detection
    if bullet_state == "fire" and bullet_y < enemy_y + enemy_height:
        if enemy_x < bullet_x < enemy_x + enemy_width or enemy_x < bullet_x + bullet_width < enemy_x + enemy_width:
            score += 1
            bullet_state = "ready"
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy_y = 50

    # Render and draw the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update enemy position
    enemy_x += enemy_speed
    if enemy_x <= 0 or enemy_x >= WIDTH - enemy_width:
        enemy_speed *= -1

    pygame.display.flip()

# Quit the game
pygame.quit()

import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Missile Command")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game constants
FPS = 60
CITY_HEIGHT = 20
CITY_SPACING = 100
MISSILE_SPEED = 5
BOMB_SPEED = 2

# Levels
levels = [
    {"cities": 5, "missiles": 10, "bombs": 20},
    {"cities": 4, "missiles": 12, "bombs": 25},
    {"cities": 3, "missiles": 15, "bombs": 30}
]

# Create the cities
cities = []
def create_cities(num_cities):
    for i in range(num_cities):
        city_x = i * CITY_SPACING + CITY_SPACING // 2
        city_y = HEIGHT - CITY_HEIGHT
        cities.append(pygame.Rect(city_x, city_y, CITY_HEIGHT, CITY_HEIGHT))

# Create the missiles and bombs
missiles = []
bombs = []

# Game variables
level = 0
score = 0
game_over = True

# Create the cities for the initial level
create_cities(levels[level]["cities"])

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over:
            # Start a new game
            level = 0
            score = 0
            cities.clear()
            missiles.clear()
            bombs.clear()
            create_cities(levels[level]["cities"])
            game_over = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            if len(missiles) < levels[level]["missiles"]:
                target_x, target_y = event.pos
                missiles.append(pygame.Rect(target_x - 2, HEIGHT - CITY_HEIGHT, 4, CITY_HEIGHT))

    if not game_over:
        # Move the missiles
        for missile in missiles:
            missile.y -= MISSILE_SPEED

        # Move the bombs
        for bomb in bombs:
            bomb.y += BOMB_SPEED

        # Check for missile-bomb collisions
        for missile in missiles:
            for bomb in bombs:
                if missile.colliderect(bomb):
                    missiles.remove(missile)
                    bombs.remove(bomb)
                    break

        # Check for bomb-city collisions
        for bomb in bombs:
            for city in cities:
                if city.colliderect(bomb):
                    cities.remove(city)
                    bombs.remove(bomb)
                    break

        # Check if all cities are destroyed
        if len(cities) == 0:
            game_over = True

        # Check if all bombs are destroyed
        if len(bombs) == 0:
            if level < len(levels) - 1:
                level += 1
                score += 1
                cities.clear()
                missiles.clear()
                bombs.clear()
                create_cities(levels[level]["cities"])
            else:
                game_over = True

    # Update the screen
    screen.fill(BLACK)

    # Draw the cities
    for city in cities:
        pygame.draw.rect(screen, WHITE, city)

    # Draw the missiles
    for missile in missiles:
        pygame.draw.rect(screen, WHITE, missile)

    # Draw the bombs
    for bomb in bombs:
        pygame.draw.circle(screen, RED, (bomb.x, bomb.y), 5)

    # Draw the score and level
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, WHITE)
    level_text = pygame.font.Font(None, 36).render(f"Level: {level + 1}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    # Draw game over text if the game is over
    if game_over:
        game_over_text = pygame.font.Font(None, 72).render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        restart_text = pygame.font.Font(None, 36).render("Click to restart", True, WHITE)
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, (HEIGHT - restart_text.get_height()) // 2 + 100))

    pygame.display.flip()

# Quit the game
pygame.quit()

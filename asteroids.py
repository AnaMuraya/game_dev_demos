import pygame
import math
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

# Load images
player_image = pygame.image.load("assets/apple.jpg")
asteroid_image = pygame.image.load("assets/image8.jpg")

# Player constants
player_size = player_image.get_size()
player_radius = max(player_size) // 2
player_speed = 5
player_rotation_speed = 5

# Asteroid constants
asteroid_min_speed = 1
asteroid_max_speed = 4
asteroid_min_size = 30
asteroid_max_size = 60
asteroid_spawn_delay = 1000

# Laser constants
laser_lifetime = 50  # Lifespan of lasers in frames
laser_speed = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the player
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
player_angle = 0

# Create a list to store the asteroids
asteroids = []
asteroid_spawn_time = pygame.time.get_ticks()

# Create a list to store the lasers
lasers = []

# Create a font object for rendering text
score_font = pygame.font.Font(None, 36)

# Game variables
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= player_rotation_speed
    if keys[pygame.K_RIGHT]:
        player_angle += player_rotation_speed
    if keys[pygame.K_SPACE]:
        lasers.append({
            'position': player_pos + pygame.Vector2(math.cos(math.radians(player_angle)), -math.sin(math.radians(player_angle))) * player_radius,
            'velocity': pygame.Vector2(math.cos(math.radians(player_angle)), -math.sin(math.radians(player_angle))) * laser_speed,
            'life': laser_lifetime
        })

    # Move the player
    direction = pygame.Vector2(math.cos(math.radians(player_angle)), -math.sin(math.radians(player_angle)))
    if keys[pygame.K_UP]:
        player_pos += direction * player_speed

    # Update the screen
    screen.fill(BLACK)

    # Draw the player
    rotated_player = pygame.transform.rotate(player_image, player_angle)
    player_rect = rotated_player.get_rect(center=player_pos)
    screen.blit(rotated_player, player_rect)

    # Spawn asteroids
    current_time = pygame.time.get_ticks()
    if current_time - asteroid_spawn_time >= asteroid_spawn_delay:
        size = random.randint(asteroid_min_size, asteroid_max_size)
        speed = random.uniform(asteroid_min_speed, asteroid_max_speed)
        angle = random.uniform(0, 360)
        position = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        velocity = pygame.Vector2(math.cos(math.radians(angle)), -math.sin(math.radians(angle))) * speed
        asteroids.append((position, velocity, size))
        asteroid_spawn_time = current_time

    # Update and draw the asteroids
    for asteroid in asteroids:
        position, velocity, size = asteroid
        position += velocity
        asteroid_rect = asteroid_image.get_rect(center=position)
        screen.blit(pygame.transform.scale(asteroid_image, (size, size)), asteroid_rect)
        asteroid_rect.inflate_ip(-20, -20)
        if player_rect.colliderect(asteroid_rect):
            running = False

    # Update and draw the lasers
    for laser in lasers:
        laser['position'] += laser['velocity']
        pygame.draw.circle(screen, WHITE, laser['position'], 2)
        laser['life'] -= 1
        if laser['life'] <= 0:
            lasers.remove(laser)

    # Check for collisions between lasers and asteroids
    for laser in lasers:
        for asteroid in asteroids:
            position, _, size = asteroid
            asteroid_rect = pygame.Rect(position, (size, size))
            if asteroid_rect.collidepoint(laser['position']):
                score += 1
                asteroids.remove(asteroid)
                lasers.remove(laser)
                break

    # Render and draw the player's score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Quit the game
pygame.quit()

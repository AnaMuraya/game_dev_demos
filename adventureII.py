import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Adventures of Alex")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player properties
player_width, player_height = 50, 50
player_x, player_y = 50, screen_height - player_height - 50
player_speed = 5
jump_force = 20
gravity = 0.1

# Platform properties
platform_width, platform_height = 94, 94
platforms = []
num_platforms = 6
previous_platform_y = screen_height - player_height - 50
for i in range(num_platforms):
    platform_x = random.randint(50, screen_width - platform_width - 50)
    platform_y = random.randint(100, screen_height - platform_height - 50)
    platforms.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))


# Gem properties
gem_width, gem_height = 30, 30
random_platform_number = random.randint(1,5)
random_platform = platforms[random_platform_number]
random_gemx = random.randint(random_platform.x-jump_force, random_platform.x+random_platform.width+jump_force)
random_gemy = random.randint(random_platform.y-player_height-jump_force, random_platform.y-player_height)
gem_x = random_gemx
gem_y = random_gemy
gem_rect = pygame.Rect(gem_x, gem_y, gem_width, gem_height)

# Game variables
score = 0
lives = 3
level = 1
start_time = time.time()
time_limit = 10  #

# Load images
player_img = pygame.image.load("adventureAssets/player.png")
platform_img = pygame.image.load("adventureAssets/grass.png")
gem_img = pygame.image.load("adventureAssets/treasure.png")
background_img = pygame.image.load("adventureAssets/jungleBackground.jpg")

# Resize images
player_img = pygame.transform.scale(player_img, (player_width, player_height))
platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))
gem_img = pygame.transform.scale(gem_img, (gem_width, gem_height))
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Load the sound effects
game_over = pygame.mixer.Sound("assets/gameover.wav")
gem_sound = pygame.mixer.Sound("assets/ding.mp3")
win_sound = pygame.mixer.Sound("assets/won.wav")
background_music = pygame.mixer.Sound("assets/background.wav")

# Game loop
running = True
clock = pygame.time.Clock()

is_jumping = False
jump_count = 0

while running:
    clock.tick(60)  # Set the frame rate

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                jump_count = jump_force


    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed


    # Jumping
    if is_jumping:
        player_y -= jump_count
        jump_count -= 1

        if jump_count < 0:
            is_jumping = False

    # Apply gravity
    player_y += gravity

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    # gem_rect = pygame.Rect(gem_x, gem_y, gem_width, gem_height)

    for platform in platforms:
        if player_rect.colliderect(platform):
            player_y = platform.y - player_height
            gravity = 0
            jump_count = 0
            break

    if player_rect.colliderect(gem_rect):
        gem_sound.play()
        score += 10
        # gem_x, gem_y = random.randint(50, screen_width - gem_width - 50), random.randint(50, screen_height - gem_height - 50)
        random_platform_number = random.randint(1,5)
        random_platform = platforms[random_platform_number]
        random_gemx = random.randint(random_platform.x-jump_force, random_platform.x+random_platform.width+jump_force)
        random_gemy = random.randint(random_platform.y-player_height-jump_force, random_platform.y-player_height)
        gem_x = random_gemx
        gem_y = random_gemy
        gem_rect = pygame.Rect(gem_x, gem_y, gem_width, gem_height)

    # Apply gravity
    if player_y < screen_height - player_height:
        gravity += 0.2
    else:
        player_y = screen_height - player_height
        gravity = 0

    # Check if the time limit has been reached
    elapsed_time = time.time() - start_time
    if elapsed_time >= time_limit:
        if score < 10:
            # play game over sound than after 2 seconds quit the game
            game_over.play()
            time.sleep(2)
            running = False
        else:
            # win_sound.play()
            # time.sleep(5)

             #Update the level if the score is greater than 10
            level += 1
            score = 0
            start_time = time.time()

            if level == 2:
                background_img = pygame.image.load("adventureAssets/forestBackground.jpg")
                platform_img = pygame.image.load("adventureAssets/wood.png")
                # player_img = pygame.image.load("adventureAssets/player.png")
                gem_img = pygame.image.load("adventureAssets/coin.png")
            elif level == 3:
                background_img = pygame.image.load("adventureAssets/mountainsBackground.jpg")
                platform_img = pygame.image.load("adventureAssets/rocks.png")
                player_img = pygame.image.load("adventureAssets/rabbit.png")
                gem_img = pygame.image.load("adventureAssets/carrot.png")
            
            platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))
            background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
            player_img = pygame.transform.scale(player_img, (player_width, player_height))
            gem_img = pygame.transform.scale(gem_img, (gem_width, gem_height))
            player_rect = pygame.Rect(50, screen_height - player_height - 50, player_width, player_height)


    # Update the display
    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))

    # background_music.play()
    screen.blit(player_img, (player_x, player_y))
    for platform in platforms:
        screen.blit(platform_img, platform)
    screen.blit(gem_img, (gem_x, gem_y))

    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, BLUE)
    lives_text = font.render("Time: " + str(int(time.time() - start_time)), True, RED)
    level_text = font.render("Level: " + str(level), True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (10, 90))

    pygame.display.flip()

pygame.quit()

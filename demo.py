#Initialize pygame
import pygame
import random
import time

pygame.init()

#Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Adventure Two")

#Set up the colors
black = (0, 0, 0)
white = (255, 255, 255)
teal = (0, 128, 128)
red = (255, 0, 0)

#Set up the platforms
platform_width = 94
platform_height = 94
platforms = []
num_platforms = 6
for i in range(num_platforms):
    platform_x = random.randint(0, screen_width - platform_width)
    platform_y = random.randint(platform_height, screen_height - platform_height)
    platforms.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))

#Set up the player
player_width = 48
player_height = 48
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height
player_speed = 5
jumping_force = 20
gravity = 1

#Set up the treasure
treasure_width = 48
treasure_height = 48
random_platform_number = random.randint(0, num_platforms - 1)
random_platform = platforms[random_platform_number]
random_treasure_x = random.randint(random_platform.x - jumping_force, random_platform.x + jumping_force)
random_treasure_y = random.randint(random_platform.y - jumping_force, random_platform.y + jumping_force)
treasure_x = random_treasure_x
treasure_y = random_treasure_y
treasure_Rect = pygame.Rect(treasure_x, treasure_y, treasure_width, treasure_height)

#Load the images
platform_img = pygame.image.load("adventureAssets/grass.png")
treasure_img = pygame.image.load("adventureAssets/treasure.png")
player_img = pygame.image.load("adventureAssets/player.png")
background_img = pygame.image.load("adventureAssets/jungleBackground.jpg")


#Resize images
platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))
treasure_img = pygame.transform.scale(treasure_img, (treasure_width, treasure_height))
player_img = pygame.transform.scale(player_img, (player_width, player_height))
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

#Load the sound effects
game_over_sound = pygame.mixer.Sound("assets/gameover.wav")
win_sound = pygame.mixer.Sound("assets/won.wav")
treasure_sound = pygame.mixer.Sound("assets/ding.mp3")

#Set up game variables
score = 0
start_time = time.time()
time_limit = 10  # 10 seconds
level = 1

#Main loop
running = True
clock = pygame.time.Clock()

is_jumping = False
jumping_count = 0

while running:
    #Handle the frame rate
    clock.tick(60)

    #Handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Handle jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                jumping_count = jumping_force

    #Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    #Check if the player is jumping
    if is_jumping:
        player_y -= jumping_count
        jumping_count -= 1

        if jumping_count < 0:
            is_jumping = False

    #Apply gravity
    player_y += gravity

    #Check if the player is on a platform
    player_Rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for platform in platforms:
        if player_Rect.colliderect(platform):
            player_y = platform.y - player_height
            gravity = 0
            jumping_count = 0
            break

    #Check if the player collides with the treasure
    if player_Rect.colliderect(treasure_Rect):
        treasure_sound.play()
        score += 1
        treasure_x = random.randint(0, screen_width - treasure_width)
        treasure_y = random.randint(0, screen_height - treasure_height)
        treasure_Rect = pygame.Rect(treasure_x, treasure_y, treasure_width, treasure_height)

    #Check if the player goes off the screen
    if player_y < screen_height - player_height:
        gravity += 0.2
    else:
        player_y = screen_height - player_height
        gravity = 0

    #Check if the time limit has been reached
    elapsed_time = time.time() - start_time
    if elapsed_time > time_limit:
        if score < 1:
            game_over_sound.play()
            time.sleep(3)
            running = False
        else:
            level += 1
            score = 0
            start_time = time.time()

            time_limit *= 0.5

            # Decrease the platform width on level increase
            platform_width -= 10

            # Generate new platforms with updated width
            platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))

            platforms = []
            for i in range(num_platforms):
                platform_x = random.randint(0, screen_width - platform_width)
                platform_y = random.randint(platform_height, screen_height - platform_height)
                platforms.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))


            background_img = pygame.image.load(f"adventureAssets/jungleBackground{level}.jpg")
            background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Set up the background
    screen.blit(background_img, (0, 0))

    # Draw the platforms
    for platform in platforms:
        screen.blit(platform_img, platform)
    # Draw the treasure
    screen.blit(treasure_img, treasure_Rect)
    # Draw the player
    screen.blit(player_img, (player_x, player_y))

    # Draw the score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, white)
    time_text = font.render("Time: " + str(int(time.time() - start_time)), True, white)
    levels_text = font.render("Level: " + str(level), True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 50))
    screen.blit(levels_text, (10, 90))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()

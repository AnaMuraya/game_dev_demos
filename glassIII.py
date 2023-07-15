import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Drop Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Background image
background_image = pygame.image.load("glassAssets/background1.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set up the glass
glass_image = pygame.image.load("glassAssets/glass.png")
broken_glass_image = pygame.image.load("glassAssets/brokenGlass.png")
glass_width = 100
glass_height = 20
glass_x = (WIDTH - glass_width) // 2
glass_y = (HEIGHT - glass_height) // 2
glass_speed = 5

# Set up animal variables
animals = []
animal_weights = [10, 20, 30, 40, 50]
animal_images = [
    pygame.image.load("glassAssets/animal1.png"),
    pygame.image.load("glassAssets/animal2.png"),
    pygame.image.load("glassAssets/animal3.png"),
    pygame.image.load("glassAssets/animal4.png"),
    pygame.image.load("glassAssets/animal5.png")
]
animal_width = 100
animal_height = 100
animal_speed = 3
animal_spawn_delay = 1000  # in milliseconds
last_spawn_time = pygame.time.get_ticks()

# Set up game variables
score = 0
weight_limit = 100
game_over = False
weight_on_glass = 0

# Time challenge variables
time_limit = 10  # Time limit in seconds for each time challenge
challenge_active = False
challenge_start_time = 0
challenge_score = 0
challenge_target = 10  # Number of animals to catch in the time challenge

# Load font
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def spawn_animal():
    animal_image = random.choice(animal_images)
    animal_x = random.randint(0, WIDTH - animal_width)
    animal_y = 0
    animal_weight = random.choice(animal_weights)
    animals.append((animal_image, animal_x, animal_y, animal_weight))

def draw_glass():
    if weight_on_glass > weight_limit:
        window.blit(broken_glass_image, (glass_x, glass_y))
    else:
        window.blit(glass_image, (glass_x, glass_y))

def draw_animals():
    for animal in animals:
        window.blit(animal[0], (animal[1], animal[2]))

def update_animals():
    updated_animals = []
    for animal in animals:
        updated_animal = list(animal)
        animal_x, animal_y = updated_animal[1], updated_animal[2]
        if (
            animal_y + animal_height >= glass_y
            and animal_y + animal_height <= glass_y + glass_height
            and (
                (animal_x >= glass_x and animal_x <= glass_x + glass_width)
                or (animal_x + animal_width >= glass_x and animal_x + animal_width <= glass_x + glass_width)
            )
        ):
            updated_animal[2] = glass_y - animal_height
    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and glass_x > 0:
                updated_animal[1] -= glass_speed
            if keys[pygame.K_RIGHT] and glass_x < WIDTH - glass_width:
                updated_animal[1] += glass_speed
        else:
            updated_animal[2] += animal_speed
        updated_animals.append(updated_animal)
    animals[:] = updated_animals

def display_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

def display_weight():
    weight_text = font.render("Weight: " + str(get_total_weight()), True, WHITE)
    window.blit(weight_text, (10, 50))

def get_total_weight():
    if animals:
        return animals[-1][3]
    else:
        return 0

def display_total_glass_weight():
    weight_text = font.render("Total Weight: " + str(weight_on_glass), True, WHITE)
    window.blit(weight_text, (10, 90))

def check_collision():
    global game_over, weight_on_glass, score

    weight_on_glass = 0
    current_score = 0

    for animal in animals:
        animal_x, animal_y = animal[1], animal[2]
        if (
            animal_y + animal_height >= glass_y
            and animal_y + animal_height <= glass_y + glass_height
            and (
                (animal_x >= glass_x and animal_x <= glass_x + glass_width)
                or (animal_x + animal_width >= glass_x and animal_x + animal_width <= glass_x + glass_width)
            )
        ):
            weight_on_glass += animal[3]
            current_score += 1


    if weight_on_glass > weight_limit:
        game_over = True
    else:
        score = current_score

def display_time_left(time_left):
    time_text = font.render("Time Left: " + str(time_left), True, WHITE)
    window.blit(time_text, (WIDTH - 150, 10))

def start_time_challenge():
    global challenge_active, challenge_start_time, challenge_score, score
    challenge_active = True
    challenge_start_time = pygame.time.get_ticks()
    challenge_score = score
    score = 0

def end_time_challenge():
    global challenge_active, challenge_score
    challenge_active = False
    score = challenge_score

def game_loop():
    global game_over, last_spawn_time, score, glass_x

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and glass_x > 0:
            glass_x -= glass_speed
        if keys[pygame.K_RIGHT] and glass_x < WIDTH - glass_width:
            glass_x += glass_speed

        window.fill(BLACK)
        window.blit(background_image, (0, 0))

        if challenge_active:
            time_left = time_limit - (pygame.time.get_ticks() - challenge_start_time) // 1000
            if time_left <= 0:
                end_time_challenge()
                continue
            else:
                if pygame.time.get_ticks() - last_spawn_time > animal_spawn_delay:
                    spawn_animal()
                    last_spawn_time = pygame.time.get_ticks()
            display_time_left(time_left)
        else:
            start_time_challenge()
            if pygame.time.get_ticks() - last_spawn_time > animal_spawn_delay:
                spawn_animal()
                last_spawn_time = pygame.time.get_ticks()
                # if len(animals) >= challenge_target:
                #     start_time_challenge()

        check_collision()
        update_animals()
        draw_glass()
        draw_animals()
        display_score()
        display_weight()
        display_total_glass_weight()

        pygame.display.update()
        clock.tick(60)

        if game_over:
            pygame.time.delay(3000)

            window.fill(BLACK)
            game_over_text = font.render("Game Over", True, WHITE)
            final_score_text = font.render("Final Score: " + str(score), True, WHITE)
            window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            window.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(3000)

    pygame.quit()

game_loop()

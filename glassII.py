import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Drop Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Background image
background_image = pygame.image.load("glassAssets/background4.jpg")
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
time_limit = 30  # Time limit in seconds
start_time = pygame.time.get_ticks()  # Get the start time of the game
# animal_count_limit = 3

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
            updated_animal[2] = glass_y - animal_height  # Set y-coordinate to glass's y-coordinate minus animal's height
    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and glass_x > 0:
                updated_animal[1] -= glass_speed  # Move the animal left with the glass
            if keys[pygame.K_RIGHT] and glass_x < WIDTH - glass_width:
                updated_animal[1] += glass_speed  # Move the animal right with the glass
        else:
            updated_animal[2] += animal_speed  # Move animal downwards
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
        return animals[-1][3]  # Return the weight of the last animal in the list
    else:
        return 0  # If no animals have been spawned, return 0

def display_total_glass_weight():
    weight_text = font.render("Total Weight: " + str(weight_on_glass), True, WHITE)
    window.blit(weight_text, (10, 90))

def check_collision():
    global game_over, weight_on_glass, score

    weight_on_glass = 0  # Reset the weight on glass for each iteration
    current_score = 0  # Reset the current score for each iteration
    
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

def display_time():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate elapsed time in seconds
    remaining_time = max(0, time_limit - elapsed_time)  # Calculate remaining time by subtracting elapsed time from the time limit
    time_text = font.render("Time: " + str(remaining_time) + " seconds", True, WHITE)
    window.blit(time_text, (10, 130))

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

        window.blit(background_image, (0, 0))  # Blit the background image again before game over screen

        if pygame.time.get_ticks() - last_spawn_time > animal_spawn_delay:
            spawn_animal()
            last_spawn_time = pygame.time.get_ticks()

        check_collision()
        update_animals()
        draw_glass()
        draw_animals()
        display_score()
        display_weight()
        display_total_glass_weight()
        display_time()

        pygame.display.update()
        clock.tick(60)

        # Check if the time limit has been reached
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate elapsed time in seconds
        if elapsed_time >= time_limit:
            game_over = True

        if game_over:
            # Pause for 3 seconds to show the broken glass image
            pygame.time.delay(3000)

            # Game over screen
            window.fill(BLACK)
            game_over_text = font.render("Game Over", True, WHITE)
            final_score_text = font.render("Final Score: " + str(score), True, WHITE)
            elapsed_time_text = font.render("Time: " + str(elapsed_time) + " seconds", True, WHITE)
            window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            window.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
            window.blit(elapsed_time_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
            pygame.display.update()
            pygame.time.wait(3000)

    pygame.quit()

# Start the game
game_loop()

#initialization
import pygame
import random

pygame.init()

#Set up the drawing window
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animal Drop Game")

#Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Set up glass variables
glass_image = pygame.image.load("glassAssets/glass.png")
broken_glass_image = pygame.image.load("glassAssets/brokenGlass.png")
glass_width = 100
glass_height = 20
glass_x = (width - glass_width) // 2
glass_y = (height - glass_height) // 2
glass_speed = 5

#Set up animal variables
animals = []
animal_weights = [10, 20, 30, 40, 50]
animal_images = [
    pygame.image.load("glassAssets/animal1.png"),
    pygame.image.load("glassAssets/animal2.png"),
    pygame.image.load("glassAssets/animal3.png"),
    pygame.image.load("glassAssets/animal4.png"),
    pygame.image.load("glassAssets/animal5.png"),
]
animal_width = 100
animal_height = 100
animal_speed = 3
animal_spawn_delay = 1000
last_spawn_time = pygame.time.get_ticks()

#Set up game variables
score = 0
weight_limit = 100
weight_on_glass = 0
running = True

font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

def spawn_animal():
    animal_image = random.choice(animal_images)
    animal_x = random.randint(0, width - animal_width)
    animal_y = 0
    animal_weight = random.choice(animal_weights)
    animals.append((animal_image, animal_x, animal_y, animal_weight))

def draw_animals():
    for animal in animals:
        screen.blit(animal[0], (animal[1], animal[2]))

def update_animals():
    updated_animals = []
    for animal in animals:
        updated_animal = list(animal)
        animal_y = updated_animal[2]
        animal_x = updated_animal[1]

        if (
            animal_y + animal_height >= glass_y
            and animal_y + animal_height <= glass_y + glass_height
            and (
                (animal_x >= glass_x and animal_x <= glass_x + glass_width)
                or (animal_x + animal_width >= glass_x and animal_x + animal_width <= glass_x + glass_width)
            )
        ):
            updated_animal[2] = glass_y - animal_height
        else:
            updated_animal[2] += animal_speed
        
        updated_animals.append(updated_animal)
    animals[:] = updated_animals

def draw_glass():
    if weight_on_glass > weight_limit:
        screen.blit(broken_glass_image, (glass_x, glass_y))
    else:
        screen.blit(glass_image, (glass_x, glass_y))

def check_for_collisions():
    global weight_on_glass, running

    weight_on_glass = 0
    for animal in animals:
        animal_x = animal[1]
        animal_y = animal[2]
        if(
            animal_y + animal_height >= glass_y
            and animal_y + animal_height <= glass_y + glass_height
            and (
                (animal_x >= glass_x and animal_x <= glass_x + glass_width)
                or (animal_x + animal_width >= glass_x and animal_x + animal_width <= glass_x + glass_width)
            )
        ):
            weight_on_glass += animal[3]

    if weight_on_glass > weight_limit:
        running = False

def display_score():
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (0, 0))

def display_total_glass_weight():
    text = font.render("Total weight: " + str(weight_on_glass), True, BLACK)
    screen.blit(text, (0, 30))

def get_recent_animal_weight():
    if animals:
        return animals[-1][3]
    else:
        return 0

def display_recent_animal_weight():
    text = font.render("Weight: " + str(get_recent_animal_weight()), True, BLACK)
    screen.blit(text, (0, 60))

#Main loop
while running:
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    #Handle keyboard events
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and glass_x > 0:
        glass_x -= glass_speed
    if key[pygame.K_RIGHT] and glass_x < width - glass_width:
        glass_x += glass_speed

    #Fill the background with white
    screen.fill(WHITE)

    if pygame.time.get_ticks() - last_spawn_time >= animal_spawn_delay:
        spawn_animal()
        last_spawn_time = pygame.time.get_ticks()

    #Draw the animals
    check_for_collisions()
    update_animals()
    draw_glass()
    draw_animals()
    display_score()
    display_recent_animal_weight()
    display_total_glass_weight()

    #Flip the display
    pygame.display.flip()
    clock.tick(60)

    if not running:
        pygame.time.delay(3000)

        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        final_score_text = font.render("Final Score: " + str(score), True, WHITE)
        screen.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
        screen.blit(final_score_text, (width // 2 - 100, height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)


#Done! Time to quit
pygame.quit()
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
        running = True

#Main loop
while running:
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill the background with white
    screen.fill(WHITE)

    #Draw the animals
    check_for_collisions()
    update_animals()
    draw_glass()
    draw_animals()
    spawn_animal()

    #Flip the display
    pygame.display.flip()

#Done! Time to quit
pygame.quit()
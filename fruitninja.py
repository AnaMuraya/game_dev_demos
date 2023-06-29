import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Fruit Ninja")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fruit images
fruit_images = [
    pygame.transform.scale(pygame.image.load(f"assets/image{1}.jpg").convert(), (100, 100)),
    pygame.transform.scale(pygame.image.load(f"assets/image{2}.jpg").convert(), (100, 100)),
    pygame.transform.scale(pygame.image.load(f"assets/image{3}.jpg").convert(), (100, 100))
]

# Fruit class
class Fruit(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, window_width - 50)
        self.rect.y = window_height + random.randint(50, 200)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()

# Create a group to hold the fruit sprites
fruit_group = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill(BLACK)

    # Update and draw fruits
    fruit_group.update()
    fruit_group.draw(window)

    # Check for collisions with fruits
    mouse_pos = pygame.mouse.get_pos()
    for fruit in fruit_group:
        if fruit.rect.collidepoint(mouse_pos):
            fruit.kill()
            score += 1

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    window.blit(text, (20, 20))

    # Spawn new fruits randomly
    if random.randint(0, 100) < 3:
        fruit_image = random.choice(fruit_images)
        new_fruit = Fruit(fruit_image)
        fruit_group.add(new_fruit)

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

# Quit the game
pygame.quit()

import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define player variables
player_size = 30
player_color = BLUE
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5

# Define NPC variables
npc_size = 50
npc_color = WHITE
npc_x = 100
npc_y = 100

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        player_y -= player_speed
    if keys[K_DOWN]:
        player_y += player_speed
    if keys[K_LEFT]:
        player_x -= player_speed
    if keys[K_RIGHT]:
        player_x += player_speed

    # Check collision with NPC
    if (
        player_x < npc_x + npc_size
        and player_x + player_size > npc_x
        and player_y < npc_y + npc_size
        and player_y + player_size > npc_y
    ):
        print("You interacted with the NPC!")

    # Draw the game
    screen.fill(BLACK)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, npc_color, (npc_x, npc_y, npc_size, npc_size))

    pygame.display.flip()

pygame.quit()

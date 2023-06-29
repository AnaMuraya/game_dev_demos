import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Load the card images
card_images = []
for i in range(1, 9):
    image = pygame.image.load(f"assets/image{i}.jpg").convert()
    image = pygame.transform.scale(image, (100, 100))  # Resize the image to match card size
    card_images.append(image)

# Define card properties
CARD_WIDTH = card_images[0].get_width()
CARD_HEIGHT = card_images[0].get_height()
GAP = 10

# Load the sound effects
flip_sound = pygame.mixer.Sound("assets/crash.mp3")
match_sound = pygame.mixer.Sound("assets/ding.mp3")
win_sound = pygame.mixer.Sound("assets/bg_music_1.mp3")

# Create the grid of cards
ROWS = 4
COLS = 4

# Ensure the number of card images matches the number of cards
assert len(card_images) >= ROWS * COLS // 2, "Not enough card images."

cards = []
for row in range(ROWS):
    for col in range(COLS):
        x = col * (CARD_WIDTH + GAP) + GAP
        y = row * (CARD_HEIGHT + GAP) + GAP
        cards.append(pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT))

# Create pairs of image indices for the cards
image_indices = [i // 2 for i in range(ROWS * COLS)]
random.shuffle(image_indices)

# Create a list to keep track of flipped cards
flipped = []

# Create a list to keep track of matched cards
matched = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(flipped) < 2:
                # Get the index of the clicked card
                for i, card in enumerate(cards):
                    if card.collidepoint(event.pos) and i not in flipped and i not in matched:
                        flipped.append(i)
                        flip_sound.play()

    # Update the screen
    screen.fill((255, 255, 255))
    win_sound.play()

    # Draw the cards
    for i, card in enumerate(cards):
        if i in flipped or i in matched:
            image_index = image_indices[i]
            if image_index < len(card_images):
                screen.blit(card_images[image_index], card)
            else:
                pygame.draw.rect(screen, (0, 0, 0), card)  # Draw a solid rectangle if the image index is out of range
        else:
            pygame.draw.rect(screen, (0, 0, 0), card)

    # Check if two cards are flipped
    if len(flipped) == 2:
        index1, index2 = flipped
        if image_indices[index1] == image_indices[index2]:
            matched.extend(flipped)
            match_sound.play()
        flipped = []

    # Check if all cards are matched
    if len(matched) == ROWS * COLS:
        font = pygame.font.Font(None, 36)
        text = font.render("You win!", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

# Quit the game
pygame.quit()

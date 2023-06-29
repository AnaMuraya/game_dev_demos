import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Puzzle Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Puzzle size
puzzle_size = 3

# Load puzzle images
puzzle_images = [
    pygame.image.load(f"assets/image{5}.jpg"),
    pygame.image.load(f"assets/image{5}.jpg"),
    pygame.image.load(f"assets/image{5}.jpg")
]

# Create the puzzle pieces
puzzle_pieces = []
piece_size = window_width // puzzle_size

for row in range(puzzle_size):
    for col in range(puzzle_size):
        piece_image = random.choice(puzzle_images)
        piece_rect = pygame.Rect(col * piece_size, row * piece_size, piece_size, piece_size)
        puzzle_pieces.append((piece_image, piece_rect))

# Shuffle the puzzle pieces
random.shuffle(puzzle_pieces)

# Variables for dragging puzzle pieces
selected_piece = None
offset = None

# Check if the puzzle is solved
def check_win():
    for index, (_, piece_rect) in enumerate(puzzle_pieces):
        correct_position = pygame.Rect(index % puzzle_size * piece_size, index // puzzle_size * piece_size, piece_size, piece_size)
        if piece_rect != correct_position:
            return False
    return True

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if the player clicked on a puzzle piece
                mouse_pos = pygame.mouse.get_pos()
                for piece_image, piece_rect in puzzle_pieces:
                    if piece_rect.collidepoint(mouse_pos):
                        selected_piece = (piece_image, piece_rect)
                        offset = pygame.Vector2(mouse_pos) - piece_rect.topleft
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and selected_piece:
                # Check if the player released a puzzle piece in a valid position
                mouse_pos = pygame.mouse.get_pos()
                for index, (_, piece_rect) in enumerate(puzzle_pieces):
                    if piece_rect.collidepoint(mouse_pos) and piece_rect != selected_piece[1]:
                        puzzle_pieces.remove(selected_piece)
                        puzzle_pieces.insert(index, selected_piece)
                        break
                selected_piece = None
                offset = None

    # Clear the screen
    window.fill(BLACK)

    # Draw the puzzle pieces
    for piece_image, piece_rect in puzzle_pieces:
        window.blit(pygame.transform.scale(piece_image, (piece_size, piece_size)), piece_rect)

    # If a puzzle piece is selected, move it with the mouse cursor
    if selected_piece:
        mouse_pos = pygame.mouse.get_pos()
        selected_piece[1].topleft = mouse_pos - offset

    # Update the display
    pygame.display.flip()

    # Check if the puzzle is solved
    if check_win():
        print("Congratulations! Puzzle solved!")
        running = False

    # Set the frames per second
    clock.tick(60)

# Quit the game
pygame.quit()

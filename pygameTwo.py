import pygame
pygame.init()

display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('My Customized Name')

#Colors to use
white = (255,255,255)
teal = (0,128,128)

#Set the font
font = pygame.font.SysFont('Comicsansms', 25)

#Set the text
name = 'Ana Muraya'
text = font.render(name, True, white)

#Calculate the center of the display to set text position
text_rect = text.get_rect()
text_rect.center = (display_width // 2, display_height // 2)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(teal)  # Set the background color
    screen.blit(text, text_rect)  # Draw the name on the screen
    pygame.display.flip()

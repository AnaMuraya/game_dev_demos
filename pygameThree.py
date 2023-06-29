import pygame
pygame.init()

#Setting the display
display_width = 600
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Drawing a Circle")

#Setting up the player
player_x = display_width//2
player_y = display_height//2
player_radius = 20
player_color = (0, 128, 0)

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #Drawing the background
    screen.fill((255, 255, 255))
    #Drawing the player
    pygame.draw.circle(screen, player_color, (player_x, player_y), player_radius)
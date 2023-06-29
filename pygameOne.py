import pygame #Imports pygame library
pygame.init() #Initializes pygame

#Sets up the display
display_width = 800 #Sets the width of the display in pixels
display_height = 600 #Sets the height of the display in pixels
screen = pygame.display.set_mode((display_width,display_height)) #Sets the display size
pygame.display.set_caption('My First Pygame Project') #Sets the title of the display

#Set the font
font = pygame.font.SysFont('Arial', 25)

#Create a text
text = font.render('Hello World!', True, (0, 128, 0))

#Set the position of the text
text_x = display_width/2
text_y = display_height/2

#Draw the text onto the display
screen.blit(text, (text_x, text_y))

#Update the display
pygame.display.update()

#While loop to check whether the user has quit the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

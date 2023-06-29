#initialize pygame
import pygame
import random
pygame.init()

#Set up display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

#Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
teal = (0, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

#Set up variables
bird_x = 100
bird_y = height // 2
bird_radius = 10
bird_speed = 0
gravity = 0.1
bird_acceleration = 1

pipe_width = 10
pipe_height = random.randint(100, 400)
pipe_gap = 300
pipe_x = width - pipe_width

score = 1

#Set up font for score
font = pygame.font.SysFont("Arial", 30)

#Set up sounds
#Function to reset the pipes
def reset_pipes():
    global pipe_height, pipe_x, score
    pipe_height = random.randint(100, 400)
    pipe_x = width - pipe_width

#Main loop
running = True
while running:
    #Check for events
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -bird_acceleration


    #Move the bird
    bird_speed += gravity
    bird_y += bird_speed

    #Move the pipes
    pipe_x -= 1


    #Top pipe position
    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    #Bottom pipe position
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, height - pipe_height - pipe_gap)
    #Bird position
    bird = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
    #Check for the bird successfully passing through the pipes without colliding, then reset the pipes and add 1 to the score
    if bird_x > pipe_x + pipe_width and not bird.colliderect(top_pipe) and not bird.colliderect(bottom_pipe):
        reset_pipes()
        score += 1
    #Check for collisions with the pipes, ceiling, and floor then reset the pipes, reset the score, and reset the bird
    if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
        reset_pipes()
        score = 0
        bird_x = 100
        bird_y = height // 2
        bird_speed = 0
    #Check for collisions with the ceiling and floor then bounce the bird off of them
    if bird_y < bird_radius or bird_y > height - bird_radius:
        bird_speed *= -1
        bird_speed += gravity

    

    #Clear the screen
    screen.fill(black)

    #Draw the ground
    #Draw the bird
    pygame.draw.circle(screen, yellow, (bird_x, bird_y), bird_radius)

    #Draw the pipes
    pygame.draw.rect(screen, red, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, red, (pipe_x, pipe_height + pipe_gap, pipe_width, height - pipe_height - pipe_gap))

    #Draw the score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width // 2, 50))
    
    #Update the display
    pygame.display.update()
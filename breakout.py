#initialize
import pygame
import random
pygame.init()

#set up display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")

#colors
white = (255, 255, 255)
black = (0, 0, 0)
teal = (0, 255, 255)
red = (255, 0, 0)

#variables
paddle_width = 100
paddle_height = 20
paddle_x = (width - paddle_width) // 2
paddle_y = height - paddle_height - 10
paddle_speed = 3

ball_radius = 10
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 0.5
ball_speed_y = 0.5

brick_width = 100
brick_height = 20
brick_rows = 5
brick_cols = width // brick_width
brick_colors = [white, teal, red]
bricks = []
for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        #randomly choose a color
        color = random.choice(brick_colors)
        #get brick x and y position with a 2 pixel space between bricks and 1 pixel space for the border
        brick_x = 1 + (brick_width + 2) * col
        brick_y = 1 + (brick_height + 2) * row
        #create a rectangle for the brick
        brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        #add the brick to the bricks array/list
        bricks.append((brick_rect, color))



#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
        paddle_x += paddle_speed

    #Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    #Check for wall collisions then bounce it in the opposite direction if it hits a wall
    if ball_x > width - ball_radius or ball_x < ball_radius:
        ball_speed_x *= -1
    if ball_y > height - ball_radius or ball_y < ball_radius:
        ball_speed_y *= -1

    #Check for paddle collisions
    if ball_x > paddle_x and ball_x < paddle_x + paddle_width and ball_y > paddle_y and ball_y < paddle_y + paddle_height:
        ball_speed_y *= -1
        ball_speed_x *= -1

    #Check for brick collisions
    for brick in bricks:
        if ball_x > brick[0].x and ball_x < brick[0].x + brick_width and ball_y > brick[0].y and ball_y < brick[0].y + brick_height:
            bricks.remove(brick)
            ball_speed_y *= -1

    #Clear the screen
    screen.fill(black)

    #Draw everything
    pygame.draw.rect(screen, white, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)
    for brick in bricks:
        pygame.draw.rect(screen, brick[1], brick[0])
    pygame.display.flip()

#Update the screen
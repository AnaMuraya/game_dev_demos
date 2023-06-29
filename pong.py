import pygame
pygame.init()

#Setup the display
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

#Setup the ball
ball_size = 40
ball_x = width//2 - ball_size//2
ball_y = height//2 - ball_size//2
ball_speed_x = 3
ball_speed_y = 3

#Setup the paddles
paddle_width = 20
paddle_height = 60
paddle1_x = 50
paddle2_x = width - 50 - paddle_width
paddle1_y = height//2 - paddle_height//2
paddle2_y = height//2 - paddle_height//2
paddle_speed = 0.5

#Set initial scores
player1_score = 0
player2_score = 0

font = pygame.font.Font('freesansbold.ttf', 32)

#Setup the color
white = (255, 255, 255)
black = (0, 0, 0)

#Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #Make the ball move
    ball_x += ball_speed_x  # ball_x = ball_x + ball_speed_x
    ball_y += ball_speed_y  # ball_y = ball_y + ball_speed_y

    #Check for collisions on the paddles
    if ball_x< paddle1_x + paddle_width and ball_y + ball_size > paddle1_y and ball_y < paddle1_y + paddle_height:
        ball_speed_x = abs(ball_speed_x) #reverse the ball direction

    if ball_x > width - ball_size:
        ball_speed_x = ball_speed_x * -1
    
    if ball_y > width - ball_size:
        ball_speed_y = ball_speed_y * -1

    if ball_x < 0:
        ball_speed_x = ball_speed_x * -1
    
    if ball_y < 0:
        ball_speed_y = ball_speed_y * -1

    #Make the paddles move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed

    if keys[pygame.K_s] and paddle1_y < height - paddle_height:
        paddle1_y += paddle_speed

    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    
    if keys[pygame.K_DOWN] and paddle2_y < height - paddle_height:
        paddle2_y += paddle_speed




    #Draw the background
    screen.fill(black)

    #Draw the ball
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_size)

    #Draw the paddles
    pygame.draw.rect(screen, white, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (paddle2_x, paddle2_y, paddle_width, paddle_height))
    score_text1 = font.render("Player 1: " + str(player1_score), True, white)
    screen.blit(score_text1, (10, 10))
    score_text2 = font.render("Player 2: " + str(player2_score), True, white)
    screen.blit(score_text2, (width - score_text2.get_width() - 10, 10))

    pygame.display.update()
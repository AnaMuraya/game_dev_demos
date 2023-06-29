import pygame
pygame.init()

# Setup the display
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Setup the ball
ball_size = 10
ball_x = width//2 - ball_size//2
ball_y = height//2 - ball_size//2
ball_speed_x = 0.5
ball_speed_y = 0.5

# Setup the paddles
paddle_width = 20
paddle_height = 60
paddle1_x = 50
paddle2_x = width - 50 - paddle_width
paddle1_y = height//2 - paddle_height//2
paddle2_y = height//2 - paddle_height//2
paddle_speed = 0.5

# Setup the scores
score_player1 = 0
score_player2 = 0
font = pygame.font.Font(None, 36)

# Setup the color
white = (255, 255, 255)
black = (0, 0, 0)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Make the ball move
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collision with paddles
    if ball_x < paddle1_x + paddle_width and ball_y + ball_size > paddle1_y and ball_y < paddle1_y + paddle_height:
        ball_speed_x = abs(ball_speed_x)  # Reverse the horizontal direction of the ball
        score_player1 += 1
        ball_x = paddle1_x + paddle_width  # Place the ball just outside the paddle

    if ball_x + ball_size > paddle2_x and ball_y + ball_size > paddle2_y and ball_y < paddle2_y + paddle_height:
        ball_speed_x = -abs(ball_speed_x)  # Reverse the horizontal direction of the ball
        score_player2 += 1
        ball_x = paddle2_x - ball_size  # Place the ball just outside the paddle

    # Check for collision with walls
    if ball_x > width - ball_size or ball_x < 0:
        ball_speed_x = -ball_speed_x

    if ball_y > height - ball_size or ball_y < 0:
        ball_speed_y = -ball_speed_y

    # Make the paddles move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed

    if keys[pygame.K_s] and paddle1_y < height - paddle_height:
        paddle1_y += paddle_speed

    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed

    if keys[pygame.K_DOWN] and paddle2_y < height - paddle_height:
        paddle2_y += paddle_speed

    # Draw the background
    screen.fill(black)

    # Draw the ball
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_size)

    # Draw the paddles
    pygame.draw.rect(screen, white, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (paddle2_x, paddle2_y, paddle_width, paddle_height))

    # Draw the scores
    score_text_player1 = font.render("Player 1: " + str(score_player1), True, white)
    score_text_player2 = font.render("Player 2: " + str(score_player2), True, white)
    screen.blit(score_text_player1, (10, 10))
    screen.blit(score_text_player2, (width - 10 - score_text_player2.get_width(), 10))

    pygame.display.update()
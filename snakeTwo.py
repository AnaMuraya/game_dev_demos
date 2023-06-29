import pygame
import random
import time
from pygame.locals import *
pygame.init()

#set up the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
screen.fill((156, 46, 3))

#load the snake image and paint it on the screen
snake = pygame.image.load("assets/block.jpg").convert()
snake_x = [100, 140, 180]
snake_y = [400, 400, 400]
snake_x_change = 0
snake_y_change = 0
snake_speed = 0.5
snake_length = 3
snake_body = []
screen.blit(snake, (snake_x[0], snake_y[0]))

def draw_snake():
    screen.fill((156, 46, 3))
    screen.blit(snake, (snake_x[0], snake_y[0]))
    pygame.display.flip()

# load the apple image and paint it on the screen randomly
# apple = pygame.image.load("assets/apple.jpg").convert()
# apple_x = random.randint(0, width - 40)
# apple_y = random.randint(0, height - 40)
# screen.blit(apple, (apple_x, apple_y))

pygame.display.flip()

#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False     
            #move the snake
            if event.key == pygame.K_LEFT:
                snake_x_change = -snake_speed
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = snake_speed
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_y_change = -snake_speed
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = snake_speed
                snake_x_change = 0
    
    #update the snake's position
    for i in range(1,snake_length):
        snake_x[i] = snake_x[i-1]
        snake_y[i] = snake_y[i-1]

    snake_x[0] += snake_x_change
    snake_y[0] += snake_y_change
    draw_snake()


    #draw the snake
    for i in range(snake_length):
        screen.blit(snake, (snake_x[i], snake_y[i]))

    # Check for collision with food
    # if snake_x == apple_x and snake_y == apple_y:
    #     apple_x = random.randint(0, (width - 40) // 40) * 40
    #     apple_y = random.randint(0, (height - 40) // 40) * 40
    #     snake_length += 1
    #     snake_x.append(snake_x[snake_length - 2])
    #     snake_y.append(snake_y[snake_length - 2])
    #     screen.blit(apple, (apple_x, apple_y))


    pygame.display.flip()
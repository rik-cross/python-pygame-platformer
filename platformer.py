# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

import pygame

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')

# player
player_image = pygame.image.load('images/vita_00.png')

running = True
while running:
# game loop

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update

    # draw
    screen.fill(DARK_GREY)
    screen.blit(player_image, (300,100))
    pygame.display.flip()

# quit
pygame.quit()
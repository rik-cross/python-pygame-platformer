# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

import pygame

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)
MUSTARD = (209,206,25)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()

# player
player_image = pygame.image.load('images/vita_00.png')
player_x = 300

# platforms
platforms = [
    # middle
    pygame.Rect(100,300,400,50),
    # left
    pygame.Rect(100,250,50,50),
    # right
    pygame.Rect(450,250,50,50)
]

running = True
while running:
# game loop

    # -----
    # INPUT
    # -----

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_player_x = player_x
    
    # player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        new_player_x -= 2
    if keys[pygame.K_d]:
        new_player_x += 2

    # horizontal movement

    new_player_rect = pygame.Rect(new_player_x,200,72,72)
    x_collision = False

    #...check against every platform
    for p in platforms:
        if p.colliderect(new_player_rect):
            x_collision = True
            break

    if x_collision == False:
        player_x = new_player_x

    # update

    # draw

    # background
    screen.fill(DARK_GREY)
    # platforms
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)

    # player
    screen.blit(player_image, (player_x,200))
    # present screen
    pygame.display.flip()

    clock.tick(60)

# quit
pygame.quit()
# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

# Enemy sprite by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

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

player_y = 0
player_speed = 0
player_acceleration = 0.2

player_width = 45
player_height = 51

# platforms
platforms = [
    # middle
    pygame.Rect(100,300,400,50),
    # left
    pygame.Rect(100,250,50,50),
    # right
    pygame.Rect(450,250,50,50)
]

# coins
coin_image = pygame.image.load('images/coin_0.png')
coins = [
    pygame.Rect(100,200,23,23),
    pygame.Rect(200,250,23,23)
]

score = 0

# enemies
enemy_image = pygame.image.load('images/spike_monster.png')
enemies = [
    pygame.Rect(150,274,50,26)
]

lives = 3

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
    new_player_y = player_y
    
    # player input
    keys = pygame.key.get_pressed()
    # a=left
    if keys[pygame.K_a]:
        new_player_x -= 2
    # d=right
    if keys[pygame.K_d]:
        new_player_x += 2
    # w=jump (if on the ground)
    if keys[pygame.K_w] and player_on_ground:
        player_speed = -5

    # ------
    # UPDATE
    # ------

    # horizontal movement

    new_player_rect = pygame.Rect(new_player_x,player_y,player_width,player_height)
    x_collision = False

    #...check against every platform
    for p in platforms:
        if p.colliderect(new_player_rect):
            x_collision = True
            break

    if x_collision == False:
        player_x = new_player_x
    
    # vertical movement

    player_speed += player_acceleration
    new_player_y += player_speed

    new_player_rect = pygame.Rect(player_x,new_player_y,player_width,player_height)
    y_collision = False
    player_on_ground = False

    #...check against every platform
    for p in platforms:
        if p.colliderect(new_player_rect):
            y_collision = True
            player_speed = 0
            # if the platform is below the player
            if p[1] > new_player_y:
                # stick the player to the platform
                player_y = p[1] - player_height
                player_on_ground = True
            break

    if y_collision == False:
        player_y = new_player_y

    # see if any coins have been collected
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in coins:
        if c.colliderect(player_rect):
            coins.remove(c)
            score += 1

    # see if the player has hit an enemy
    for e in enemies:
        if e.colliderect(player_rect):
            lives -= 1
            # reset player position
            player_x = 300
            player_y = 0
            player_speed = 0

    # ----
    # DRAW
    # ----

    # background
    screen.fill(DARK_GREY)

    # platforms
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)

    # coins
    for c in coins:
        screen.blit(coin_image, (c.x, c.y))

    # coins
    for e in enemies:
        screen.blit(enemy_image, (e.x, e.y))

    # player
    screen.blit(player_image, (player_x, player_y))
    # present screen
    pygame.display.flip()

    clock.tick(60)

# quit
pygame.quit()
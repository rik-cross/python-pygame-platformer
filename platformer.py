# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

# Enemy sprite by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

# Heart sprite by Nicole Marie T
# https://opengameart.org/content/heart-1616

import pygame
import engine
import utils

def drawText(t, x, y):
    text = font.render(t, True, MUSTARD, DARK_GREY)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)
    screen.blit(text, text_rectangle)

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)
MUSTARD = (209,206,25)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# game states = playing // win // lose
game_state = 'playing'

entities = []

# images
coin_image = pygame.image.load('images/coin_0.png')
heart_image = pygame.image.load('images/heart.png')

# player
player_speed = 0
player_acceleration = 0.2
score = 0
lives = 3

# platforms
platforms = [
    # middle
    pygame.Rect(100,300,400,50),
    # left
    pygame.Rect(100,250,50,50),
    # right
    pygame.Rect(450,250,50,50)
]

entities.append(utils.makeCoin(100,200))
entities.append(utils.makeCoin(200,250))
entities.append(utils.makeEnemy(150,274))
player = utils.makePlayer(300,0)
entities.append(player)

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

    if game_state == 'playing':

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y
        
        # player input
        keys = pygame.key.get_pressed()
        # a=left
        if keys[pygame.K_a]:
            new_player_x -= 2
            player.direction = 'left'
            player.state = 'walking'
        # d=right
        if keys[pygame.K_d]:
            new_player_x += 2
            player.direction = 'right'
            player.state = 'walking'
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player.state = 'idle'
        # w=jump (if on the ground)
        if keys[pygame.K_w] and player_on_ground:
            player_speed = -5

    # ------
    # UPDATE
    # ------

    if game_state == 'playing':

        # update animations
        for entity in entities:
            entity.animations.animationList[entity.state].update()

        # horizontal movement

        new_player_rect = pygame.Rect(new_player_x,player.position.rect.y,player.position.rect.width,player.position.rect.height)
        x_collision = False

        #...check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player.position.rect.x = new_player_x
        
        # vertical movement

        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pygame.Rect(player.position.rect.x,new_player_y,player.position.rect.width,player.position.rect.height)
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
                    player.position.rect.y = p[1] - player.position.rect.height
                    player_on_ground = True
                break

        if y_collision == False:
            player.position.rect.y = new_player_y

        # see if any coins have been collected
        player_rect = pygame.Rect(player.position.rect.x, player.position.rect.y, player.position.rect.width, player.position.rect.height)

        # collection system
        for entity in entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    entities.remove(entity)
                    score += 1
                    # win if the score is 2
                    if score >= 2:
                        game_state = 'win'

        # enemy system
        for entity in entities:
            if entity.type == 'dangerous':
                if entity.position.rect.colliderect(player_rect):
                    lives -= 1
                    # reset player position
                    player.position.rect.x = 300
                    player.position.rect.y = 0
                    player_speed = 0
                    # change the game state
                    # if no lives remaining
                    if lives <= 0:
                        game_state = 'lose'

    # ----
    # DRAW
    # ----

    # background
    screen.fill(DARK_GREY)

    # platforms
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)

    # draw system
    for entity in entities:
        s = entity.state
        a = entity.animations.animationList[s]
        if entity.direction == 'left':
            a.draw(screen, entity.position.rect.x, entity.position.rect.y, True, False)
        else:
            a.draw(screen, entity.position.rect.x, entity.position.rect.y, False, False)

    # player information display

    # score
    screen.blit(coin_image, (10,10))
    drawText(str(score), 50, 10)

    # lives
    for l in range(lives):
        screen.blit(heart_image, (200 + (l*50),10))

    if game_state == 'win':
        drawText('You win!', 50, 50)
        
    if game_state == 'lose':
        drawText('You lose!', 50, 50)

    # present screen
    pygame.display.flip()

    clock.tick(60)

# quit
pygame.quit()
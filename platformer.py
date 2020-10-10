import pygame

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')

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
    pygame.display.flip()

# quit
pygame.quit()
import pygame
import engine
import pickle

WIDTH = 32*40
HEIGHT = 32*20

offsetX = 0
offsetY = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Level Editor')
clock = pygame.time.Clock()

def convertToMapCoords(pos):
    return (pos[0]//32 + offsetX, pos[1]//32 + offsetY)

map = engine.Map(64,64)

# add tiles
engine.Tile.addTile('platform', engine.Tile(pygame.image.load('images/textures/platform.png'), 'platform', True))

running = True
while running:
# game loop

    for event in pygame.event.get():

        # check for quit
        if event.type == pygame.QUIT:
            running = False

        # get mouse
        ms = pygame.mouse.get_pressed()
        #print(ms)
        
        # left click = place
        if ms[0]:
            pos = pygame.mouse.get_pos()
            mapPos = convertToMapCoords(pos)
            
            if map.map[mapPos[1]][mapPos[0]] is engine.Tile.tiles['none']:
                map.map[mapPos[1]][mapPos[0]] = engine.Tile.tiles['platform']

        # right-click = remove
        if ms[2]:
            pos = pygame.mouse.get_pos()
            mapPos = convertToMapCoords(pos)
            
            if map.map[mapPos[1]][mapPos[0]] is not engine.Tile.tiles['none']:
                map.map[mapPos[1]][mapPos[0]] = engine.Tile.tiles['none']

        if event.type == pygame.KEYUP:

            # save map
            if event.key==pygame.K_s:
                map.saveToFile(input('Enter filename to save to: '))
            
            # load map
            if event.key==pygame.K_l:
                map.loadFromFile(input('Enter file to load: '))

    #
    # draw
    #

    # clear screen
    screen.fill((0,0,0))

    # draw map
    map.draw(screen, offsetX*32, offsetY*32, 1)

    # draw grid lines
    for r in range(32,HEIGHT,32):
        pygame.draw.line(screen, engine.DARK_GREY, (0,r), (WIDTH,r), 1)
    for c in range(32,WIDTH,32):
        pygame.draw.line(screen, engine.DARK_GREY, (c,0), (c,HEIGHT), 1)

    pygame.display.flip()
    clock.tick(60)

# quit
pygame.quit()
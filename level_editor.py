import pygame
import engine
import pickle
import game_tiles
import utils

WIDTH = 32*32 + 250
HEIGHT = 32*16

MAPWIDTH = 32*32
MAPHEIGHT = 32*16

offsetX = 0
offsetY = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Level Editor')
clock = pygame.time.Clock()

def convertToMapCoords(pos):
    return ((pos[0] - offsetX*map.tileSize)//map.tileSize, (pos[1] - offsetY*map.tileSize)//map.tileSize)

map = engine.Map()

tiles = []
y = 50
x = MAPWIDTH + 50
for t in engine.Tile.tiles:
    tiles.append([t, engine.Tile.tiles[t], x, y])
    y += 50

running = True
while running:
# game loop

    for event in pygame.event.get():

        # check for quit
        if event.type == pygame.QUIT:
            running = False

        # get mouse click position
        ms = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        
        # left click
        if ms[0]:
            
            # place tile
            if pos[0] < MAPWIDTH and pos[1] < MAPHEIGHT:

                mapPos = convertToMapCoords(pos)

                if mapPos[0] >= 0 and mapPos[1] >= 0:                
                    if map.map[mapPos[1]][mapPos[0]] == 'none':
                        map.map[mapPos[1]][mapPos[0]] = 'platform'
                        map.setDimensions()

        # right click
        if ms[2]:
            
            # remove tile
            if pos[0] < MAPWIDTH and pos[1] < MAPHEIGHT:
                mapPos = convertToMapCoords(pos)
                
                if mapPos[0] >= 0 and mapPos[1] >= 0:
                    if map.map[mapPos[1]][mapPos[0]] != 'none':
                        map.map[mapPos[1]][mapPos[0]] = 'none'
                        map.setDimensions()

        if event.type == pygame.KEYUP:

            # save map
            if event.key==pygame.K_s:
                filename = input('Enter filename to save to: ')
                filename = 'levels/' + filename + '.lvl'
                pickle.dump( map, open( filename, "wb" ) )
            
            # load map
            if event.key==pygame.K_l:
                filename = input('Enter file to load: ')
                filename = 'levels/' + filename + '.lvl'
                map = pickle.load( open( filename, "rb" ) )

            # smaller tiles
            if event.key==pygame.K_MINUS:
                map.tileSize = max(8, int(map.tileSize/2))
                map.setDimensions()

            # larger tiles
            if event.key==pygame.K_EQUALS:
                map.tileSize = min(64, int(map.tileSize*2))
                map.setDimensions()

            # up
            if event.key==pygame.K_UP:
                offsetY = min(0, offsetY+1)
            # down
            if event.key==pygame.K_DOWN:
                offsetY -= 1
            # left
            if event.key==pygame.K_LEFT:
                offsetX = min(0, offsetX+1)
            # right
            if event.key==pygame.K_RIGHT:
                offsetX -= 1

    #
    # draw
    #

    # clear screen
    screen.fill((0,0,0))

    # set clip
    screen.set_clip(pygame.rect.Rect(0,0,MAPWIDTH,MAPHEIGHT))

    # draw map background
    pygame.draw.rect(screen, (20,20,20), pygame.rect.Rect(offsetX*map.tileSize,offsetY*map.tileSize,map.w_real,map.h_real))

    # draw map
    map.draw(screen, offsetX*map.tileSize, offsetY*map.tileSize, 1)

    screen.set_clip(None)

    # draw grid lines
    for r in range(map.tileSize, MAPHEIGHT+map.tileSize, map.tileSize):
        pygame.draw.line(screen, (engine.DARK_GREY), (0,r), (MAPWIDTH, r), 1)
    for c in range(map.tileSize, MAPWIDTH+map.tileSize, map.tileSize):
        pygame.draw.line(screen, engine.DARK_GREY, (c,0), (c,MAPHEIGHT), 1)

    # draw tiles
    for t in tiles:
        pygame.draw.rect(screen, (40,40,40), pygame.rect.Rect(t[2],t[3],32,32))
        t[1].draw(screen, t[2], t[3], 32, 32)
        utils.drawText(screen, t[0], t[2]+50, t[3], (255,255,255), 255)

    pygame.display.flip()
    clock.tick(60)

# quit
pygame.quit()
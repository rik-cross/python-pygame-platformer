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

def loadMap():
    pass

def saveMap():
    pass

def convertToMapCoords(pos):
    return (pos[0]//32 + offsetX, pos[1]//32 + offsetY)

map = [ [ None for w in range(64) ] for h in range(64) ]

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
            
            if map[mapPos[1]][mapPos[0]] is None:
                map[mapPos[1]][mapPos[0]] = engine.material_platform

        # right-click = remove
        if ms[2]:
            pos = pygame.mouse.get_pos()
            mapPos = convertToMapCoords(pos)
            
            if map[mapPos[1]][mapPos[0]] is not None:
                map[mapPos[1]][mapPos[0]] = None

        if event.type == pygame.KEYUP:

            # save map
            if event.key==pygame.K_s:
                filename = input('Enter filename to save to: ')
                filename = 'levels/' + filename + '.lvl'

                mapToSave = []
                for r in range(len(map)):
                    rowToSave = []
                    for c in map[r]:
                        rowToSave.append(engine.materialToString[c])
                    mapToSave.append(rowToSave)

                pickle.dump( mapToSave, open( filename, "wb" ) )

            
            # load map
            if event.key==pygame.K_l:
                filename = input('Enter file to load: ')
                filename = 'levels/' + filename + '.lvl'
                mapToLoad = pickle.load( open( filename, "rb" ) )

                map = []
                for r in range(len(mapToLoad)):
                    row = []
                    for c in mapToLoad[r]:
                        row.append(engine.stringToMaterial[c])
                    map.append(row)
                

    # draw map

    for r in range(64):
        for c in range(64):
            material = map[r][c]
            newX = (offsetX*32) + (c*32)
            newY = (offsetY*32) + (r*32)
            if material is not None: 
                #newWidth = int(material.texture.get_rect().w * z)
                #newHeight = int(material.texture.get_rect().h * z)
                material.draw(screen, newX, newY, 32, 32)
            else:
                pygame.draw.rect(screen, (0,0,0), (newX,newY,32,32))


    # draw grid

    for r in range(32,HEIGHT,32):
        pygame.draw.line(screen, engine.DARK_GREY, (0,r), (WIDTH,r), 1)
    for c in range(32,WIDTH,32):
        pygame.draw.line(screen, engine.DARK_GREY, (c,0), (c,HEIGHT), 1)

    pygame.display.flip()
    
    clock.tick(60)

# quit
pygame.quit()
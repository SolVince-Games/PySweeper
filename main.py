# ~ Imports ~ #
import pygame
import random
import os

# Inits
pygame.init()
clock = pygame.time.Clock()

# Create window
global display_width,display_height

def setSize(x: int,y: int):
    global display_width,display_height
    (display_width,display_height) = (x,y)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    return pygame.display.set_mode((display_width, display_height))

def setScale(scale: int):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    return pygame.display.set_mode((scale*display_width, scale*display_height))

# display = setSize(152,81)
display = setSize(280,323)
setScale(1)
pygame.display.set_caption('PySweeper')




# Load assets
screen = pygame.Surface((display_width,display_height))

pieces = {
    "0":pygame.image.load(f'images/0.png').convert_alpha(),
    "1":pygame.image.load(f'images/1.png').convert_alpha(),
    "2":pygame.image.load(f'images/2.png').convert_alpha(),
    "3":pygame.image.load(f'images/3.png').convert_alpha(),
    "4":pygame.image.load(f'images/4.png').convert_alpha(),
    "5":pygame.image.load(f'images/5.png').convert_alpha(),
    "6":pygame.image.load(f'images/6.png').convert_alpha(),
    "7":pygame.image.load(f'images/7.png').convert_alpha(),
    "8":pygame.image.load(f'images/8.png').convert_alpha(),
    "b":pygame.image.load(f'images/bomb.png').convert_alpha(),
    "f":pygame.image.load(f'images/flag.png').convert_alpha(),
    "h":pygame.image.load(f'images/hidden.png').convert_alpha()
}

sounds = {
    # "":pygame.mixer.Sound('sounds/.mp3')
}




# Load controls
controls = {
    "quit": {pygame.K_ESCAPE},
    "mode": {pygame.K_SPACE}
}


# Define variables

frameRate = 60

global mapWidth,mapHeight,totalBombs,flagged
global spriteGroup,mode
global running,closed,replay

def resetVars():
    global mapWidth,mapHeight,totalBombs,flagged,running,closed,replay,sprites,spriteGroup,mode
    mapWidth = 16
    mapHeight = 16
    totalBombs = 40
    flagged = 0
    running = True
    closed = False
    replay = True
    sprites = []
    spriteGroup = pygame.sprite.Group()
    mode = 'clear'
resetVars()




# Map storage

tileMap = []
def clearMap():
    global tileMap
    tileMap = []
    for row in range(mapHeight):
        column = []
        for x in range(mapWidth):
            column.append('0h')
        tileMap.append(column)

def setTileonMap(x,y, value):
    try:
        if x < 0 or x >= mapWidth or y < 0 or y >= mapHeight:
            return 'Out of Bounds'
        tileMap[y][x] = value
        return value
    except IndexError:
        return 'Out of Bounds'

def getTileonMap(x,y) -> str:
    try:
        if x < 0 or x >= mapWidth or y < 0 or y >= mapHeight:
            return 'Out of Bounds'
        return tileMap[y][x]
    except IndexError:
        return 'Out of Bounds'

def populateMap():
    i = 0
    while i < totalBombs:
        x = random.randint(0,mapWidth-1)
        y = random.randint(0,mapHeight-1)
        if getTileonMap(x,y)[0] != 'b':
            setTileonMap(x,y,'bh')
            i += 1
            for neighborY in range(-1,2):
                for neighborX in range(-1,2):
                    neighborTile = getTileonMap(x+neighborX,y+neighborY)[0]
                    if neighborTile.isnumeric():
                        setTileonMap(x+neighborX,y+neighborY,str(int(neighborTile)+1)+'h')




def getInp(control_scheme):
    keys = pygame.key.get_pressed()
    for key in controls[control_scheme]:
        if keys[key]:
            return True
    return False

# Main game loop
while replay:
    resetVars()
    setSize(24+(16*mapWidth),67+(16*mapHeight))
    setScale(3)

    clearMap()
    populateMap()
    for row in tileMap:
        print(row)

    running = True
    closed = False
    while running and not closed:
        clock.tick(frameRate)

        # Get sprites
        sprites = []
        spriteGroup.empty()
        (startX,startY) = (12,55)
        y = 0
        for row in tileMap:
            x = 0
            for tile in row:
                sprite = pygame.sprite.Sprite()
                if len(tile) == 1:
                    sprite.image = pieces[tile[0]]
                else:
                    sprite.image = pieces[tile[1]]
                sprite.rect = sprite.image.get_rect()
                sprite.rect.topleft = (startX+16*x,startY+16*y)
                sprite.x = x
                sprite.y = y
                sprites.append(sprite)
                spriteGroup.add(sprite)
                x += 1
            y += 1

        # -- Events -- 
        for event in pygame.event.get():
            # Detect window closed
            if event.type == pygame.QUIT:
                closed = True
                replay = False
            # - Input -
            if event.type == pygame.KEYDOWN:
                if event.key in controls['quit']:
                    closed = True
                    replay = False
                if event.key in controls['mode']:
                    if mode == 'clear':
                        mode = 'flag'
                    else:
                        mode = 'clear'
            if event.type == pygame.MOUSEBUTTONUP:
                [mouseX,mouseY] = pygame.mouse.get_pos()
                mouseX = mouseX // (display.get_width() // screen.get_width())
                mouseY = mouseY // (display.get_width() // screen.get_width())
                for sprite in sprites:
                    if sprite.rect.collidepoint((mouseX,mouseY)):
                        tile = getTileonMap(sprite.x,sprite.y)
                        if mode == 'clear':
                            if len(tile) == 2:
                                if tile[1] == 'h':
                                    setTileonMap(sprite.x,sprite.y,tile[0])
                        else:
                            if len(tile) == 2:
                                if tile[1] == 'h':
                                    setTileonMap(sprite.x,sprite.y,tile[0]+'f')
                        break
            # - Input -
        # -- Events --

        # --- Rendering ---
        screen.fill((192,192,192))
        # -- Frames --
            # - Outer -
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, display_width, 3)) # top
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 3, display_height)) # left
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(0, display_height-1, 1, 1)) # bottom left intermediate
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(1, display_height-2, 1, 1)) # bottom left intermediate
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(2, display_height-3, 1, 1)) # bottom left intermediate
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(1, display_height-1, 1, 1)) # bottom left overlap
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(2, display_height-2, 1, 2)) # bottom left overlap
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(display_width-1, 0, 1, 1)) # top right intermediate
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(display_width-2, 1, 1, 1)) # top right intermediate
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(display_width-3, 2, 1, 1)) # top right intermediate
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(display_width-2, 2, 1, 1)) # top right overlap
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(display_width-1, 1, 1, 2)) # top right overlap
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(3, display_height-3, display_width-3, 3)) # bottom
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(display_width-3, 3, 3, display_height-3)) # right
            # - Outer -
            # - Top Gui -
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(9, 9, display_width-(9*2)-1, 2)) # top
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(9, 9, 2, 36)) # left
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(10, 44, display_width-(9*2)-1, 2)) # bottom
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(10, 44, 1, 1)) # bottom left intermediate
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(display_width-9-2, 10, 2, 36)) # right
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(display_width-9-2, 10, 1, 1)) # top right intermediate
                # - Left Numbers -
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(16, 15, 40, 1)) # top
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(16, 15, 1, 24)) # left
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(17, 39, 40, 1)) # bottom
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(56, 16, 1, 24)) # right
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(17, 16, 39, 23)) # inner
                # - Left Numbers -
                # - Right Numbers -
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(display_width-57, 15, 40, 1)) # top
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(display_width-57, 15, 1, 24)) # left
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(display_width-56, 39, 40, 1)) # bottom
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(display_width-17, 16, 1, 24)) # right
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(display_width-56, 16, 39, 23)) # inner
                # - Right Numbers -
            # - Top Gui -
            # - Field -
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(9, 52, 16*mapWidth+3+2, 3)) # top
        pygame.draw.rect(screen, (128,128,128), pygame.Rect(9, 52, 3, 16*mapHeight+3+2)) # left
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(11, display_height-12, 16*mapWidth+2+2, 3)) # bottom
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(11, display_height-12, 1, 1)) # bottom left intermediate
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(10, display_height-11, 1, 1)) # bottom left intermediate
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(10, display_height-10, 1, 1)) # bottom overlap
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(display_width-12, 54, 3, 16*mapHeight+2+2)) # right
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(display_width-11, 53, 1, 1)) # top right intermediate
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(display_width-12, 54, 1, 1)) # top right intermediate
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(display_width-10, 53, 1, 1)) # right overlap
            # - Field -
        # -- Frames --
        spriteGroup.draw(screen) # Tiles
        scaled = pygame.transform.scale(screen, display.get_size())
        display.blit(scaled, (0, 0))
        pygame.display.flip()
        # --- Rendering ---
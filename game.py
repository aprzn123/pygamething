"""
The main game.
"""
import pygame

# window dimensions
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 512

pygame.init()

# create window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# set title bar title
pygame.display.set_caption("game")

# player variables
x = 0
y = 0
w = 64
h = 64
x_v = 4
is_jumping = False
y_v = 0

def draw():
    # background black
    WINDOW.fill((0, 0, 0))
    # create rectangle
    pygame.draw.rect(WINDOW, (255, 127, 0), (x, y, w, h))

# game loop
run = True
while run:
    # 15 ms/tick
    pygame.time.delay(15)

    # detect events
    for event in pygame.event.get():
        
        # actions to quit
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
    
    keys = pygame.key.get_pressed()

    # player movement
    if keys[pygame.K_LEFT] and x > 0:
        x -= x_v
    if keys[pygame.K_RIGHT] and x + w < WINDOW_WIDTH:
        x += x_v
    if keys[pygame.K_UP] and y + h >= WINDOW_HEIGHT:
        is_jumping = True
    
    # gravity
    if y + h < WINDOW_HEIGHT:
        # above ground
        y_v -= 1
    else:
        # below ground
        y = WINDOW_HEIGHT - h
        y_v = 0

    # jumps
    if is_jumping:
        y_v = 20
        is_jumping = False
    
    # finalize y movement
    y -= y_v

    draw()

    # update the display
    pygame.display.update()

pygame.quit()

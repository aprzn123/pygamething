"""
The main game.
"""
import pygame
# window dimensions
WINDOW_WIDTH = 852
WINDOW_HEIGHT = 480

pygame.init()

# create window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# set title bar title
pygame.display.set_caption("game")

# import sprite images
walk_r = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walk_l = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')

# player variables
x = 256
y = 0
w = 64
h = 64
x_v_MAX = 5
x_v = 0
is_jumping = False
y_v_MAX = 20
y_v = 0
r = False
l = False
walk_count = 0

# Drawing all the things
def draw():
    global walk_count
    global y
    global h
    # background
    WINDOW.blit(bg, (0, 0))

    #blit with the (walk_count % 27)//3
    #draw character
    if l:
        WINDOW.blit(walk_l[(walk_count % 27)//3], (x, y))
    elif r:
        WINDOW.blit(walk_r[(walk_count % 27)//3], (x, y))
    else:
        WINDOW.blit(char, (x, y))
    if y + h == WINDOW_HEIGHT:
        walk_count += 1

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
    
    # compute gravity
    if y + h < WINDOW_HEIGHT: # above ground
        y_v -= 1
    else: 
        y = WINDOW_HEIGHT - h # below/on ground
        y_v = 0

    # compute x decel
    if x_v > 0:
        x_v -= 1
    elif x_v < 0:
        x_v += 1
    
    # compute player movement
    if keys[pygame.K_LEFT] and x > 0:
        if not keys[pygame.K_RIGHT]:
            if x_v > -1 * x_v_MAX:
                x_v -= 2
            else:
                x_v = -1 * x_v_MAX
            l, r = True, False
        else:
            l, r = False, False
    elif keys[pygame.K_RIGHT] and x + w < WINDOW_WIDTH:
        if x_v < x_v_MAX:
            x_v += 2
        else:
            x_v = x_v_MAX
        r, l = True, False
    else:
        l, r = False, False
        walk_count = 0
    if keys[pygame.K_UP] and y + h >= WINDOW_HEIGHT:
        is_jumping = True

    # compute jumps
    if is_jumping:
        y_v = y_v_MAX
        is_jumping = False

    # finalize movement
    y -= y_v
    x += x_v

    draw()

    # update the display
    pygame.display.update()

pygame.quit()

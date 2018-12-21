"""
The main game.
"""
import pygame

# window dimensions
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

pygame.init()

# create window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# set title bar title
pygame.display.set_caption("game")

# player variables
x = 50
y = 50
w = 40
h = 60
v = 5

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
    
    # player movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > v:
        x -= v
    if keys[pygame.K_RIGHT] and x + w < 500 - v:
        x += v
    if keys[pygame.K_UP] and y > v:
        y -= v
    if keys[pygame.K_DOWN] and y + h < 500 - v:
        y += v

    # background black
    WINDOW.fill((0, 0, 0))
    # create rectangle
    pygame.draw.rect(WINDOW, (255, 127, 0), (x, y, w, h))

    # update the display
    pygame.display.update()

pygame.quit()

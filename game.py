"""
The main game.
"""
import pygame


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

pygame.init()

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("game")

x = 50
y = 50
w = 40
h = 60
v = 5

run = True
while run:
    pygame.time.delay(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > v:
        x -= v
    if keys[pygame.K_RIGHT] and x + w < 500 - v:
        x += v
    if keys[pygame.K_UP] and y > v:
        y -= v
    if keys[pygame.K_DOWN] and y + h < 500 - v:
        y += v

    WINDOW.fill((0, 0, 0))
    pygame.draw.rect(WINDOW, (255, 127, 0), (x, y, w, h))

    pygame.display.update()

pygame.quit()

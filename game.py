"""
The main game.
"""
import pygame


pygame.init()

WINDOW = pygame.display.set_mode((500, 500))

pygame.display.set_caption("game")

x = 50
y = 50
w = 40
h = 60
v = 5

run = True
while run:
    pygame.time.delay(100)
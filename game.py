"""
The main game.
"""
# INITIALIZE ---------------------------------------------------------------------------

import pygame
# window dimensions
WINDOW_WIDTH = 852
WINDOW_HEIGHT = 480

pygame.init()

# create window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# set title bar title
pygame.display.set_caption("game")

# import the images
walk_r = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), \
pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), \
pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), \
pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), \
pygame.image.load('assets/R9.png')]
walk_l = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), \
pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), \
pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), \
pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), \
pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')

# END INITIALIZE -----------------------------------------------------------------------
# CREATE CLASSES -----------------------------------------------------------------------

# Create player class
class Player(object):
    def __init__(self, x, y, w, h, x_v_MAX, y_v_MAX):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_v_MAX = x_v_MAX
        self.y_v_MAX = y_v_MAX
        self.x_v = 0
        self.y_v = 0
        self.l = False
        self.r = True
        self.walk_count = 0
        self.is_jumping = False
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)
    
    # draw character
    def draw(self, win):
        if self.l:
            win.blit(walk_l[(self.walk_count % 27)//3], (self.x, self.y))
        elif self.r:
            win.blit(walk_r[(self.walk_count % 27)//3], (self.x, self.y))
        else:
            win.blit(char, (self.x, self.y))
        if self.y + self.h == WINDOW_HEIGHT:
            self.walk_count += 1

# Create projectile class
class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.x_v = 16 * facing
        self.y_v = 10

    # draw projectile
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Create Enemy class
class Enemy(object):
    walk_r = [pygame.image.load('assets/R1E.png'), pygame.image.load('assets/R2E.png'), \
    pygame.image.load('assets/R3E.png'), pygame.image.load('assets/R4E.png'), \
    pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'), \
    pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'), \
    pygame.image.load('assets/R9E.png'), pygame.image.load('assets/R10E.png'), \
    pygame.image.load('assets/R11E.png')]

    walk_l = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'), \
    pygame.image.load('assets/L3E.png'), pygame.image.load('assets/L4E.png'), \
    pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'), \
    pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'), \
    pygame.image.load('assets/L9E.png'), pygame.image.load('assets/L10E.png'), \
    pygame.image.load('assets/L11E.png')]

    def __init__(self, x, y, w, h, v, end):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.end = end
        self.walk_count = 0
        self.v = v
        self.path = [self.x, self.end]

    def draw(self, win):
        if self.v < 0:
            win.blit(self.walk_l[(self.walk_count  % 33) // 3], (self.x, self.y))
        else:
            win.blit(self.walk_r[(self.walk_count % 33) // 3], (self.x, self.y))
        self.walk_count += 1
        print(self.walk_count)
    
    def move(self):
        if self.v > 0:
            if self.x + self.w < self.path[1]:
                self.x += self.v
                #print("moved right")
            else:
                self.v = self.v * -1
                self.walk_count = 0
                #print("turned left")
        else:
            if self.x > self.path[0]:
                self.x += self.v
                #print("moved left")
            else:
                self.v = self.v * -1
                self.walk_count = 0
                #print("turned right")

# END CREATE CLASSES -------------------------------------------------------------------
# DEFINE VARIABLES AND FUNCTIONS -------------------------------------------------------

# clock
clock = pygame.time.Clock()

# entities
you = Player(256, 100, 64, 64, 5, 15)
bullets = []
enemy = Enemy(00, 416, 64, 64, 3, 800)

# shot timer
shot_timer = 0

# Drawing all the things
def redrawFrame():
    # background
    WINDOW.blit(bg, (0, 0))

    # player
    you.draw(WINDOW)

    # bullets
    for bullet in bullets:
        bullet.draw(WINDOW)

    # enemy
    enemy.draw(WINDOW)

    # NOTHING PAST HERE ===========
    pygame.display.update()
# debug
def debug():
    pass

# END DEFINE VARIABLES AND FUNCTIONS ---------------------------------------------------
# GAME LOOP ----------------------------------------------------------------------------

# game loop
run = True
while run:
    # 60 fps/tps
    clock.tick(60)

    # detect events
    for event in pygame.event.get():
        
        # actions to quit
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
    
    keys = pygame.key.get_pressed()
    
    # the bullets
    if keys[pygame.K_SPACE] and not(shot_timer): # shoot
        bullets.append(Projectile(you.x + round(you.w / 2), \
        you.y + round(you.h / 2), 4, (0, 0, 0), int((you.r - 0.5) * 2)))
        shot_timer = 10
    elif shot_timer:
        shot_timer -= 1
            
    for bullet in bullets: # x movement
        if bullet.x < WINDOW_WIDTH and bullet.x > 0 and bullet.y > 0 and bullet.y < WINDOW_HEIGHT:
            bullet.x += bullet.x_v
        else:
            bullets.pop(bullets.index(bullet))
    
    # compute gravity
    # player
    if you.y + you.h < WINDOW_HEIGHT: # above ground
        you.y_v -= 1
    else: 
        you.y = WINDOW_HEIGHT - you.h # below/on ground
        you.y_v = 0
    # projectile
    for bullet in bullets:
        bullet.y_v -= 1

    # compute x decel
    if you.x_v > 0:
        you.x_v -= 1
    elif you.x_v < 0:
        you.x_v += 1
    
    # compute player movement
    if keys[pygame.K_LEFT] and you.x > 0:
        if not keys[pygame.K_RIGHT]:
            if you.x_v > -1 * you.x_v_MAX:
                you.x_v -= 2
            else:
                you.x_v = -1 * you.x_v_MAX
        you.l, you.r = True, False
        you.standing = False
    elif keys[pygame.K_RIGHT] and you.x + you.w < WINDOW_WIDTH:
        if you.x_v < you.x_v_MAX:
            you.x_v += 2
        else:
            you.x_v = you.x_v_MAX
        you.r, you.l = True, False
        you.standing = False
    else:
        you.walk_count = 0
        you.standing = True
    if keys[pygame.K_UP] and you.y + you.h >= WINDOW_HEIGHT:
        you.is_jumping = True

    # compute jumps
    if you.is_jumping:
        you.y_v = you.y_v_MAX
        you.is_jumping = False

    # finalize movement
    you.y -= you.y_v
    you.x += you.x_v
    for bullet in bullets:
        bullet.y -= bullet.y_v
    enemy.move()

    redrawFrame()
    debug()

pygame.quit()
# END GAME LOOP ------------------------------------------------------------------------

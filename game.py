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

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.x_v = 8 * facing
        self.y_v = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
  
# clock
clock = pygame.time.Clock()

you = Player(256, 100, 64, 64, 5, 20)
bullets = []

# Drawing all the things
def draw():
    global walk_count
    global y
    global h
    # background
    WINDOW.blit(bg, (0, 0))

    # player
    you.draw(WINDOW)

    pygame.display.update()

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
    
    #the bullets
    if keys[pygame.K_SPACE]:
        if len(bullets) < 10:
            bullets.append(Projectile(you.x + round(you.w / 2), \
            you.y + round(you.h / 2), 6, (0, 0 , 0), (you.r - 0.5) * 2))
    for bullet in bullets:
        if bullet.x < WINDOW_WIDTH and bullet.x > 0:
            bullet.x += bullet.x_v
        else:
            bullets.pop(bullets.index(bullet))
    
    # compute gravity
    if you.y + you.h < WINDOW_HEIGHT: # above ground
        you.y_v -= 1
    else: 
        you.y = WINDOW_HEIGHT - you.h # below/on ground
        you.y_v = 0

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

    draw()

pygame.quit()

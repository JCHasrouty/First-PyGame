import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        # character placement on screen
        self.x = x
        self.y = y
        # character size
        self.width = width
        self.height = height
        # character speed
        self.vel = 5
        # movement variables
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
    def draw(self, win):
        # IF walkCount reaches higher than 27 we will have an indexing error
        # Each sprite display is limited to 3 frames because we have 9 sprites total  
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
                

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def redrawGameWindow():
    win.blit(bg, (0,0))
    BillyTheGoat.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

#main loop
BillyTheGoat = player(300, 410, 64, 64)
bullets = []
run = True
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            # find index of bullet in list and remove it
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if BillyTheGoat.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(BillyTheGoat.x + BillyTheGoat.width //2), round(BillyTheGoat.y + BillyTheGoat.height //2), 6, (0,0,0), facing))
            
    if keys[pygame.K_LEFT] and BillyTheGoat.x > 0:
        BillyTheGoat.x -= BillyTheGoat.vel
        BillyTheGoat.left = True
        BillyTheGoat.right = False
        BillyTheGoat.standing = False
    elif keys[pygame.K_RIGHT] and BillyTheGoat.x < 500 - BillyTheGoat.width:
        BillyTheGoat.x += BillyTheGoat.vel
        BillyTheGoat.right = True
        BillyTheGoat.left = False
        BillyTheGoat.standing = False
    else:
        BillyTheGoat.standing = True
        BillyTheGoat.walkCount = 0
        
    if not(BillyTheGoat.isJump):
        if keys[pygame.K_UP]:
            BillyTheGoat.isJump = True
            BillyTheGoat.right = False
            BillyTheGoat.left = False
            BillyTheGoat.walkCount = 0
    else:
        if BillyTheGoat.jumpCount >= -10:
            BillyTheGoat.y -= (BillyTheGoat.jumpCount * abs(BillyTheGoat.jumpCount)) * 0.5
            BillyTheGoat.jumpCount -= 1
        else:
            BillyTheGoat.isJump = False
            BillyTheGoat.jumpCount = 10

    redrawGameWindow()

pygame.quit()
        

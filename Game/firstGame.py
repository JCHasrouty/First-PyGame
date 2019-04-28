import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
# importing music/sound effects
#bulletSound = pygame.mixer.Sound('bullet.wav')
#hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0

#Player class
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
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        # hit box dimensions
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        
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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
        
#Projectile class
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


#Enemy class
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            # Enemy health bar
            # red background
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # green health bar
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
    
    def move(self):
        if self.vel > 0:
            # if character hasn't passed the end of path allow him to move
            if self.x  + self.vel < self.path[1]:
                self.x += self.vel
            # else if he has change directions
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        # if velocity is negative then check if x - vel is > path 1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

#Draw game window function        
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (350, 10))
    BillyTheGoat.draw(win)
    Cody.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

#main loop
font = pygame.font.SysFont('comicsans', 30, True)
BillyTheGoat = player(300, 410, 64, 64)
Cody = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)
    if Cody.visible == True:
        # check if player and character collided then reduce player health 
        if BillyTheGoat.hitbox[1] < Cody.hitbox[1] + Cody.hitbox[3] and BillyTheGoat.hitbox[1] + BillyTheGoat.hitbox[3] > Cody.hitbox[1]:
            if BillyTheGoat.hitbox[0] + BillyTheGoat.hitbox[2] > Cody.hitbox[0] and BillyTheGoat.hitbox[0] < Cody.hitbox[0] + Cody.hitbox[2]:
                BillyTheGoat.hit()
                score -= 5

    # bullet shooting cooldown
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    for bullet in bullets:
        # check if bullet is above the bottom and below the top of the rectangle (within hitbox dimensions)
        if bullet.y - bullet.radius < Cody.hitbox[1] + Cody.hitbox[3] and bullet.y + bullet.radius > Cody.hitbox[1]:
            # check if bullet is between left and right sides of the hitbox
            if bullet.x + bullet.radius > Cody.hitbox[0] and bullet.x - bullet.radius < Cody.hitbox[0] + Cody.hitbox[2]:
                #hitSound.play()
                Cody.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            # find index of bullet in list and remove it
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        #bulletSound.play()
        if BillyTheGoat.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(BillyTheGoat.x + BillyTheGoat.width //2), round(BillyTheGoat.y + BillyTheGoat.height //2), 6, (0,0,0), facing))

        shootLoop = 1
        
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
        

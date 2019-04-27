import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First Game")

isJump = False
jumpCount = 10

x = 50
y = 50
width = 40
height = 60
vel = 10

run = True
while run:
    pygame.time.delay(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
    if keys[pygame.K_RIGHT] and x < 500 - width:
        x += vel
    if not(isJump):
        if keys[pygame.K_UP] and y > 0:
            y -= vel
        if keys[pygame.K_DOWN] and y < 500 - height:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()
        

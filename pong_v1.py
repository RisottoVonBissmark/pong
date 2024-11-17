#imports
import pygame, sys, time
from pygame.locals import *


pygame.init()

width=850
height=550

fps=60
FPS=pygame.time.Clock()

font=pygame.font.SysFont("Verdana", 20)

displaySurf=pygame.display.set_mode((width, height))

class pad(pygame.sprite.Sprite):
    def __init__(self, up, down, pos):
        super().__init__()
        self.surf=pygame.Surface((10, 100))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.rect.center=(pos, int(height/2))
    
        self.up=up
        self.down=down
        
        self.score=0
    
    def move(self):  
        pressed_key=pygame.key.get_pressed()
        
        if self.rect.top>0:
            if pressed_key[self.up]:
                self.rect.move_ip(0,-5)
        if self.rect.bottom<height:
            if pressed_key[self.down]:
                self.rect.move_ip(0,5)
            
class ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.rect.center=(width/2, height/2)
        
        self.speed=3
        
        self.x=self.speed
        self.y=0
        
    def move(self):
        
        hits=pygame.sprite.spritecollideany(b1, pads, False)
        if hits:
            
            self.x=-self.x
            if self.x>0:
                self.x=self.speed
            if self.x<0:
                self.x=-self.speed
            h=hits.surf.get_height()
            
            if self.rect.top>=hits.rect.top and self.rect.top<hits.rect.top+int(h/3):
                self.y=-(self.speed/3)
            elif self.rect.top>=hits.rect.top+int(h/3) and self.rect.top<hits.rect.top+(2*int(h/3)):
                self.y=0
            elif self.rect.top>=hits.rect.top+(2*int(h/3)) and self.rect.top<hits.rect.top+(3*int(h/3)):
                self.y=self.speed/3
        
        if self.rect.top<=0:
            self.y=-self.y
        if self.rect.bottom>=height:
            self.y=-self.y

        self.rect.move_ip(self.x,self.y)




p1=pad(K_w, K_s, 30)
p2=pad(K_UP, K_DOWN, width-30)

b1=ball()

allSprites=pygame.sprite.Group()
allSprites.add(p1)
allSprites.add(p2)
allSprites.add(b1)

pads=pygame.sprite.Group()
pads.add(p1)
pads.add(p2)

incSpeed=pygame.USEREVENT+1
pygame.time.set_timer(incSpeed, 9999) 

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==incSpeed:
            b1.speed+=1
            
    if b1.rect.right<0:
        p2.score+=1
        time.sleep(1)
        b1.speed=3
        b1.rect.center=(width/2, height/2)
        b1.x=-b1.speed
        b1.y=0
    if b1.rect.left>width:
        p1.score+=1
        time.sleep(1)
        b1.speed=3
        b1.rect.center=(width/2, height/2)
        b1.x=b1.speed
        b1.y=0
    
    if p1.score>10 or p2.score>10:
        displaySurf.fill((0,0,0))
        if p1.score>10:
            gameOver=font.render("player 1 win", True, (255,255,255))
        if p2.score>10:
            gameOver=font.render("player 2 win", True, (255,255,255))
        displaySurf.blit(gameOver, height/2, 100)
        pygame.display.update()
        time.sleep(2)
        for entity in allSprites:
            entity.kill()
        pygame.quit()
        sys.exit

    displaySurf.fill((0,0,0))
    
    for entity in allSprites:
        displaySurf.blit(entity.surf, entity.rect)
        entity.move()
    
    
    sco1=font.render(str(p1.score), True, (255,255,255))
    displaySurf.blit(sco1, ((width/2)-(width/4), 10))
    
    sco2=font.render(str(p2.score), True, (255,255,255))
    displaySurf.blit(sco2, ((width/2)+(width/4), 10))
    
    
   
    
    pygame.display.update()
    FPS.tick(fps)

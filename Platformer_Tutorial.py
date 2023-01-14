import pygame
from pygame.locals import *
import sys
import random
import time
import os

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
        def __init__(self):
                super().__init__()
                self.surf = pygame.Surface((30, 30))
                self.surf.fill((128, 255, 40))
                self.rect = self.surf.get_rect()

                self.pos = vec((30, 385))
                self.vel = vec(0,0)
                self.acc = vec(0,0)
                self.jumping = False
                self.score = 0 


        def move(self):
            self.acc = vec(0,0.5) #Apply Gravity

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
            if pressed_keys[K_RIGHT]:
                self.acc.x = ACC

            #Apply Friction
            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            #Screen wrap
            if self.pos.x > WIDTH:
                self.pos.x = 0
            if self.pos.x < 0:
                    self.pos.x = WIDTH
            #Actually update position
            self.rect.midbottom = self.pos

        def update(self):
            hits = pygame.sprite.spritecollide(Player_One, platforms, False)
            if Player_One.vel.y > 0:
                if hits:
                    if self.pos.y < hits[0].rect.bottom:
                        if hits[0].point == True:
                            hits[0].point = False
                            self.score += 1
                        self.pos.y = hits[0].rect.top + 1
                        self.vel.y = 0
                        self.jumping = False

        def jump(self):
            hits = pygame.sprite.spritecollide(self,platforms, False)
            if hits:   
                self.jumping = True
                self.vel.y = -15

        def cancel_jump(self):
            if self.jumping:
                if self.vel.y < -3:
                    self.vel.y = -3

def proximity_check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom < 50) and (abs(platform.rect.bottom - entity.rect.top) < 50)):
                return True
        C = False

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0,0,244))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30)))
        self.moving = True
        self.speed = random.randint(-1, 1)
        self.point = True
    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.right > WIDTH:
                self.rect.right = 0
            if self.speed < 0  and self.rect.right < 0:
                self.rect.left = WIDTH


def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = platform()
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 1000))
            C = proximity_check(p, platforms)
        platforms.add(p)
        all_sprites.add(p) 
 
PT1 = platform()
Player_One = Player()

PT1.moving = False
PT1.point = False
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
                
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(Player_One)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)




while True:
    #Event catching
    for event in pygame.event.get():
        if event.type == QUIT:
            with open("scores.txt", "a") as f:
                f.write(f"{Player_One.score}\n")
                f.close()
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player_One.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                Player_One.cancel_jump()
                

        #Endstatem, player goes off screen.
        if Player_One.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                pygame.display.update()
                time.sleep(1)
                with open("scores.txt", "a") as f:
                    f.write(f"{Player_One.score}\n")
                    f.close()
            
                pygame.quit()
                sys.exit()


    #Infinite scroll
    if Player_One.rect.top <= HEIGHT / 3:
        Player_One.pos.y += abs(Player_One.vel.y)
        for plat in platforms:
            plat.rect.y += abs(Player_One.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    #Screen wipe and platform creation            
    displaysurface.fill((0,0,0))
    Player_One.update()
    plat_gen()

    #Display the score  
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(Player_One.score), True, (123,255,0))
    displaysurface.blit(g, (WIDTH/2, 10))


    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
    pygame.display.update()
    FramePerSec.tick(FPS)

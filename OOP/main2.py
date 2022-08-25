import pygame
import os

from pygame.transform import rotate
pygame.font.init()  # Initerar pygame font library
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500  # Display parameterar
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Den gör displayen för spelet
pygame.display.set_caption("Space Fighters")

FFS = 60

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 45)


YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png',))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), (90))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png',))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), (270))
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    
    def draw(self):    
        WIN.blit(RED_SPACESHIP, (self.x, self.y))
    
    def move(self):
        pass
           
class Projectile(object):
    pass

def draw_win(WIN,SPACE):
     WIN.blit(SPACE, (0, 0))




def main2():
    
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FFS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                          
        
    main2()
    
if __name__ == "__main2__":
    main2()
            
             
        

    
    
    

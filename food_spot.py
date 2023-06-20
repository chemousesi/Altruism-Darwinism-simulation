import numpy
import pygame
from pig_tv import GREEN

pygame.init()
screen = pygame.display.set_mode((600, 480))

class Food:
    width = 20
    height =20

    def __init__(self,x,y) -> None:
        self.x = x                              # coordinate of the food spot
        self.y = y
        self.ressource = 50                         # quantity of available food
        self.state = True                           # State of the food spot, False if it is exhausted
        self.table = [(i,j) for i in range(x,x+self.width) for j in range(y,y+self.height)]
        self.regenerate = 0

        self.rect = pygame.Rect(x,y,self.width,self.height)
        
        
    

    def getting_eaten(self):
        self.ressource -= 1
        if (self.ressource == 0):
            self.state = False

    
    def get_ressource(self):
        return self.ressource
    
    def get_table(self):
        return self.table
    
    def update(self):
        return 0

    
    def draw(self):
        if (self.state == True):
            pygame.draw.rect(screen,GREEN, self.rect)
    
    def update(self):
        if (self.state == False):
            self.regenerate += 1
            if (self.regenerate == 100):
                self.regenerate = 0
                self.ressource = 50
                self.state = True
                self.draw()

        

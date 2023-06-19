import numpy
import pygame
pygame.init()
screen = pygame.display.set_mode((600, 480))

class food:
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

    
    def draw(self):
        pygame.draw.rect(screen,GREEN, self.rect)

        

a = food(3,4)
a.getting_eaten()
print("eee")
b = a.get_ressource()
print(b)
L = a.get_table()
#print(L)

while (True):
    a.draw()
    pygame.display.update()
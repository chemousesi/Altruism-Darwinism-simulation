from pig_tv_csts import *
from utils import *

from entity import Entity, CircleEntity



class Food(Entity):

    width = json_data["food_width"]
    height = json_data["food_height"]

    def __init__(self, pos, screen) -> None:

        Entity.__init__(self, screen, pos)

        x, y = self.pos

        self.ressource = 50

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

        if (self.state == True):
            pygame.draw.rect(self.screen,GREEN, self.rect)

        else:
            pygame.draw.rect(self.screen,BLACK, self.rect)
    

    def update(self, draw=False):

        if (self.state == False):
            self.regenerate += 1
            if (self.regenerate == 100):
                self.regenerate = 0
                self.ressource = 50
                self.state = True

        if draw:

            Food.draw(self)

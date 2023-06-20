from pig_tv_csts import *
from utils import *

from entity import Entity, CircleEntity



class Food(Entity):

    width = json_data["food_width"]
    height = json_data["food_height"]

    def __init__(self, pos, screen) -> None:

        Entity.__init__(self, screen, pos)

        x, y = self.pos

        self.food_value = json_data["food_value"]

        self.ressource = json_data["food_number_in_storage"]*self.food_value

        self.available_food = True                           # State of the food spot, False if it is exhausted

        self.table = [(i,j) for i in range(x,x+self.width) for j in range(y,y+self.height)]

        self.regenerate = 0  # when exhausted, ticks until limit then refills

        self.rect = pygame.Rect(x,y,self.width,self.height)

    def getting_eaten(self):

        self.ressource -= self.food_value

        if (self.ressource == 0):
            self.available_food = False

        return self.ressource

    def get_ressource(self):
        return self.ressource

    def get_table(self):
        return self.table

    def draw(self):

        if (self.available_food == True):
            pygame.draw.rect(self.screen,GREEN, self.rect)

        else:
            pygame.draw.rect(self.screen,BLACK, self.rect)
    

    def update(self, draw=False):

        if (self.available_food == False):

            self.regenerate += 1
            if (self.regenerate == 100):
                self.regenerate = 0
                self.ressource = json_data["food_storage"]
                self.available_food = True

        if draw:

            Food.draw(self)

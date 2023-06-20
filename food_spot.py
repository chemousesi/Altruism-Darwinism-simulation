from pig_tv_csts import *
from utils import *



class Food:

    width = json_data["food_width"]
    height =json_data["food_height"]

    def __init__(self,x,y,screen) -> None:
        self.x = x                              # coordinate of the food spot
        self.y = y
        self.ressource = json_data["initial_energy"]
        self.screen = screen                         # quantity of available food
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
    

    def update(self):
        if (self.state == False):
            self.regenerate += 1
            if (self.regenerate == json_data["food_regeneration_time"]):
                self.regenerate = 0
                self.ressource = json_data["initial_energy"]
                self.state = True
                self.draw()

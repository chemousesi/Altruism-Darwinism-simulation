from pig_tv_csts import *
from utils import *
import json_loader as json_loader

class Square:

    def __init__(self, i, j, screen):

        self.i = i

        self.j = j

        self.size = json_loader.json_data["grid_square_size"]

        self.x = j*self.size#(j+0.5)*self.size

        self.y = i*self.size#(i+0.5)*self.size

        self.entities = []

        self.pheromones = []

        self.foods = []

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.screen = screen

    def __repr__(self):

        return "".join([str(ph.type_pheromone) for ph in self.pheromones])

    def draw(self):

        #pygame.draw.rect(self.screen, BLUE, self.rect, 3)

        if len(self.pheromones) >= 1 and self.pheromones[-1].type_pheromone == 1:

            pygame.draw.rect(self.screen, YELLOW, self.rect)

        elif len(self.pheromones) > 1:

            pygame.draw.rect(self.screen, PURPLE, self.rect)

        #if self.entities != []:

            #pygame.draw.rect(self.screen, PURPLE, self.rect)

    def add_entity(self, entity):

        self.entities.append(entity)

    def add_pheromone(self, pheromone):

        self.pheromones.append(pheromone)

    def add_food(self, food):

        self.foods.append(food)

    def del_entity(self, entity):

        if entity:

            self.entities.remove(entity)

    def del_pheromone(self, pheromone):

        if pheromone:

            self.pheromones.remove(pheromone)

    def del_food(self, food):

        if food:

            self.foods.remove(food)        

    def empty_pheromones(self):

        self.pheromones = []

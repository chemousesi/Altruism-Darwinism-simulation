from pig_tv_csts import *
from utils import *

from entity import Entity, CircleEntity


class Pheromone(CircleEntity):

    def __init__(self, pos, screen, type_pheromone, life_span, producer_ID):

        self.type_pheromone = type_pheromone

        if self.type_pheromone == 1:

            radius = json_data["type1_pheromone_radius"]

            color = YELLOW

        elif self.type_pheromone == 2:

            radius = json_data["type2_pheromone_radius"]

            color = PURPLE
        
        elif self.type_pheromone == 3:

            radius = json_data["type3_pheromone_radius"]

            color = BLUE

        self.life_span = life_span

        self.producer_ID = producer_ID

        CircleEntity.__init__(self, screen, pos, color, radius)

    def update(self, draw):


        if self.life_span == 0:

            return -1

        self.life_span -= 1

        if draw:

            Pheromone.draw(self)

    def get_producer_ID(self):
        return self.producer_ID


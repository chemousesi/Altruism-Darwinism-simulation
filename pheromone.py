from pig_tv_csts import *
from utils import *

from entity import Entity, CircleEntity


class Pheromone(CircleEntity):

    def __init__(self, pos, screen, type_pheromone, life_span):

        self.type_pheromone = type_pheromone

        if self.type_pheromone == 1:

            radius = json_data["type1_pheromone_radius"]

            color = YELLOW

        elif self.type_pheromone == 2:

            radius = json_data["type2_pheromone_radius"]

            color = PURPLE

        self.life_span = life_span

        CircleEntity.__init__(self, screen, pos, color, radius)

    def update(self, draw):


        if self.life_span == 0:

            return -1

        self.life_span -= 1

        if draw:

            Pheromone.draw(self)


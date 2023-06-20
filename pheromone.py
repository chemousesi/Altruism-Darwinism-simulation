from pig_tv_csts import *
from utils import *

from entity import Entity, CircleEntity


class Pheromone(Entity):

    def __init__(self, pos, color, radius, screen):

        Entity.__init__(self, pos, color, radius, screen)

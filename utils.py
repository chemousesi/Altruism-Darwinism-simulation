from enum import Enum
from math import *


def distance(object_a , object_b):
    return sqrt( (object_a.x - object_b.x)**2 + (object_a.y - object_b.y)**2   )


class TypeAgent(Enum):

    BASIC = 0
    ALTRUIST = 1
    PROFITEER = 2

    def get_color(self):
        
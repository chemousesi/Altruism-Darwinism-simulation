from pig_tv_csts import *
from utils import *

from pheromone_smeller_agent import PheromoneSmellerAgent
from pheromone_producer_agent import PheromoneProducerAgent


class Profiteer(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.PROFITEER, color=RED)

    def get_color():
        return RED

class Basic(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1], type_agent=TypeAgent.BASIC, color=BLUE)

    def get_color():
        return BLUE

class Altruist(PheromoneProducerAgent):

    def __init__(self, screen, pos=None):

        PheromoneProducerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.ALTRUIST, produced_pheromones=2, color=GREEN)  # 
    
    def get_color():
        return GREEN



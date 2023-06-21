from pig_tv_csts import *
from utils import *

from pheromone_smeller_agent import PheromoneSmellerAgent
from pheromone_producer_agent import PheromoneProducerAgent


class Profiteer(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.PROFITEER)
    def update_number(self,number_list):
        number_list[2] = number_list[2]+1
        
        


class Basic(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1], type_agent=TypeAgent.BASIC)
    def update_number(self,number_list):
        number_list[0] = number_list[0]+1


class Altruist(PheromoneProducerAgent):

    def __init__(self, screen, pos=None):
        PheromoneProducerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.ALTRUIST, produced_pheromones=2)  # 
    def update_number(self,number_list):
        number_list[1] = number_list[1]+1


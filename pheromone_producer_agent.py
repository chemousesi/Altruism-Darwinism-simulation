from pig_tv_csts import *
from pheromone_smeller_agent import PheromoneSmellerAgent
from utils import *


class PheromoneProducerAgent(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, recognised_pheromones=[1, 2], type_agent=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones, type_agent)

        self.produced_pheromones = produced_pheromones

        self.pheromone_energy_cost = json_data["pheromone_energy_cost"]

        self.pheromone_life_span = json_data["pheromone_life_span"]

    def eat(self, list_of_foods, list_of_pheromones):

        Agent.eat(self, list_of_foods, list_of_pheromones)

        return Agent.produce_pheromones(self)

    def produce_pheromones(self):

        self.energy -= self.pheromone_energy_cost

        return ("pheromone", self.produced_pheromones, self.pheromone_life_span)  # universe will create the pheromone
    

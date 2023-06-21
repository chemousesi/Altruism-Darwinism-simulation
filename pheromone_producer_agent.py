from pig_tv_csts import *
from pheromone_smeller_agent import PheromoneSmellerAgent
from utils import *


class PheromoneProducerAgent(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, recognised_pheromones=[1, 2], produced_pheromones=[2],type_agent=None, color=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones, type_agent, color)

        self.produced_pheromones = produced_pheromones

        self.pheromone_energy_cost_ratio = json_data["cost_of_pheromone_ratio"]

        self.pheromone_life_span = json_data["pheromone_life_span"]

    def update(self, list_of_foods, list_of_pheromones, draw=True):

        agent_state = super().update_energy(draw)
        #bebe = self.update_energy(draw)
        # updates vector then moves
        PheromoneSmellerAgent.update_vect(self, list_of_pheromones=list_of_pheromones)
        super().move()
        #self.move()

        # eats
        return [PheromoneProducerAgent.eat(self, list_of_foods), agent_state]  # returns in case a pheromone has been created

    def eat(self, list_of_foods):

        super().eat(list_of_foods)

        if self.is_eating:
            return self.produce_pheromones()
    
    def produce_pheromones(self):

        self.energy -= self.pheromone_energy_cost_ratio*json_data["food_value"]

        self.can_make_pheromone = False

        return ("pheromone", self.produced_pheromones, self.pheromone_life_span)  # universe will create the pheromone


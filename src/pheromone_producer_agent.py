from pig_tv_csts import *
from pheromone_smeller_agent import PheromoneSmellerAgent
from utils import *


class PheromoneProducerAgent(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, recognised_pheromones=[1, 2, 3], produced_pheromones=[2,3],type_agent=None, color=None, draw_energy=True):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones, type_agent, color, draw_energy=draw_energy)

        self.produced_pheromones = produced_pheromones

        self.pheromone_energy_cost_ratio = json_data["cost_of_pheromone_ratio"]

        self.pheromone_energy_cost_ratio_2 = json_data["cost_of_pheromone_ratio_2"]

        self.pheromone_life_span = json_data["pheromone_life_span"]

        self.pheromone_life_span_2 = json_data["pheromone_life_span_2"]

        self.ID = None

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
        
        else:
            return self.produce_pheromones_2()

    def produce_pheromones(self):

        self.energy -= self.pheromone_energy_cost_ratio*json_data["food_value"]

        self.can_make_pheromone = False

        return ("pheromone", self.produced_pheromones[0], self.pheromone_life_span,self.pos, None)  # universe will create the pheromone
    
    def produce_pheromones_2(self):

        if (self.ID == None):
            self.ID = random.randrange(100)

        else:
            self.energy -= self.pheromone_energy_cost_ratio_2*json_data["food_value"]

            #self.can_make_pheromone = False

            return ("pheromone", self.produced_pheromones[1], self.pheromone_life_span,self.pos, self.ID)  # universe will create the pheromone



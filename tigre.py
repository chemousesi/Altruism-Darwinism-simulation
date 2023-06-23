from pig_tv_csts import *
from utils import *

from pheromone_smeller_agent import PheromoneSmellerAgent

class Tigre(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None):

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.TIGRE, color=ORANGE)

        self.target_agent = None

        self.max_distance = 60

        self.target_distance = self.max_distance

        self.speed_norm *= 1.2

    def eat(self):

        self.add_to_energy(self.target_agent.energy)

        dead_agent = self.target_agent

        self.re_init_target()

        return dead_agent

    def re_init_target(self):

        self.target_agent = None

        self.target_distance = self.max_distance

    def change_target_agent(self, agent):

        dist = distance(self, agent)

        if dist < self.target_distance:

            self.target_distance = dist

            self.target_agent = agent

    def update_vect(self, list_of_pheromones):

        pheromone = self.find_closest_pheromone(list_of_pheromones)

        if pheromone != None:

            self.vector = -1* (pheromone.pos - self.pos)

            super().normalize_vect()

        elif self.target_agent != None:

            self.vector = self.target_agent.pos - self.pos

            super().normalize_vect()

        else:

            super().random_walk()

    def update(self, list_of_pheromones, agents, draw=True):

        if self.target_agent != None:

            self.target_distance = distance(self, self.target_agent)

        agent_state = agent_state = super().update_energy(draw)  # super().update(list_of_foods, list_of_pheromones, draw=True )

        if agent_state == "dead":

            return [None, agent_state]

        #
        for agent in agents:

            self.change_target_agent(agent)

        self.update_vect(list_of_pheromones)

        super().move()

        dead_agent = None

        if self.target_distance < 5:

            dead_agent = self.eat()

        return [dead_agent, None]




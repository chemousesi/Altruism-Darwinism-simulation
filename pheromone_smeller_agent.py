from pig_tv_csts import *
from agent import Agent
from utils import *


class PheromoneSmellerAgent(Agent):

    def __init__(self, screen, pos=None, recognised_pheromones=[1], type_agent=None):

        Agent.__init__(self, screen, pos, type_agent)

        self.recognised_pheromones = recognised_pheromones

    def find_closest_pheromone(self, list_of_pheromones):

        if len(list_of_pheromones) > 0:
            # chercher le phéromone le plus proche
            min_ph = list_of_pheromones[0]
            min_dist = distance(min_ph, self)

            for ph in list_of_pheromones:
                dist = distance(ph,self)
                if dist <= ph.radius and dist <= min_dist:
                    min_dist = dist
                    min_ph = ph

            return ph

    def move(self):
        if not self.is_eating :
            #smelling pheromones 
            pheromone = self.find_closest_pheromone()
            if pheromone != None:
                self.vect = pheromone.pos - self.pos
            else :
                super.move()
        

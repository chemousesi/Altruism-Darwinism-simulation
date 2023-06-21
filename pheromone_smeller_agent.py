from pig_tv_csts import *
from agent import Agent
from utils import *


class PheromoneSmellerAgent(Agent):

    def __init__(self, screen, pos=None, recognised_pheromones=[1], type_agent=None, color=None):

        Agent.__init__(self, screen, pos, type_agent, color=color)

        self.recognised_pheromones = recognised_pheromones

    def find_closest_pheromone(self, list_of_pheromones):
        """ returns the closest pheromone that is close enough to the agent so that he can smell it """

        if len(list_of_pheromones) > 0:
            # chercher le phéromone le plus proche
            min_ph = None
            min_dist = screen_width+screen_height

            for ph in list_of_pheromones:

                if ph.type_pheromone in self.recognised_pheromones:  # PheromoneSmellerAgent only sensible to some pheromones

                    dist = distance(ph,self)
                    if dist <= ph.radius and dist <= min_dist:
                        min_dist = dist
                        min_ph = ph

            if min_ph != None and min_ph.radius > min_dist:

                return min_ph

    def update(self, list_of_foods, list_of_pheromones, draw=True):

        bebe = Agent.update_energy(self, draw)

        # updates vector then moves
        PheromoneSmellerAgent.update_vect(self, list_of_pheromones)
        Agent.move(self)

        # eats
        Agent.eat(self, list_of_foods)

        return [None, bebe]


    def update_vect(self, list_of_pheromones):

        if self.is_eating :

            self.vector = Arr.get_nul([2])

        else:

            #smelling pheromones 

            pheromone = self.find_closest_pheromone(list_of_pheromones)

            if pheromone != None:

                self.vector = pheromone.pos - self.pos

                Agent.normalize_vect(self)

                #print(self.vector , pheromone.pos , self.pos)

            else :
                Agent.random_walk(self)
        

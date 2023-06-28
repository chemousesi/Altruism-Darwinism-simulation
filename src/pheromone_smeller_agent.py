from pig_tv_csts import *
from agent import Agent
from json_loader import *
from utils import *


class PheromoneSmellerAgent(Agent):

    def __init__(self, screen, pos=None, recognised_pheromones=[1], type_agent=None, color=None, draw_energy=True):

        Agent.__init__(self, screen, pos, type_agent, color=color, draw_energy=draw_energy)

        self.recognised_pheromones = recognised_pheromones

    def find_closest_pheromone(self):  # , list_of_pheromones):
        """ returns the closest pheromone that is close enough to the agent so that he can smell it """

        list_of_pheromones = self.square.pheromones

        if len(list_of_pheromones) > 0:
            # chercher le phéromone le plus proche
            min_ph = None
            min_dist = screen_width+screen_height

            for ph in list_of_pheromones:

                if ph.type_pheromone in self.recognised_pheromones:  # PheromoneSmellerAgent only sensible to some pheromones

                    dist = distance(ph,self)
                    if dist <= min_dist:  # dist <= ph.radius and 
                        min_dist = dist
                        min_ph = ph

            if min_ph != None:# and min_ph.radius > min_dist:

                return min_ph

    def update(self, draw=True):  # list_of_foods, list_of_pheromones, 

        agent_state = super().update_energy(draw)

        # updates vector then moves
        PheromoneSmellerAgent.update_vect(self)  # , list_of_pheromones)
        Agent.move(self)

        # eats
        Agent.eat(self)  # , list_of_foods)

        return agent_state


    def update_vect(self):  # , list_of_pheromones):

        if self.is_eating :

            self.vector = Arr.get_nul([2])

        else:

            #smelling pheromones

            pheromone = self.find_closest_pheromone()  # list_of_pheromones)

            if pheromone != None:

                self.vector = pheromone.pos - self.pos

                Agent.normalize_vect(self)

            else :
                Agent.random_walk(self)


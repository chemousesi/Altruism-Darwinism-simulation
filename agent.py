from pig_tv_csts import *
from utils import *

import universe
import button
from entity import Entity, CircleEntity


class Agent(CircleEntity):

    dico_color = {TypeAgent.ALTRUIST:GREEN, TypeAgent.PROFITEER:RED, TypeAgent.BASIC:BLUE}

    cost_of_reproduction = json_data["cost_of_reproduction"]

    required_energy_to_reproduce = json_data["required_energy_to_reproduce"]

    cost_of_pheromone = json_data["cost_of_pheromone"]

    prob_of_mutation = json_data["prob_of_mutation"]

    def __init__(self, screen, pos=None, type_agent : TypeAgent =None, radius=None, energy=None):

        # type_agent
        if type_agent != None:

            self.type_agent = type_agent

        else:

            self.type_agent = TypeAgent.BASIC

        if self.type_agent == TypeAgent.BASIC:
            self.type_agent_int =0
        elif self.type_agent == TypeAgent.ALTRUIST:
            self.type_agent_int =1
        elif self.type_agent == TypeAgent.PROFITEER:
            self.type_agent_int =2

        #
        CircleEntity.__init__(self, screen, pos, Agent.dico_color[self.type_agent], radius)

        #energy
        if energy != None:
            self.energy = energy
        else:
            self.energy = json_data["agent_initial_energy"]
        ##

        self.vector = Arr([10, 0])  # Arr.get_nul([2])

        self.speed_norm = json_data["agent_speed_norm"]

        self.delta_t = random.random()

        self.mode_transitoire = 0

        self.age = 0

        self.is_eating = False

        self.on_food = False

        self.can_make_pheromone = True

        self.has_reproduced_this_cycle = False

        self.new_born = True

    def get_color():
        return self.color

    def get_energy(self):

        return self.energy

    def get_vector(self):

        return self.vector

    def get_y(self):

        return self.y

    def get_x(self):

        return self.x

    def add_to_energy(self,loss):
        self.energy += loss

    def aging(self): #changes the value of the agent based on its age
        age = self.age

        def loss_function(x):

            return log(x+1)  # so it's never negative

        Agent.add_to_energy(self, -loss_function(age))

    def reproduce_alone(self): #returns the list of the agents after the reproduction cycle
         #checks if the agent is able to reproduce
        mutation = random.random()
        child = Agent(self.screen)
        if mutation < Agent.prob_of_mutation: #checks weither the child will be the type of its parent or not
            if self.type_agent_int == 1:
                child.type_agent_int = 2
            elif self.type_agent_int == 2:
                child.type_agent_int = 1
            else :
                child.type_agent_int = 0
        else:
            child.type_agent_int = self.type_agent_int
        child.x = self.x
        child.y = self.y
        Agent.add_to_energy(self, -Agent.cost_of_reproduction)
        return child


    def eat(self, list_of_foods):
        agent_has_eaten = False

        for food in list_of_foods: #checks if the agent is on a food spot

            if food.ressource > 0:

                if (self.pos-food.pos).norme_eucli() < 5:  # close enough

                    self.on_food = True #the agent is on a food
                    self.is_eating = True #the agent is no longer moving

                    energy = food.getting_eaten() #updates the amount of food remaining in the box
                    Agent.add_to_energy(self, energy) #updates the energy of the agent
                    agent_has_eaten =True

        if (agent_has_eaten == False) and (self.on_food == True): #if another agent has eaten the last bit of food of the food before this agent, it still needs to be able to move again or it will be stuck on the food
            self.is_eating = False
            self.can_make_pheromone = True

    def update(self, list_of_foods, list_of_pheromones, draw=True ):

        bebe = Agent.update_energy(self, draw)

        # updates vector then moves
        Agent.random_walk(self)
        Agent.move(self)

        # eats
        Agent.eat(self, list_of_foods)  # returns in case a pheromone has been created

        return [None, bebe]

    def update_energy(self, draw):

        if self.new_born == False:

            self.age += 1

            if self.energy > 0:

                if draw:

                    Agent.draw(self)

                # if possible, reproduction
                if self.energy >= Agent.required_energy_to_reproduce:
                    return Agent.reproduce_alone(self)

                # decreases energy
                Agent.aging(self)

            else:
                return "dead"  # dead

        else :
            self.new_born = False

    def find_closest_pheromone(self, list_of_pheromones):
        # this class is for the the basic agents that don't sens pheormones
        return None

    def draw(self):

        CircleEntity.draw(self)

        aff_txt(str(self.energy), self.x, self.y, window=self.screen)

    def move(self):

        self.pos += self.vector
        Agent.update_pos(self)

    def normalize_vect(self):

        self.vector.normalize(self.speed_norm)

    def random_walk(self) :

          # if he s eating we don't change position
          if self.is_eating :

              vect2 = Arr.get_nul([2])

          else:

              vect = self.get_vector()

              #module = sqrt((vect[0]**2 + vect[1]**2))

              if (self.get_y() <= 0) or (self.get_y() >= screen_height) or (self.get_x() <= 0) or (self.get_x() >= screen_width):  # out screen

                self.mode_transitoire = 10

                vect2 = Arr(screen_center)-self.pos  # Arr([-sin(pi*j*1/6),-cos(pi*j*1/6)])

                self.delta_t = random.random()

              else:

                  # back into screen
                  if self.mode_transitoire > 0 :
                       vect2 = vect
                       self.mode_transitoire -= 1

                  #randomized movement
                  else :
                      frequency = 10000
                      #t=0.01
                      amp = 5

                      perturbation = Arr([sin(2*pi*self.delta_t*frequency),cos(2*pi*self.delta_t*frequency)])

                      perturbation.normalize(self.speed_norm/10)

                      vect2 = perturbation+vect

          self.vector = vect2

          Agent.normalize_vect(self)



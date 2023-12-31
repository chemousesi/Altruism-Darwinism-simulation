from pig_tv_csts import *
from utils import *
import json_loader as json_loader
import universe
import button
from importlib import reload
from entity import Entity, CircleEntity

# Classe d'agent racine 
class Agent(CircleEntity):

    reload(json_loader)

    cost_of_reproduction = json_loader.json_data["cost_of_reproduction"]

    required_energy_to_reproduce = json_loader.json_data["required_energy_to_reproduce"]

    prob_of_mutation = json_loader.json_data["prob_of_mutation"]

    def __init__(self, screen, pos=None, type_agent : TypeAgent =None, radius=None, energy=None, color=None, draw_energy=True):

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

        CircleEntity.__init__(self, screen, pos, color, radius)

        #energy
        if energy != None:
            self.energy = energy
        else:
            self.energy = json_loader.json_data["agent_initial_energy"]
        ##

        self.vector = Arr([10, 0])  # Arr.get_nul([2])

        self.speed_norm = json_loader.json_data["agent_speed_norm"]

        self.delta_t = random.random()

        self.mode_transitoire = 0

        self.age = 0

        self.is_eating = False

        self.on_food = False

        self.can_make_pheromone = True

        self.has_reproduced_this_cycle = False

        self.new_born = True

        self.proba_of_gene_proba_change_max = json_loader.json_data["proba_of_gene_proba_change_max"]

        self.draw_energy = draw_energy

        self.square = None

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

            return log(log(x+1)+1)/2  # the "+1" value is due to the fact that log must always be positive

        Agent.add_to_energy(self, -loss_function(age))

    def reproduce_alone(self,object_type,genome,gene_prob):
        child = object_type(self.screen, self.pos, gene_type=genome, gene_proba=gene_prob)

        #child.gene_type =
        #child.gene_proba = gene_prob

        # change = gene + random.randrange(-self.proba_of_gene_proba_change_max*100,self.proba_of_gene_proba_change_max*100,1)/10000
        # if change < 0:
        #     child.gene_proba = 0
        # elif change > 1:
        #     child.gene_proba = 1
        # else :
        #     child.gene_proba = change

        return child

    def eat(self): # Simulate eating on the food spot

        list_of_foods = self.square.foods

        agent_has_eaten = False

        for food in list_of_foods: #checks if the agent is on a food spot

            if food.ressource > 0:

                if (self.pos-food.pos).norme_eucli() < 10:  # close enough

                    self.on_food = True #the agent is on a food
                    self.is_eating = True #the agent is no longer moving

                    energy = food.getting_eaten() #updates the amount of food remaining in the box
                    Agent.add_to_energy(self, energy) #updates the energy of the agent
                    agent_has_eaten =True

        if (agent_has_eaten == False) and (self.on_food == True): #if another agent has eaten the last bit of food of the food before this agent, it still needs to be able to move again or it will be stuck on the food
            self.is_eating = False
            self.can_make_pheromone = True

    def update(self, draw=True ):  # , list_of_foods, list_of_pheromones

        agent_state = Agent.update_energy(self, draw)

        # updates vector then moves
        Agent.random_walk(self)
        Agent.move(self)

        # eats
        Agent.eat(self)  # returns in case a pheromone has been created

        return agent_state

    def update_energy(self, draw): #Changing energy (decreasing when aging and increasing when eating)

        if self.new_born == False:

            self.age += 1

            # decreases energy
            Agent.aging(self)

            if self.energy > 0:

                if draw:

                    Agent.draw(self)

            else:
                return "dead"  # If it has no more energy then it's dead

        else :
            self.new_born = False
        return

    def find_closest_pheromone(self):
        # this class is for the the basic agents that don't sense pheormones
        return None

    def draw(self):

        #CircleEntity.draw(self)

        if self.vector == Arr.get_nul([2]):

            vertical = Arr([1, 0])

        else:

            vertical = self.vector

        vertical.normalize(self.radius)

        horizontal = vertical.get_orth()

        horizontal.normalize(self.radius/2)

        pt_list = (self.pos-vertical-horizontal, self.pos-vertical+horizontal, self.pos+vertical)

        pygame.draw.polygon(self.screen, self.color, pt_list)

        if self.draw_energy:

            aff_txt(str(round(self.energy)), self.x, self.y, window=self.screen)

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

                      perturbation = Arr([sin(2*pi*self.delta_t*frequency),cos(2*pi*self.delta_t*frequency)]) # The movement is sinusoidal and it's random

                      perturbation.normalize(self.speed_norm/10)

                      vect2 = perturbation+vect

          self.vector = vect2

          Agent.normalize_vect(self)








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


        self.vector = Arr([10, 0])  # Arr.get_nul([2])

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
        self.speed_norm = 5

        self.delta_t = random.random()

        self.mode_transitoire = 0

        self.age = 0

        self.is_eating = False

        self.on_food = False

        self.can_make_pheromone = True

        self.has_reproduced_this_cycle = False

        self.new_born = True

    def get_energy(self):

        return self.energy

    def get_vector(self):

        return self.vector

    def get_y(self):

        return self.y

    def get_x(self):

        return self.x

    def reduce_energy(self,loss):
        self.energy -= loss
        return

    def aging(self): #changes the value of the agent based on its age
        age = self.age
        Agent.reduce_energy(self,age)
        if self.energy <= 0:
            return "dead"
        return

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
        Agent.reduce_energy(self,Agent.cost_of_reproduction)
        return child


    def eat(self, list_of_foods, list_of_pheromones):
        agent_has_eaten = False
        for food in list_of_foods: #checks if the agent is on a food spot
            if food.ressource > 0:
                for food_box in food.table: #we could check if the agent is in the food before checking every single food_box in the food
                    if food_box == self.pos:
                        self.on_food = True #the agent is on a food
                        self.is_eating = True #the agent is no longer moving
                        food.getting_eaten() #update the amount of food remaining in the box
                        if self.can_make_pheromone == True and self.type_agent_int == 1: #If the agent just arrived on the food and is altruist, then he spreads pheromones around his location
                            self.can_make_pheromone == False
                            Agent.reduce_energy(self,Agent.cost_of_pheromone)
                            new_pheromone = Pheromone()
                            new_pheromone.x = self.x
                            new_pheromone.y = self.y
                            list_of_pheromones.append(new_pheromone)
                        if food.ressource == 0: #if the agent eats the last bit of food of the food, it can move again
                            self.is_eating = False
                            self.can_make_pheromone = True
                        Agent.reduce_energy(self,Food.food_value) #update the energy of the agent
                        agent_has_eaten =True
        if agent_has_eaten == False and self.on_food == True: #if another agent has eaten the last bit of food of the food before this agent, it still needs to be able to move again or it will be stuck on the food
            self.is_eating = False
            self.can_make_pheromone = True
        return list_of_pheromones, list_of_foods

    def update(self, list_of_pheromones, list_of_foods, list_of_agents, draw=True ):
        if self.new_born == False :
            self.age += 1

            if self.energy > 0:

                Agent.move(self)

                if draw:

                    Agent.draw(self)

                if self.energy >= Agent.required_energy_to_reproduce:
                    list_of_agents.append(Agent.reproduce_alone(self))

                check_alive = Agent.aging(self)

                if check_alive == "death":
                    return -1

                list_of_pheromones, list_of_foods = Agent.eat(self,list_of_foods, list_of_pheromones)

            else:

                return -1  # dead
        else :
            self.new_born = False

    def find_closest_pheromone(self, list_of_pheromones):
        # finds the closest phéromone
        if self.type_agent == TypeAgent.BASIC:
            return None
        elif len(list_of_pheromones) > 0:
            # chercher le phéromone le plus proche
            closest_pheromone = None
            min_ph = list_of_pheromones[0]
            min_dist = distance(min_ph, self)
            for ph in list_of_pheromones:
                dist = distance(ph,self)
                if dist <= ph.radius and dist <= min_dist:
                    min_dist = dist
                    min_ph = ph
            return ph
        else :
            return None

    def move(self):
        # if he s eating we don't change position
        if not self.is_eating :
            self.pos += self.vector

        self.pos += self.vector

        self.x = self.pos[0]
        self.y = self.pos[1]

    def random_walk(self) :
           
          vect = self.get_vector()

          #module = sqrt((vect[0]**2 + vect[1]**2))
         
          if (self.get_y() <= 0) or (self.get_y() >= screen_height) or (self.get_x() <= 0) or (self.get_x() >= screen_width):
           
            self.mode_transitoire = 10
           
            vect2 = Arr(screen_center)-self.pos  # Arr([-sin(pi*j*1/6),-cos(pi*j*1/6)])
           
            vect2.normalize(self.speed_norm)
           
            self.delta_t = random.random()

          else:

              if self.mode_transitoire > 0 :
                   vect2 = vect
                   self.mode_transitoire -= 1
             
              else :
                  frequency = 10000
                  #t=0.01
                  amp = 5
                 
                  perturbation = Arr([sin(2*pi*self.delta_t*frequency),cos(2*pi*self.delta_t*frequency)])
                 
                  perturbation.normalize(self.speed_norm/10)
                 
                  vect2 = perturbation+vect
                 
                  vect2.normalize(self.speed_norm)
                 
          self.vector = vect2
          self.move() #ajouté

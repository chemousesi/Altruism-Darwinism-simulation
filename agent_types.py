from pig_tv_csts import *
from utils import *

from pheromone_smeller_agent import PheromoneSmellerAgent
from pheromone_producer_agent import PheromoneProducerAgent


class Profiteer(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, draw_energy=True):


        self.gene_type = [0 for i in range(json_data["number_type_gene"])]

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.PROFITEER, color=RED, draw_energy=draw_energy)



        self.gene_proba = json_data["initial_prob_of_mutation"]

    def update(self, list_of_foods, list_of_pheromones, draw=True ):

        agent_state = super().update(list_of_foods, list_of_pheromones, draw=True )

        if agent_state == "dead":

            return [None, agent_state]

        # if possible, reproduction
        if self.energy >= super().required_energy_to_reproduce:
            child_genome = [0 for i in range(len(self.gene_type))]
            prob = 0
            for i in range(len(child_genome)):
                mutation = random.random()
                if mutation < self.gene_proba:
                    child_genome[i] = (self.gene_type[i] + 1) % 2
                else :
                    child_genome[i] = self.gene_type[i]
                    prob +=1
            prob = prob /len(child_genome)
            mutation = random.random()
            if mutation < prob:
                bebe = super().reproduce_alone(Profiteer,child_genome,self.gene_proba)
            else:
                bebe = super().reproduce_alone(Altruist,child_genome,self.gene_proba)
            super().add_to_energy(-super().cost_of_reproduction)
            return [None, bebe]

        return [None, None]

    def update_number(self,number_list):
        number_list[2] = number_list[2]+1
#
#     def reproduce_alone(self): #returns the list of the agents after the reproduction cycle
#         #checks if the agent is able to reproduce
#         mutation = random.random()
#         child = Profiteer(self.screen)
#
# ##        if mutation < Agent.prob_of_mutation: #checks weither the child will be the type of its parent or not
# ##            if self.type_agent_int == 1:
# ##                child.type_agent_int = 2
# ##            elif self.type_agent_int == 2:
# ##                child.type_agent_int = 1
# ##            else :
# ##                child.type_agent_int = 0
# ##        else:
# ##            child.type_agent_int = self.type_agent_int
#
#         child.pos = self.pos
#         super().add_to_energy(-super().cost_of_reproduction)
#         return child


class Basic(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, draw_energy=True):


        self.gene_type = [0 for i in range(json_data["number_type_gene"])]


        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1], type_agent=TypeAgent.BASIC, color=BLUE, draw_energy=draw_energy)


        self.gene_proba = 0

    def update(self, list_of_foods, list_of_pheromones, draw=True ):

        agent_state = super().update(list_of_foods, list_of_pheromones, draw=True )

        if agent_state == "dead":

            return [None, agent_state]

        # if possible, reproduction
        if self.energy >= super().required_energy_to_reproduce:
            bebe = super().reproduce_alone(Basic,self.gene_type,0)
            super().add_to_energy(-super().cost_of_reproduction*2)
            return [None, bebe]

        return [None, None]

    def update_number(self,number_list):
        number_list[0] = number_list[0]+1

#     def reproduce_alone(self): #returns the list of the agents after the reproduction cycle
#          #checks if the agent is able to reproduce
#         mutation = random.random()
#         child = Basic(self.screen)
#
# ##        if mutation < Agent.prob_of_mutation: #checks weither the child will be the type of its parent or not
# ##            if self.type_agent_int == 1:
# ##                child.type_agent_int = 2
# ##            elif self.type_agent_int == 2:
# ##                child.type_agent_int = 1
# ##            else :
# ##                child.type_agent_int = 0
# ##        else:
# ##            child.type_agent_int = self.type_agent_int
#
#         child.pos = self.pos
#         super().add_to_energy(-super().cost_of_reproduction)
#         return child


class Altruist(PheromoneProducerAgent):

    def __init__(self, screen, pos=None, draw_energy=True):


        self.gene_type = [1 for i in range(json_data["number_type_gene"])]


        PheromoneProducerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.ALTRUIST, produced_pheromones=2, color=GREEN, draw_energy=draw_energy)


        self.gene_proba = json_data["initial_prob_of_mutation"]

    def update(self, list_of_foods, list_of_pheromones, draw=True ):

        agent_states = super().update(list_of_foods, list_of_pheromones, draw=True )

        if agent_states[1] == "dead":

            return agent_states

        # if possible, reproduction
        if self.energy >= super().required_energy_to_reproduce:
            child_genome = [0 for i in range(len(self.gene_type))]
            prob = 0
            for i in range(len(child_genome)):
                mutation = random.random()
                if mutation < self.gene_proba:
                    child_genome[i] = (self.gene_type[i] + 1) % 2
                else :
                    child_genome[i] = self.gene_type[i]
                    prob +=1
            prob = prob /len(child_genome)
            mutation = random.random()
            if mutation < prob:
                bebe = super().reproduce_alone(Altruist,child_genome,self.gene_proba)
            else:
                bebe = super().reproduce_alone(Profiteer,child_genome,self.gene_proba)
            super().add_to_energy(-super().cost_of_reproduction)
            return [agent_states[0], bebe]

        return agent_states


    def update_number(self,number_list):
        number_list[1] = number_list[1]+1

#     def reproduce_alone(self): #returns the list of the agents after the reproduction cycle
#          #checks if the agent is able to reproduce
#         mutation = random.random()
#         child = Altruist(self.screen)
#
# ##        if mutation < Agent.prob_of_mutation: #checks weither the child will be the type of its parent or not
# ##            if self.type_agent_int == 1:
# ##                child.type_agent_int = 2
# ##            elif self.type_agent_int == 2:
# ##                child.type_agent_int = 1
# ##            else :
# ##                child.type_agent_int = 0
# ##        else:
# ##            child.type_agent_int = self.type_agent_int
#
#         child.pos = self.pos
#         super().add_to_energy(-super().cost_of_reproduction)
#         return child


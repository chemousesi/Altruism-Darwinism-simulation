from pig_tv_csts import *
from utils import *
from importlib import reload
import json_loader as json_loader
from pheromone_smeller_agent import PheromoneSmellerAgent
from pheromone_producer_agent import PheromoneProducerAgent


class Profiteer(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, gene_type=None, gene_proba=None, draw_energy=True):
        reload(json_loader)

        if gene_type == None:

            self.gene_type = [0 for i in range(json_loader.json_data["number_type_gene"])]

        else:

            self.gene_type = gene_type

        if gene_proba == None:

            self.gene_proba = json_loader.json_data["initial_prob_of_mutation"]

        else:

            self.gene_proba = gene_proba

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.PROFITEER, color=RED, draw_energy=draw_energy)

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


class Basic(PheromoneSmellerAgent):

    def __init__(self, screen, pos=None, gene_type=None, gene_proba=None, draw_energy=True):

        reload(json_loader)

        PheromoneSmellerAgent.__init__(self, screen, pos, recognised_pheromones=[1], type_agent=TypeAgent.BASIC, color=BLUE, draw_energy=draw_energy)

        if gene_type == None:

            self.gene_type = [-1 for i in range(json_loader.json_data["number_type_gene"])]

        else:

            self.gene_type = gene_type

        if gene_proba == None:

            self.gene_proba = 0

        else:

            self.gene_proba = gene_proba

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


class Altruist(PheromoneProducerAgent):

    def __init__(self, screen, pos=None, gene_type=None, gene_proba=None, draw_energy=True):
        reload(json_loader)

        PheromoneProducerAgent.__init__(self, screen, pos, recognised_pheromones=[1, 2], type_agent=TypeAgent.ALTRUIST, produced_pheromones=2, color=GREEN, draw_energy=draw_energy)

        if gene_type == None:

            self.gene_type = [1 for i in range(json_loader.json_data["number_type_gene"])]

        else:

            self.gene_type = gene_type

        if gene_proba == None:

            self.gene_proba = json_loader.json_data["initial_prob_of_mutation"]

        else:

            self.gene_proba = gene_proba

    def update(self, list_of_foods, list_of_pheromones, draw=True ):

        agent_states = super().update(list_of_foods, list_of_pheromones, draw=True )

        if agent_states[1] == "dead":

            return agent_states

        # if possible, reproduction
        if self.energy >= super().required_energy_to_reproduce:

            child_genome = [0 for i in range(len(self.gene_type))]  # adn will get filled according to parent genome and random mutations

            for i in range(len(child_genome)):
                mutation = random.random()
                if mutation < self.gene_proba:
                    child_genome[i] = (self.gene_type[i] + 1) % 2
                else :
                    child_genome[i] = self.gene_type[i]

            determinist_gene = random.choice(child_genome)

            if determinist_gene == 1:
                bebe = super().reproduce_alone(Altruist,child_genome,self.gene_proba)
            else:
                bebe = super().reproduce_alone(Profiteer,child_genome,self.gene_proba)

            super().add_to_energy(-super().cost_of_reproduction)  # cost of reproduction
            return [agent_states[0], bebe]

        return agent_states


    def update_number(self,number_list):
        number_list[1] = number_list[1]+1



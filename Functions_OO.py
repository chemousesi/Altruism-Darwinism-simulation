import random
import math
from altruisme import Agent
from pig_tv import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def reproduce_alone(agent, prob_of_mutation): #returns the list of the agents after the reproduction cycle
    if agent.energy >= Agent.required_energy_to_reproduce: #checks if the agent is able to reproduce
        mutation = random.random()
        child = Agent()
        if mutation < prob_of_mutation: #checks weither the child will be the type of its parent or not
            if agent.type_agent_int == 1:
                child.type_agent_int = 2
            elif agent.type_agent_int == 2:
                child.type_agent_int = 1
            else :
                child.type_agent_int = 0
        else:
            child.type_agent_int = agent.type_agent_int
        child.x = agent.x
        child.y = agent.y
        agent.update_energy(Agent.cost_of_reproduction)
        return child
    return


def lose_energy(agent, loss_function): #changes the value of the energy of each agent based on its age (lost_energy = loss_function(age)) and returns the list of agents after energy update
    agent.reduce_energy(agent,loss_function(agent.age))
    if agent.energy <= 0:
        return "dead"
    return


def eat(agent, list_of_foods, list_of_pheromones):
    agent_has_eaten = False
    for food in list_of_food: #checks if the agent is on a food spot
        if food.ressource > 0:
            for food_box in food.table: #we could check if the agent is in the food before checking every single food_box in the food
                if food_box == agent.pos:
                    agent.on_food = True #the agent is on a food
                    agent.is_eating = True #the agent is no longer moving
                    food.getting_eaten() #update the amount of food remaining in the box
                    if agent.can_make_pheromone == True and agent.type_agent_int == 1: #If the agent just arrived on the food and is altruist, then he spreads pheromones around his location
                        agent.can_make_pheromone == False
                        agent.reduce_energy(Agent.cost_of_pheromone)
                        new_pheromone = Pheromone()
                        new_pheromone.x = agent.x
                        new_pheromone.y = agent.y
                        list_of_pheromones.append(new_pheromone)
                    if food.ressource == 0: #if the agent eats the last bit of food of the food, it can move again
                        agent.is_eating = False
                        agent.can_make_pheromone = True
                    agent.reduce_energy(Food.food_value) #update the energy of the agent
                    agent_has_eaten =True
    if agent_has_eaten == False and agent.on_food == True: #if another agent has eaten the last bit of food of the food before this agent, it still needs to be able to move again or it will be stuck on the food
        agent.is_eating = False
        agent.can_make_pheromone = True
    return list_of_pheromones, list_of_foods


class Pheromone:

    radius = 60

    def __init__(self,x,y):
        self.life_span = 40
        self.age = 0
        sel.pos = (self.x,self.y)
        self.x = x
        self.y = y


def update_pheromone(pheromone): #increments the age of every pheromones and removes the ones that have been there for too long, returns the updated list of pheromones
    pheromone.age = pheromone.age + 1
    if pheromone.age > Pheromone.life_span:
        return "dead"
    return

def reproduct_with_a_partner(agent,list_of_agents,prob_of_mutation, required_energy_to_reproduce, cost_of_reproduction, distance_to_reproduct, prob_of_being_altruist): #if two agents are close enough they will reproduce, return the list of the agents after the reproduction cycle
    if agent.energy > required_energy_to_reproduce and agent.has_reproduced_this_cycle == False : # has the agent already reproduced this cycle and is he able to reproduce ?
        for partner in list_of_agents:
            if partner.has_reproduced_this_cycle == False and partner.energy > required_energy_to_reproduce and distance_between_two_agents(agent,partner) < distance_to_reproduct and partner != agent: #checks if any of the other agents is close enough to reproduce (and is able to)
                child = Agent()
                if agent.type_agent_int == partner.type_agent_int and agent.type_agent_int == 1: #both parents are altruist -> same has reproduct_alone
                    mutation = random.random()
                    if mutation < prob_of_mutation:
                        child.type_agent_int = 2
                    else :
                        child.type_agent_int = 1
                elif agent.type_agent_int == partner.type_agent_int and agent.type_agent_int == 2: #both parents are cheaters -> same has reproduct_alone
                    mutation = random.random()
                    if mutation < prob_of_mutation:
                        child.type_agent_int = 1
                    else :
                        child.type_agent_int = 2
                elif agent.type_agent_int != 0 and partner.type_agent_int == 0: #the second parent is basic -> same has reproduct_alone
                    mutation = random.random()
                    if mutation < prob_of_mutation:
                        if agent.type_agent_int == 1:
                            child.type_agent_int = 2
                        else :
                            child.type_agent_int = 1
                    else :
                        if agent.type_agent_int == 1:
                            child.type_agent_int = 1
                        else :
                            child.type_agent_int = 2
                elif agent.type_agent_int == 0 and partner.type_agent_int != 0: #the first parent is basic -> same has reproduct_alone
                    mutation = random.random()
                    if mutation < prob_of_mutation:
                        if partner.type_agent_int == 1:
                            child.type_agent_int = 2
                        else :
                            child.type_agent_int = 1
                    else :
                        if partner.type_agent_int == 1:
                            child.type_agent_int = 1
                        else :
                            child.type_agent_int = 2
                elif agent.type_agent_int == 0 and partner.type_agent_int == 0: #both parents are basic -> the child is basic
                    child.type_agent_int = 0
                elif (agent.type_agent_int == 1 and partner.type_agent_int == 2) or (agent.type_agent_int == 2 and partner.type_agent_int == 1): #parents have different types -> first we check which parent will give its gene, then we check if the gene mutates or not
                    choice_of_type = random.random()
                    mutation = random.random()
                    if choice_of_type < prob_of_being_altruist:
                        if mutation < prob_of_mutation:
                            child.type_agent_int = 2
                        else :
                            child.type_agent_int = 1
                    else :
                        if mutation < prob_of_mutation:
                            child.type_agent_int = 1
                        else :
                            child.type_agent_int = 2
                child.x = agent.x
                child.y = agent.y
                agent.reduce_energy(cost_of_reproduction)
                partner.reduce_energy(cost_of_reproduction)
                agent.has_reproduced_this_cycle = True #the two agents can no longer reproduce this cycle
                partner.has_reproduced_this_cycle = True
    return child

def distance_between_two_agents(agent1, agent2): #calculate the absolute distance between two agents
    return math.sqrt((agent1.x - agent2.x)**2 + (agent1.y - agent2.y)**2)

def update_list_of_each_type(list_of_agents, is_last_cycle, list_of_altruists, list_of_basics, list_of_cheaters, number_of_cycles):
    list_of_altruists.append(0)
    list_of_basics.append(0)
    list_of_cheaters.append(0)
    for agent in list_of_agents:
        if agent.type_agent_int == 0:
            list_of_basics[-1] = list_of_basics[-1] + 1
        elif agent.type_agent_int == 1:
            list_of_altruists[-1] = list_of_altruists[-1] + 1
        elif agent.type_agent_int == 2:
            list_of_cheaters[-1] = list_of_cheaters[-1] + 1
    if is_last_cycle :
        X = [i for i in range(number_of_cycles)]
        Ya = list_of_basics
        Yb = list_of_altruists
        Yc = list_of_cheaters
        plt.plot(X, Ya)
        plt.plot(X, Yb)
        plt.plot(X, Yc)
        plt.show()


# agent1 = Agent()
# agent2 = Agent()
# agent1.energy = 100
# agent2.energy = 100
# agent1.x,agent1.y = agent2.x, agent2.y
# cost = 0
# energy_required = 1
# proba = 0.5
# agent1.type_agent_int = 1
# agent2.type_agent_int = 2
# list = [agent1,agent2]
# #list = reproduct_alone(list,proba,energy_required,cost)
# list = reproduct_with_a_partner(list,0.15, 1, 0, 10, 0)



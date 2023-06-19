import random

def reproduct(list_of_agents, prob_of_mutation, required_energy_to_reproduce, cost_of_reproduction): #prob of mutation between 0 and 1
    for agent in list_of_agents:
        if agent.energy >= required_energy_to_reproduce: #checks if the agent is able to reproduce
            choice_of_type = random.random()
            child = Agent()
            if choice_of_type < prob_of_mutation: #checks weither the child will be the type of its parent or not
                if agent.type_agent_int == 1
                    child.type_agent_int = 2
                elif agent_type_agent_int == 2:
                    child.type_agent_int = 1
                else :
                    child.type_agent_int = 0
            child.x = agent.x
            child.y = agent.y
            list_of_agents.append(child)
            agent.energy = agent.energy - cost_of_reproduction


def lose_energy(list_of_agents, loss_function): #changes the value of the energy of each agent based on its age (lost_energy = loss_function(age))
    for agent in list_of_agents:
        agent.energy = agent.energy - loss_function(agent.age)
        if agent.energey <= 0:
            list_of_agents.remove(agent)

def eat(list_of_agents, list_of_spots, food_value): #food_value = energy given by eating one piece of food
    agent_has_eaten = 0
    for agent in list_of_agents:
        for spot in list_of_spots: #checks if the agent is on a food spot
            if spot.ressource > 0:
                for food_box in spot.table: #we could check if the agent is in the spot before checking every single food_box in the spot
                    if food_box = agent.pos:
                        agent.on_spot = 1 #the agent is on a spot
                        agent.is_eating = 1 #the agent is no longer moving
                        spot.ressource = spot.ressource - 1 #update the amount of food remaining in the box
                        if spot.ressource == 0: #if the agent eats the last bit of food of the spot, it can move again
                            agent.is_eating = 0
                        agent.energy = agent.energy + food_value #update the energy of the agent
                        agent_has_eaten =1
        if agent_has_eaten == 0 and agent.on_spot ==1: #if another agent has eaten the last bit of food before this agent, it still needs to be able to move again or he will be stuck on the spot
            agent.is_eating = 0

class pheromone:

    radius = 60

    def __init__(self,x,y):

        self.x = x
        self.y = y
def update_pheromone()


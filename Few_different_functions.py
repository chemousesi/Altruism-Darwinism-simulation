import random

def reproduct(list_of_agents, prob_of_mutation, required_energy_to_reproduce, cost_of_reproduction): #returns the list of the agents after the reproduction cycle
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
    return list_of_agents


def lose_energy(list_of_agents, loss_function): #changes the value of the energy of each agent based on its age (lost_energy = loss_function(age)) and returns the list of agents after energy update
    for agent in list_of_agents:
        agent.energy = agent.energy - loss_function(agent.age)
        if agent.energy <= 0:
            list_of_agents.remove(agent)
    return list_of_agents


def eat(list_of_agents, list_of_spots, food_value, list_of_pheromones): #food_value = energy given by eating one piece of food
    for agent in list_of_agents:
        agent_has_eaten = False
        for spot in list_of_spots: #checks if the agent is on a food spot
            if spot.ressource > 0:
                for food_box in spot.table: #we could check if the agent is in the spot before checking every single food_box in the spot
                    if food_box = agent.pos:
                        agent.on_spot = True #the agent is on a spot
                        agent.is_eating = True #the agent is no longer moving
                        spot.ressource = spot.ressource - 1 #update the amount of food remaining in the box
                        if agent.can_make_pheromone == True and agent.type_agent_int == 1: #If the agent just arrived on the spot and is altruist, then he spreads pheromones around his location
                            agent.can_make_pheromone == False
                            new_pheromone = Pheromone()
                            new_pheromone.x = agent.x
                            new_pheromone.y = agent.y
                            list_of_pheromones.append(new_pheromone)
                        if spot.ressource == 0: #if the agent eats the last bit of food of the spot, it can move again
                            agent.is_eating = False
                            agent.can_make_pheromone = True
                        agent.energy = agent.energy + food_value #update the energy of the agent
                        agent_has_eaten =True
        if agent_has_eaten == False and agent.on_spot == True: #if another agent has eaten the last bit of food of the spot before this agent, it still needs to be able to move again or it will be stuck on the spot
            agent.is_eating = False
            agent.can_make_pheromone = True
    return list_of_agents, list_of_pheromones


class Pheromone:

    radius = 60

    def __init__(self,x,y):

        self.age = 0
        self.x = x
        self.y = y


def update_pheromone(list_of_pheromones, pheromone_life_span): #increments the age of every pheromones and removes the ones that have been there for too long, returns the updated list of pheromones
    for pheromone in list_of_pheromones:
        pheromone.age = pheromone.age + 1
        if pheromone.age > pheromone_life_span:
            list_of_pheromones.remove(pheromone)
    return list_of_pheromones





from altruisme import *



# gère les déplacement de tous les agents

class Simulator:


    def __init__(list_of_agents) -> None:
        pass


# force_tot = force_phéromone + 


def distance(object_a , object_b):
    return sqrt( (object_a.x - object_b.x)**2 + (object_a.y - object_b.y)**2   )


def update_movements(list_of_agents : list[Agent()], list_of_pheromones : list[Pheromone()]):
    for agent in list_of_agents:
        if agent.is_eating :
            agent.vector = Arr([0, 0])
        else :
            ret = find_closest_pheromone(agent, list_of_pheromones)
            if ret != None:
                # goes to random walk
                agent.vector = Arr([ ret.x - agent.x  , ret.y - agent.y ])
            else :
                # goto pheromone 
                agent.vector = random_walk(agent)

def random_walk(agent):
    agent.vector = Arr(random.randrange(0, 3, 1) -1 ,random.randrange(0, 3, 1) -1, 0)




def find_closest_pheromone(agent, list_of_pheromones):
    if len(list_of_pheromones) > 0:
        # chercher le phéromone le plus proche
        closest_pheromone = None
        min_ph = list_of_pheromones[0]
        min_dist = distance(min_ph, agent)
        for ph in list_of_pheromones:
            dist = distance(ph,agent)
            if dist <= ph.radius and dist <= min_dist:
                min_dist = dist
                min_ph = ph 
        return ph
    else : 
        return None

                






from profiteer import Profiteer 
from pig_tv_csts import *

class Altruist(Profiteer):
    # this class is for altruist an agent that can generate pheromones

    def sendPheromone():
        pass

    def get_color():
        return GREEN

    def eat(self, list_of_foods, list_of_pheromones):
        agent_has_eaten = False
        for food in list_of_foods: #checks if the agent is on a food spot
            if food.ressource > 0:
                for food_box in food.table: #we could check if the agent is in the food before checking every single food_box in the food
                    if food_box == self.pos:
                        self.on_food = True #the agent is on a food
                        self.is_eating = True #the agent is no longer moving
                        food.getting_eaten() #update the amount of food remaining in the box
                        if self.can_make_pheromone == True and self.type_agent.ALTRUIST: #If the agent just arrived on the food and is altruist, then he spreads pheromones around his location
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
    
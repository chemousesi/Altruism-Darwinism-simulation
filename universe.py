from pig_tv_csts import *
from utils import *
from pig_tv import wait
import button
import agent
import pheromone
import matplotlib as mpl
import matplotlib.pyplot as plt

class Universe:

    '''
    attributes
    list_agents

    '''

    button_height = 100

    def __init__(self, screen):

        # universe objects
        self.number_of_initial_basic_agents = json_data["number_of_basic_agents"]
        self.number_of_initial_altruist_agents =json_data["number_of_altruist_agents"]
        self.number_of_initial_profiteer_agents =json_data["number_of_profiteer_agents"]
        
        # respectively basic , altruist , profiteer agents
        self.number_of_agents_list = [0,0,0]
        
        self.agents = []

        self.pheromones = []

        self.foods = []

        # graphic interface

        self.screen = screen

        # buttons

        self.buttons = []

        self.selected_button = None

        self.list_of_basics = []

        self.list_of_altruists = []

        self.list_of_cheaters = []

    def add_agent(self, agent):

        self.agents.append(agent)
        agent.update_number(self.number_of_agents_list)
        

    def add_button(self, object_, screen, string):

        n_button = object_(screen, 0, Universe.button_height*len(self.buttons), string, "0")

        self.buttons.append(n_button)

    def add_food_source(self, object_, screen, nb=1):

        for i in range(nb):

            n_food = object_(Arr(get_random_point_in_screen()), screen)

            self.foods.append(n_food)

    def add_pheromone(self, pos, type_pheromone, life_span):

        n_pheromone = pheromone.Pheromone(pos, self.screen, type_pheromone, life_span)

        self.pheromones.append(n_pheromone)

    def update_buttons(self, draw, mouse_clicked, user_input):

        mouse_pos = pygame.mouse.get_pos()

        button_got_clicked = False

        for button in self.buttons:

            # drawing if necessary

            if draw:

                button.draw()

            # modifying val of selected button

            if self.selected_button != None:

                self.selected_button.update_val(user_input)

            # updating clicked button

            if mouse_clicked:

                if button.clicked(mouse_pos):

                    button_got_clicked = True

                    if not self.selected_button == button:

                        self.selected_button = button

                        button.set_clicked(True)

        if mouse_clicked and (self.selected_button != None) and (not button_got_clicked):

            self.selected_button.set_clicked(False)

            self.selected_button = None

    def update_foods(self, draw):

        for food in self.foods:

            food.update(draw)

            if food.available_food:

                Universe.add_pheromone(self, food.pos, type_pheromone=1, life_span=1)

    def update_pheromones(self, draw):

        for pheromone in self.pheromones:

            if pheromone.update(draw) == -1:

                self.pheromones.remove(pheromone)

    def update(self, draw, mouse_clicked, user_input,time):

        Universe.update_buttons(self, draw, mouse_clicked, user_input)

        Universe.update_pheromones(self, draw)

        Universe.update_foods(self, draw)

        # agent update
        for agent in self.agents:
            #print(len(self.agents))

            pheromones = self.pheromones
            foods  = self.foods
            agents = self.agents

            pheromone_return, agent_return = agent.update(foods, pheromones, draw)

            if agent_return == "dead" : # when the agent has no more energy we kill him
                agents.remove(agent)

                if agent.type_agent_int == 0:
                    self.list_of_basics[-1] -= 1
                elif agent.type_agent_int == 1:
                    self.list_of_altruists[-1] -= 1
                elif agent.type_agent_int == 2:
                    self.list_of_cheaters[-1] -= 1

                

            # baby
            elif agent_return != None:
                self.add_agent(agent_return)
                
                

            if (pheromone_return != None) and (pheromone_return[0] == "pheromone"):
                Universe.add_pheromone(self, agent.pos, pheromone_return[1], pheromone_return[2])

        Universe.make_graph(self, time)

    def make_graph(self, time):
        self.list_of_altruists.append(0)
        self.list_of_basics.append(0)
        self.list_of_cheaters.append(0)
        for agent in self.agents:
            if agent.type_agent_int == 0:
                self.list_of_basics[-1] += 1
            elif agent.type_agent_int == 1:
                self.list_of_altruists[-1] +=1
            elif agent.type_agent_int == 2:
                self.list_of_cheaters[-1] += 1

        X = [i for i in range(time)]
        Ya = self.list_of_basics
        Yb = self.list_of_altruists
        Yc = self.list_of_cheaters
        plt.plot(X, Ya)
        plt.plot(X, Yb)
        plt.plot(X, Yc)

    def show_graph(self):
        plt.show()
        wait()
        return




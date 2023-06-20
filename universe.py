from pig_tv_csts import *
from utils import *

import button
import agent


class Universe:

    '''
    attributes
    list_agents

    '''

    button_height = 100

    def __init__(self):

        # universe objects

        self.agents = []

        self.pheromones = []

        self.foods = []

        # graphic interface

        # buttons

        self.buttons = []

        self.selected_button = None

    def add_agent(self, agent):

        self.agents.append(agent)

    def add_button(self, object_, screen, string):

        n_button = object_(screen, 0, Universe.button_height*len(self.buttons), string, "0")

        self.buttons.append(n_button)

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


    def update(self, draw, mouse_clicked, user_input):

        Universe.update_buttons(self, draw, mouse_clicked, user_input)

        # agent update

        Universe.update_movements(self)

        for agent in self.agents:
            #print(len(self.agents))
            pheromones = self.pheromones
            foods  = self.foods
            agents = self.agents
            agent.update( pheromones, foods, agents, draw)


    def update_movements(self):

        for agent in self.agents:

            if agent.is_eating:
                agent.set_vector(Arr([0, 0]))

            else :

                phero = agent.find_closest_pheromone(self.pheromones)
                if phero != None:
                    # goes to pheromone
                    agent.vector = Arr([ phero.x - agent.x  , phero.y - agent.y ])
                else :
                    # goto randomwalk
                    agent.random_walk()



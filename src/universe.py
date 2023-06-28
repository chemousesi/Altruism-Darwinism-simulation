from pig_tv_csts import *
from utils import *

from pig_tv import wait, clock
import button
import agent
import pheromone
from importlib import reload
import json_loader as json_loader


from panel import Panel

import matplotlib as mpl
import matplotlib.pyplot as plt
from food_spot import Food
from square import Square

class Universe:

    '''
    attributes
    list_agents

    '''

    def __init__(self, screen):
        reload(json_loader)

        # universe objects
        self.number_of_initial_basic_agents = json_loader.json_data["number_of_basic_agents"]
        self.number_of_initial_altruist_agents =json_loader.json_data["number_of_altruist_agents"]
        self.number_of_initial_profiteer_agents =json_loader.json_data["number_of_profiteer_agents"]

        # respectively basic , altruist , profiteer agents
        self.number_of_agents_list = [0,0,0]

        self.agents = []

        self.pheromones = []

        self.foods = []

        self.tigres = []

        # graphic interface

        self.screen = screen

        # buttons

        self.buttons = []

        self.selected_button = None

        # panns

        self.altruist_panel = None

        self.profiteer_panel = None

        self.basic_panel = None

        self.panels = []

        ## lists

        self.list_of_basics = []

        self.list_of_altruists = []

        self.list_of_cheaters = []

        self.list_of_average_altruist_genome = []

        self.list_of_average_cheater_genome = []

        # grid

        self.square_size = json_loader.json_data["grid_square_size"]

        self.grid = [[Square(i, j, screen) for j in range(screen_width//self.square_size)] for i in range(screen_height//self.square_size)]

        ##
        self.average_basics= 0

        self.average_altruists = 0

        self.average_cheaters = 0

    def add_agent(self, agent):

        self.agents.append(agent)
        agent.update_number(self.number_of_agents_list)


    def add_button(self, object_, screen, string):

        n_button = object_(screen, 0, Universe.button_height*len(self.buttons), string, "0")

        self.buttons.append(n_button)

    def set_profiteer_panel(self, object_, screen):
        self.profiteer_panel = self.add_panel(object_, screen)

    def set_altruist_panel(self, object_, screen):
        self.altruist_panel = self.add_panel(object_, screen)

    def set_basic_panel(self, object_, screen):
        self.basic_panel = self.add_panel(object_, screen)

    def add_panel(self, object_, screen, string=""):

        x, y = 0, Panel.height*len(self.panels)

        draw_decal = 30

        draw_function = object_(screen, Arr([x+draw_decal, y+draw_decal]), draw_energy=False).draw

        n_pan = Panel(screen, x, y, string, draw_function)

        self.panels.append(n_pan)

        return n_pan

    def add_food_source(self, object_, screen, nb):

        for n in range(nb):

            j, i = random.randint(0, screen_width//self.square_size-1), random.randint(0, screen_height//self.square_size-1)

            x, y = int((j+0.5)*self.square_size), int((i+0.5)*self.square_size)

            n_food = object_(Arr([x, y]), screen)

            self.foods.append(n_food)

            self.add_food_grid(n_food)

    def add_food_source_with_mouse(self, object_, mousepos, screen):

        n_food = object_(Arr(mousepos), screen)
        self.foods.append(n_food)

    def initialize_food_with_mouse(self, screen, number_of_spots):

        if number_of_spots > 0:

            self.add_food_source(Food, screen, number_of_spots)

        else :
        
            time = 0
            draw = True
            run = True
            while run:

                time += 1

                clicked = False

                user_input = None

                # user events

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        run = False

                    elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                        clicked = True
                        # ici il faut gérer le food spawn
                        self.add_food_source_with_mouse(Food, pygame.mouse.get_pos(),screen)

                    elif event.type == pygame.KEYDOWN:
                            
                        if event.key == pygame.K_RETURN:
                            return 

                # drawing and updating universe

                if draw:
                    screen.fill(GREY)

                #univers.updateMovement()
                self.update(draw, clicked, user_input, time, initialisation=True)
                if draw:

                    pygame.display.update()
                    clock.tick(60)

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

                self.add_phero_grid(self.pheromones[-1])

    def update_pheromones(self, draw):

##        for line in self.grid:
##
##            for square in line:
##
##                square.empty_pheromones()   

        for pheromone in self.pheromones:

            if pheromone.update(draw) == -1:

                self.pheromones.remove(pheromone)

                for sq in pheromone.squares:

                    sq.del_pheromone(pheromone)

    def update_panels(self):

        for pan in self.panels:

            pan.draw()

    def update(self, draw, mouse_clicked, user_input,time, initialisation=False):

        #print(self.grid)

        #Universe.update_buttons(self, draw, mouse_clicked, user_input)

        if draw:

            self.draw()

        Universe.update_pheromones(self, False)  # draw

        Universe.update_foods(self, draw)

        average_genome = 0

        # agent update
        for agent in self.agents:

            self.add_to_grid(agent)

            genome = agent.gene_type

            res = agent.update(draw)

            pheromone_return, agent_return = res

            #pheromone_return, agent_return = agent.update(draw)  # foods, pheromones, draw)
            if pheromone_return != None:

                self.add_pheromone(pheromone_return[3],pheromone_return[1],pheromone_return[2])

                self.add_phero_grid(self.pheromones[-1])

            if agent_return == "dead" : # when the agent has no more energy we kill him

                self.agents.remove(agent)


            # baby
            elif agent_return != None:

                self.add_agent(agent_return)

##        # tigres
##        for tigre in self.tigres:
##
##            dead_agent, state = tigre.update(list_of_pheromones=self.pheromones, agents=self.agents, draw=draw)
##
##            if state == "dead":
##
##                self.tigres.remove(tigre)
##
##            if dead_agent in self.agents:
##
##                self.agents.remove(dead_agent)
##
##                
##
##        ##

        if not initialisation:

            Universe.make_graph(self)

        if draw:

            self.update_panels()

        Universe.update_average(self)

    def draw(self):

        for line in self.grid:

            for square in line:

                square.draw()

    def add_phero_grid(self, phero):

        range_ = phero.type_pheromone

        range_ = range_*2-1  # maps to (1;3)

        #print(phero.pos)

        i, j = round((phero.y-self.square_size//2)/self.square_size), round((phero.x-self.square_size//2)/self.square_size)

        for k in range(-range_+1, range_):  # if big pheromone, reaches more squares

            for l in range(-range_+1, range_):

                u, v = i+k, j+l

                #print((k, l), u, v)

                if (0<=u<len(self.grid)) and (0<=v<len(self.grid[0])):

                    square = self.grid[u][v]

                    square.add_pheromone(phero)

                    #print(k, l)

                    phero.squares.append(square)

    def add_food_grid(self, food):

        i, j = round((food.y-self.square_size//2)/self.square_size), round((food.x-self.square_size//2)/self.square_size)

        square = self.grid[i][j]

        square.add_food(food)

    def add_to_grid(self, agent):

        last_square = agent.square

        i, j = round((agent.y-self.square_size//2)/self.square_size), round((agent.x-self.square_size//2)/self.square_size)

        if i < 0:

            i = 0

        if i > screen_height//self.square_size-1:

            i = screen_height//self.square_size-1

        if j < 0:

            j = 0

        if j > screen_height//self.square_size-1:

            j = screen_height//self.square_size-1

        square = self.grid[i][j]

        if square != last_square:

            square.add_entity(agent)

            if last_square:

                last_square.del_entity(agent)

        #self.grid[i][j].append_entity(entity)

            agent.square = self.grid[i][j]

    def update_list_basics(self, val):
        self.list_of_basics[-1] += val


    def update_list_profiteers(self, val):
        self.list_of_cheaters[-1] += val


    def update_list_altruists(self, val):
        self.list_of_altruists[-1] += val


    def make_graph(self):
        self.list_of_altruists.append(0)
        self.list_of_basics.append(0)
        self.list_of_cheaters.append(0)
        self.list_of_average_altruist_genome.append(0)
        self.list_of_average_cheater_genome.append(0)
        for agent in self.agents:
            if agent.type_agent_int == 0:
                self.update_list_basics(1)
            elif agent.type_agent_int == 1:
                self.list_of_altruists[-1] +=1
            elif agent.type_agent_int == 2:
                self.list_of_cheaters[-1] += 1

        self.altruist_panel.string = str(self.list_of_altruists[-1])
        self.profiteer_panel.string = str(self.list_of_cheaters[-1])
        self.basic_panel.string = str(self.list_of_basics[-1])

        for agent in self.agents:
            if agent.type_agent_int == 1:
                for elt in agent.gene_type:
                    if elt ==1:
                        self.list_of_average_altruist_genome[-1] += 1
            elif agent.type_agent_int == 2:
                for elt in agent.gene_type:
                    if elt ==1:
                        self.list_of_average_cheater_genome[-1] += 1

        if self.list_of_altruists[-1]>0:
            self.list_of_average_altruist_genome[-1]=self.list_of_average_altruist_genome[-1]/self.list_of_altruists[-1]
        if self.list_of_cheaters[-1] >0:
            self.list_of_average_cheater_genome[-1]=self.list_of_average_cheater_genome[-1]/self.list_of_cheaters[-1]




    def show_graph(self):
        Ya = self.list_of_basics
        Yb = self.list_of_altruists
        Yc = self.list_of_cheaters
        Yd = self.list_of_average_altruist_genome
        Ye = self.list_of_average_cheater_genome
        X = [i for i in range(len(Ya))]
        plt.plot(X, Ya, "b", label="basics")
        plt.plot(X, Yb, "g", label="altruists")
        plt.plot(X, Yc, "r", label="profiteers")
        plt.plot(X, Yd, "y", label="prob_mutation_altruist")
        plt.plot(X, Ye, "p", label="prob_mutation_profiteer")
        plt.legend(loc='best')
        plt.show()

        return

    def show_genes(self):

        altruists_genes = []

        profiteers_genes = []

        indexs = []

        for agent in self.agents:

            genes = agent.gene_type

            if genes[0] != -1:

                altruists_genes.append(sum(genes))

                profiteers_genes.append(len(genes)-sum(genes))

                indexs.append(agent.type_agent_int-1)

        x = range(len(altruists_genes)) # position en abscisse des barres

        # tracing diagram
        largeur_barre = 0.8

        plt.bar(x, altruists_genes, width = largeur_barre, color = "#00FF00")

        plt.bar(x, profiteers_genes, width = largeur_barre, bottom = altruists_genes, color = "#FF0000")

        plt.xticks(range(len(altruists_genes)), [(["a", "p"])[indexs[i]] for i in range(len(indexs))])

        plt.show()

    def update_average(self):
        avg = 0
        for elt in self.list_of_basics:
            avg += elt/len(self.list_of_basics)
        self.average_basics = avg
        avg = 0
        for elt in self.list_of_altruists:
            avg += elt/len(self.list_of_altruists)
        self.average_altruists = avg
        avg = 0
        for elt in self.list_of_cheaters:
            avg += elt/len(self.list_of_cheaters)
        self.average_cheaters = avg






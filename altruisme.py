from pig_tv import *
class Agent:

    dico_color = {"altruiste":GREEN, "profiteur":RED, "basique":BLUE}

    dico_type_agent = {"altruiste":1, "profiteur":2, "basique":0}

    cost_of_reproduction = 40

    required_energy_to_reproduce = 50

    cost_of_pheromone = 10

    def __init__(self, pos=None, type_agent=None, radius=None, energy=None):

        if pos != None:

            self.pos = pos

        else:

            self.pos = Arr(get_random_point_in_screen())

        self.x = self.pos[0]

        self.y = self.pos[1]

        self.vector = Arr([10, 0])  # Arr.get_nul([2])

        # type_agent
        if type_agent != None:

            self.type_agent = type_agent

        else:

            self.type_agent = "basique"

        self.type_agent_int = Agent.dico_type_agent[self.type_agent]
        ##

        # radius
        if radius != None:

            self.radius = radius

        else:

            self.radius = 10
        ##

        self.color = Agent.dico_color[self.type_agent]

        #energy
        if energy != None:

            self.energy = energy

        else:

            self.energy = 1
        ##

        self.age = 0

        self.is_eating = False

        self.on_food = False

        self.can_make_pheromone = True

        self.has_reproduced_this_cycle = False

    def get_energy(self):

        return self.energy

    def get_vector(self):

        return self.vector

    def get_y(self):

        return self.y

    def get_x(self):

        return self.x

    def reduce_energy(self,loss):
        self.energy -= loss
        return

    def aging(self): #changes the value of the agent based on its age
        age = self.age
        Agent.reduce_energy(self,age)
        if self.energy <= 0:
            return "dead"
        return

    def reproduce_alone(self, prob_of_mutation): #returns the list of the agents after the reproduction cycle
         #checks if the agent is able to reproduce
        mutation = random.random()
        child = Agent()
        if mutation < prob_of_mutation: #checks weither the child will be the type of its parent or not
            if self.type_agent_int == 1:
                child.type_agent_int = 2
            elif self.type_agent_int == 2:
                child.type_agent_int = 1
            else :
                child.type_agent_int = 0
        else:
            child.type_agent_int = self.type_agent_int
        child.x = self.x
        child.y = self.y
        Agent.reduce_energy(self,Agent.cost_of_reproduction)
        return child


    def eat(self, list_of_foods, list_of_pheromones):
        agent_has_eaten = False
        for food in list_of_foods: #checks if the agent is on a food spot
            if food.ressource > 0:
                for food_box in food.table: #we could check if the agent is in the food before checking every single food_box in the food
                    if food_box == self.pos:
                        self.on_food = True #the agent is on a food
                        self.is_eating = True #the agent is no longer moving
                        food.getting_eaten() #update the amount of food remaining in the box
                        if self.can_make_pheromone == True and self.type_agent_int == 1: #If the agent just arrived on the food and is altruist, then he spreads pheromones around his location
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

    def update(self, prob_of_mutation, list_of_pheromones, list_of_foods, list_of_agents,draw=True ):

        self.age += 1

        if self.energy > 0:

            Agent.update_vect(self)

            Agent.move(self)

            if draw:

                Agent.draw(self)

            if self.energy >= Agent.required_energy_to_reproduce:
                list_of_agents.append(Agent.reproduce_alone(self, prob_of_mutation))

            check_alive = Agent.aging(self)

            if check_alive == "death":
                return -1

            list_of_pheromones, list_of_foods = Agent.eat(self,list_of_foods, list_of_pheromones)

        else:

            return -1  # dead


    def draw(self):

        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def move(self):

        self.pos += self.vector

        self.x = self.pos[0]

        self.y = self.pos[1]

    def update_vect(self) :
      b = random.randint(0,4)
      vect = self.get_vector()
      module = sqrt((vect[0]**2 + vect[1]**2))
      if (self.get_y() <= 0) :
        for i in range(5):
          j=i+1
          if (b == i) :
            vect2 =Arr([cos(pi*j*1/6),sin(pi*j*1/6)])
            vect2 = vect2 * module
      elif(self.get_y() >= screen_height) :
        for i in range(5):
          j=i+1
          if (b == i) :
            vect2 =Arr([cos(pi*j*1/6),-sin(pi*j*1/6)])
            vect2 = vect2 * module
      elif(self.get_x() <= 0) :
        for i in range(5):
          j=i+1
          if (b == i) :
            vect2 =Arr([sin(pi*j*1/6),-cos(pi*j*1/6)])
            vect2 = vect2 * module
      elif(self.get_x() >= screen_width):
         print("hi")
         for i in range(5):
          j=i+1
          if (b == i) :
            vect2 =Arr([-sin(pi*j*1/6),-cos(pi*j*1/6)])
            vect2 = vect2 * module
      else:
        vect2 = vect

      self.vector = vect2
      self.move() #ajouté

##

class Pheromone:

    radius = 60

    life_span = 40

    def __init__(self,x,y):

        self.age = 0
        sel.pos = (self.x,self.y)
        self.x = x
        self.y = y

    def update_pheromone(self):
        self.age += 1
        if self.age > Pheromone.life_span:
            return "dead"
        return

##

class Button:

    back_color = WHITE

    deco_color = BLACK

    selected_color = RED

    def __init__(self, x, y, string, default_val=None):

        self.x = x

        self.y = y

        self.width = 200

        self.height = 75

        self.string = string

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.deco_decal = 5

        self.txt_decal_x = 2*self.deco_decal

        self.txt_decal_y = 5

        self.rect_deco = pygame.Rect(self.x+self.deco_decal, self.y+self.deco_decal, self.width-2*self.deco_decal, self.height-2*self.deco_decal)

        self.state_clicked = False

        self.val = default_val

    def draw(self):

        pygame.draw.rect(screen, Button.back_color, self.rect)

        if not self.state_clicked:

            pygame.draw.rect(screen, Button.deco_color, self.rect_deco, 3)

        else:

            pygame.draw.rect(screen, Button.selected_color, self.rect_deco, 3)

        aff_txt(self.string, self.x+self.txt_decal_x, self.y+self.txt_decal_y, taille=20)

        aff_txt(self.val, self.x+self.txt_decal_x, self.y+30+self.txt_decal_y)

    def clicked(self, mouse_pos):

        clicked = collide_point_to_rect(mouse_pos, self.rect)

        return collide_point_to_rect(mouse_pos, self.rect)

    def set_clicked(self, val):

        self.state_clicked = val

    def update_val(self, user_input):

        n_val = self.val

        if user_input != None:

            n_val += user_input

        Button.modify_val(self, n_val)

    def modify_val(self, n_val):

        self.val = n_val



class Univers:

    button_height = 100

    def __init__(self):

        self.agents = []

        # graphic interface

        # buttons

        self.buttons = []

        self.clicked_button = None

    def add_agent(self, agent):

        self.agents.append(agent)

    def add_button(self, string):

        button = Button(0, Univers.button_height*len(self.buttons), string, "0")

        self.buttons.append(button)

    def update_buttons(self, draw, mouse_clicked):

        user_input = None

        mouse_pos = pygame.mouse.get_pos()

        button_got_clicked = False

        for button in self.buttons:

            # drawing if necessary

            if draw:

                button.draw()

            # updating clicked button

            if mouse_clicked:

                if button.clicked(mouse_pos):

                    button_got_clicked = True

                    if not self.clicked_button == button:

                        self.clicked_button = button

                        button.set_clicked(True)

                # updating value of clicked button

                if button.state_clicked:

                    button.update_val(user_input)

        if mouse_clicked and (self.clicked_button != None) and (not button_got_clicked):

            self.clicked_button.set_clicked(False)

            self.clicked_button = None


    def update(self, draw, mouse_clicked):

        Univers.update_buttons(self, draw, mouse_clicked)

        # agent update

        for agent in self.agents:

            agent.update(draw,[],[],[])




def main():

    univers = Univers()

    univers.add_agent(Agent())

    univers.add_button("proba mutation")

    temps = 0

    draw = True

    run = True

    while run:

        temps += 1

        clicked = False


        # user events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicked = True

        # drawing and updating universe
        if draw:

            screen.fill(GREY)

        univers.update(draw, clicked)

        if draw:

            pygame.display.update()

            clock.tick(60)

    return


if __name__ == "__main__":

    main()

















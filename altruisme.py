from pig_tv import *
from utils import *


class Agent:

    dico_color = {TypeAgent.ALTRUIST:GREEN, TypeAgent.PROFITEER:RED, TypeAgent.BASIC:BLUE}

    cost_of_reproduction = 40

    required_energy_to_reproduce = 50

    cost_of_pheromone = 10

    def __init__(self, pos=None, type_agent : TypeAgent =None, radius=None, energy=None):



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

            self.type_agent = TypeAgent.BASIC


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

        self.on_spot = False

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

    def update(self, draw=True):

        self.age += 1

        if self.energy > 0:

            Agent.move(self)

            if draw:

                Agent.draw(self)

        else:

            return -1  # dead

    def find_closest_pheromone(self, list_of_pheromones):
        # finds the closest phéromone
        if self.type_agent == TypeAgent.BASIC:
            return None
        elif len(list_of_pheromones) > 0:
            # chercher le phéromone le plus proche
            closest_pheromone = None
            min_ph = list_of_pheromones[0]
            min_dist = distance(min_ph, self)
            for ph in list_of_pheromones:
                dist = distance(ph,self)
                if dist <= ph.radius and dist <= min_dist:
                    min_dist = dist
                    min_ph = ph
            return ph
        else :
            return None

    def draw(self):

        pygame.draw.circle(screen, self.color, self.pos.with_fun_applied(int), self.radius)

    def move(self):
        # if he s eating we don't change position
        if not self.is_eating :
            self.pos += self.vector

        self.pos += self.vector

        self.x = self.pos[0]
        self.y = self.pos[1]

    def random_walk(self) :
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
            for i in range(5):
                j=i+1
                if (b == i) :
                    vect2 =Arr([-sin(pi*j*1/6),-cos(pi*j*1/6)])
                    vect2 = vect2 * module
        else:
            vect2 = vect

        self.vector = vect2
        self.move() #ajouté


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

    '''
    attributes
    list_agents

    '''



    button_height = 100

    def __init__(self):

        # universe objects

        self.agents = []

        self.pheromones = []

        # graphic interface

        # buttons

        self.buttons = []

        self.selected_button = None

    def add_agent(self, agent):

        self.agents.append(agent)

    def add_button(self, string):

        button = Button(0, Univers.button_height*len(self.buttons), string, "0")

        self.buttons.append(button)

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

        Univers.update_buttons(self, draw, mouse_clicked, user_input)

        # agent update

        Univers.update_movements(self)

        for agent in self.agents:

            agent.update(draw)


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

        user_input = None


        # user events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicked = True

            elif event.type == pygame.KEYDOWN:

                string = event.unicode

                if string != "":

                    user_input = string

                    
        # drawing and updating universe
        if draw:

            screen.fill(GREY)

        #univers.updateMovement()
        univers.update(draw, clicked, user_input)

        if draw:

            pygame.display.update()

            clock.tick(60)

    return


if __name__ == "__main__":

    main()

















from pig_tv_csts import *
from utils import *

import universe
import button


class Agent:

    dico_color = {TypeAgent.ALTRUIST:GREEN, TypeAgent.PROFITEER:RED, TypeAgent.BASIC:BLUE}

    cost_of_reproduction = 40

    required_energy_to_reproduce = 50

    cost_of_pheromone = 10

    def __init__(self, screen, pos=None, type_agent : TypeAgent =None, radius=None, energy=None):

        self.screen = screen

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

        pygame.draw.circle(self.screen, self.color, self.pos.with_fun_applied(int), self.radius)

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

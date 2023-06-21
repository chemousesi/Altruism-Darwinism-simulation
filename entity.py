from pig_tv_csts import *
from utils import *


class Entity:

    def __init__(self, screen, pos=None):

        self.screen = screen

        if pos != None:

            self.pos = pos

        else:

            self.pos = Arr(get_random_point_in_screen())

        self.x = self.pos[0]

        self.y = self.pos[1]

    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def update_pos(self):

        self.x = self.pos[0]
        self.y = self.pos[1]


class CircleEntity(Entity):

    def __init__(self, screen, pos=None, color=None, radius=None) :

        Entity.__init__(self, screen, pos)
        # graphical information

        if color != None:

            self.color = color

        else:

            self.color = YELLOW

        if radius != None:

            self.radius = radius

        else:

            self.radius = 10

    def draw(self):

        pygame.draw.circle(self.screen, self.color, self.pos.with_fun_applied(int), self.radius)


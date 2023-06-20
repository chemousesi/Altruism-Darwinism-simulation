from pig_tv_csts import *
from utils import *


class Entity:

    def __init__(self, pos, color, radius, screen) :

        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

        # graphical information

        self.color = color
        self.radius = radius
        self.screen = screen

    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def update_pos(self):

        self.x = self.pos[0]
        self.y = self.pos[1]

    def draw(self):

        pygame.draw.circle(self.screen, self.color, self.pos.with_fun_applied(int), self.radius)


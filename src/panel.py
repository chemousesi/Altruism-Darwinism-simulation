from pig_tv_csts import *
from utils import *
from json_loader import *
import universe
import agent


class Panel:

    back_color = WHITE

    deco_color = BLACK

    height = json_data["button_height"]

    def __init__(self, screen, x, y, string, dessin=None):

        self.x = x

        self.y = y

        self.screen = screen

        self.width = json_data["button_width"]

        self.height = Panel.height

        self.string = string

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.deco_decal = 5

        self.txt_decal_x = 10*self.deco_decal

        self.txt_decal_y = 15

        self.rect_deco = pygame.Rect(self.x+self.deco_decal, self.y+self.deco_decal, self.width-2*self.deco_decal, self.height-2*self.deco_decal)

        self.dessin = dessin

    def draw(self):

        pygame.draw.rect(self.screen, Panel.back_color, self.rect)

        pygame.draw.rect(self.screen, Panel.deco_color, self.rect_deco, 3)

        aff_txt(self.string, self.x+self.txt_decal_x, self.y+self.txt_decal_y, taille=30, window=self.screen)

        self.dessin()


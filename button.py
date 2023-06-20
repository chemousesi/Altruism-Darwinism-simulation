from pig_tv_csts import *
from utils import *

import universe
import agent


class Button:

    back_color = WHITE

    deco_color = BLACK

    selected_color = RED

    def __init__(self, screen, x, y, string, default_val=None):

        self.x = x

        self.y = y

        self.screen = screen

        self.width = json_data["button_width"]

        self.height = json_data["button_height"]

        self.string = string

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.deco_decal = 5

        self.txt_decal_x = 2*self.deco_decal

        self.txt_decal_y = 5

        self.rect_deco = pygame.Rect(self.x+self.deco_decal, self.y+self.deco_decal, self.width-2*self.deco_decal, self.height-2*self.deco_decal)

        self.state_clicked = False

        self.val = default_val

    def draw(self):

        pygame.draw.rect(self.screen, Button.back_color, self.rect)

        if not self.state_clicked:

            pygame.draw.rect(self.screen, Button.deco_color, self.rect_deco, 3)

        else:

            pygame.draw.rect(self.screen, Button.selected_color, self.rect_deco, 3)

        aff_txt(self.string, self.x+self.txt_decal_x, self.y+self.txt_decal_y, taille=20, window=self.screen)

        aff_txt(self.val, self.x+self.txt_decal_x, self.y+30+self.txt_decal_y, window=self.screen)

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



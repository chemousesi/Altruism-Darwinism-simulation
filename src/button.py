from pig_tv_csts import *
from utils import *

import universe
import agent

from panel import Panel


class Button(Panel):

    back_color = WHITE

    deco_color = BLACK

    selected_color = RED

    def __init__(self, screen, x, y, string, default_val=None):

        super().__init__(screen, x, y, string)

        self.state_clicked = False

        self.val = default_val

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

    def draw(self):

        super.draw()

        if self.state_clicked:

            pygame.draw.rect(self.screen, Button.deco_color, self.rect_deco, 5)

        aff_txt(self.val, self.x+self.txt_decal_x, self.y+30+self.txt_decal_y, window=self.screen)




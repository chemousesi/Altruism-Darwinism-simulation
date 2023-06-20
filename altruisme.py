from pig_tv import *
from utils import *

from universe import Universe
from button import Button
from agent import Agent



def main():

    universe = Universe()

    universe.add_agent(Agent(screen))

    universe.add_button(Button, screen, "proba mutation")

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
        universe.update(draw, clicked, user_input)

        if draw:

            pygame.display.update()

            clock.tick(60)

    return


if __name__ == "__main__":

    main()

















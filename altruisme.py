from pig_tv import *
from utils import *


from universe import Universe
from button import Button
from agent import Agent
from food_spot import Food
from agent_types import Basic, Profiteer, Altruist



def main():

    universe = Universe(screen)
    i1 = universe.number_of_initial_basic_agents
    i2 = universe.number_of_initial_altruist_agents
    i3 = universe.number_of_initial_profiteer_agents

    for x in range(i1):
        universe.add_agent(Basic(screen))
    for x in range(i2):
        universe.add_agent(Altruist(screen))
    for x in range(i3):
        universe.add_agent(Profiteer(screen))

    #universe.add_button(Button, screen, "proba mutation")

    universe.add_food_source(Food, screen, 10)

    time = 0

    draw = True

    run = True

    while run:

        run == len(universe.agents) > 0

        time += 1

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

                    if string == "g":

                        universe.show_graph()

                    user_input = string

        # drawing and updating universe
        if draw:
            screen.fill(GREY)

        #univers.updateMovement()
        universe.update(draw, clicked, user_input, time)

        if draw:

            pygame.display.update()

            wait()

            clock.tick(60)

    return


if __name__ == "__main__":

    main()

















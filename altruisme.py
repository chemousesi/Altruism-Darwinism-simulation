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

    if number_of_spots > 0:
        universe.add_food_source(Food, screen, number_of_spots)
    else :
        universe.initialize_food_with_mouse(screen)


    for x in range(i1):
        universe.add_agent(Basic(screen))
    for x in range(i2):
        universe.add_agent(Altruist(screen))
    for x in range(i3):
        universe.add_agent(Profiteer(screen))

    #universe.add_button(Button, screen, "proba mutation")

    universe.set_profiteer_panel(Profiteer, screen)

    universe.set_altruist_panel(Altruist, screen)

    universe.set_basic_panel(Basic, screen)

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
                # ici il faut gérer le food spawn
                #universe.add_food_source_with_mouse(Food, pygame.mouse.get_pos(),screen)

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


            clock.tick(600)

    return


if __name__ == "__main__":

    main()


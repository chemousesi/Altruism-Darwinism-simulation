from pig_tv import *
from utils import *


from universe import Universe
from button import Button
from agent import Agent
from food_spot import Food



def main():

    universe = Universe(screen)

    universe.add_agent(Agent(screen))
    universe.add_agent(Agent(screen))
    universe.add_agent(Agent(screen))
    universe.add_agent(Agent(screen))


    universe.add_button(Button, screen, "proba mutation")

    universe.add_food_source(Food, screen, 10)

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

def initiate_food_spots(screen_width,screen_height,number_of_spots):
    for i in range(number_of_spots):
        colonne = int(random.random()*screen_width)
        ligne = int(random.random()*screen_height)
        food_spot = Food()
        food_spot.x = colonne
        food_spot.y = ligne
















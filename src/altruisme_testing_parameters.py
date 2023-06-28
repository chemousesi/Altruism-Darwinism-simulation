from pig_tv import *
from utils import *
from pig_tv_csts import *
import os
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import shutil

from universe import Universe
from button import Button
from agent import Agent
from food_spot import Food
from agent_types import Basic, Profiteer, Altruist
from tigre import Tigre
import json_loader as json_loader
from importlib import reload


def main(parameter_to_test, nb_iter_to_test_for, initial_value, end_value, step, number_of_times = 3): #parameter_to_test is a string which has the name of the parameter in the json file

    list_value_parameter = []
    list_average_number_of_altruists = []
    list_average_number_of_basics = []
    list_average_number_of_cheaters = []
    list_min_altruists = []
    list_max_altruists = []
    list_min_cheaters = []
    list_max_cheaters = []
    list_min_basics = []
    list_max_basics = []

    value = initial_value
    while value <= end_value:
        list_value_parameter.append(value)
        print(value)

        jsonFile = open("parameters.json", "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file

        ## Working with buffered content
        tmp = data[parameter_to_test]
        data[parameter_to_test] = value

        ## Save our changes to JSON file
        jsonFile = open("parameters.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        liste_alt=[]
        liste_prof=[]
        liste_bas=[]
        value += step
        reload(json_loader)
        for i in range(int(number_of_times)):


            universe = Universe(screen)
            i1 = universe.number_of_initial_basic_agents
            i2 = universe.number_of_initial_altruist_agents
            i3 = universe.number_of_initial_profiteer_agents
            number_of_spots = json_loader.json_data["number_of_spots"]

            #universe.add_button(Button, screen, "proba mutation")

            # graphics
            universe.set_profiteer_panel(Profiteer, screen)

            universe.set_altruist_panel(Altruist, screen)

            universe.set_basic_panel(Basic, screen)

            # food initialisation
            if number_of_spots > 0:
                universe.add_food_source(Food, screen, number_of_spots)
            else :
                universe.initialize_food_with_mouse(screen)

            ## places initial agents

            for x in range(i1):
                universe.add_agent(Basic(screen))
            for x in range(i2):
                universe.add_agent(Altruist(screen))
            for x in range(i3):
                universe.add_agent(Profiteer(screen))

            #universe.add_food_source(Food, screen, number_of_spots)

            time = 0

            draw = False

            run = True

            while run:

                run == len(universe.agents) > 0

                time += 1

                clicked = False

                user_input = None

                # user events
                if time > nb_iter_to_test_for:

                    run = False

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        run = False

                    elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                        clicked = True

                        universe.tigres.append(Tigre(screen, Arr(pygame.mouse.get_pos())))
                        # ici il faut gérer le food spawn
                        #universe.add_food_source_with_mouse(Food, pygame.mouse.get_pos(),screen)

                    elif event.type == pygame.KEYDOWN:

                        string = event.unicode

                        if string != "":

                            if string == "g":

                                universe.show_graph()

                            elif string == "d":

                                draw = not(draw)

                            elif string == "h":

                                universe.show_genes()

                            elif string == "p":

                                universe.print_average_pop()

                            user_input = string



                # drawing and updating universe
                #if draw:
                 #   screen.fill(GREY)co

                #univers.updateMovement()
                universe.update(draw, clicked, user_input, time)

                if draw:

                    #pygame.display.update()


                    clock.tick(60)

            liste_bas.append(universe.average_basics)
            liste_prof.append(universe.average_cheaters)
            liste_alt.append(universe.average_altruists)
        list_max_altruists.append(max(liste_alt))
        list_max_cheaters.append(max(liste_prof))
        list_max_basics.append(max(liste_bas))
        list_min_altruists.append(min(liste_alt))
        list_min_cheaters.append(min(liste_prof))
        list_min_basics.append(min(liste_bas))
        avrg = 0
        for elt in liste_bas:
            avrg += elt/len(liste_bas)
        list_average_number_of_basics.append(avrg)
        avrg = 0
        for elt in liste_alt:
            avrg += elt/len(liste_alt)
        list_average_number_of_altruists.append(avrg)
        avrg = 0
        for elt in liste_prof:
            avrg += elt/len(liste_prof)
        list_average_number_of_cheaters.append(avrg)

    # plot the graphs
    plt.plot(list_value_parameter,list_average_number_of_altruists,"g",label="average number of altruists")
    plt.plot(list_value_parameter,list_average_number_of_cheaters,"r",label="average number of cheaters")
    plt.plot(list_value_parameter,list_average_number_of_basics,"b",label="average number of basics")
    
    # plot the max
    plt.scatter(list_value_parameter,list_max_altruists,c="green")
    plt.scatter(list_value_parameter,list_max_basics,c="blue")
    plt.scatter(list_value_parameter,list_max_cheaters,c="red")
    plt.scatter(list_value_parameter,list_min_altruists,c="green")
    plt.scatter(list_value_parameter,list_min_basics,c="blue")
    plt.scatter(list_value_parameter,list_min_cheaters,c="red")
    plt.legend(loc='best')
    plt.show()
    return


if __name__ == "__main__":
    parameter_to_test = input("What parameter is to be tested ?")
    nb_iter_to_test_for = int(input("How many iterations should the test make ?"))
    initial_value = float(input("What is the inital value of the parameter ?"))
    end_value = float(input("What is the end value of the parameter ?"))
    step = float(input("What is the step that the parameter should take ?"))
    main(parameter_to_test, nb_iter_to_test_for, initial_value, end_value, step)

def max(liste):
    max = 0
    for elt in liste:
        if elt > max:
            max = elt
    return max

def min(liste):
    min = 1000000
    for elt in liste:
        if elt < min:
            min = elt
    return min

def average(liste):
    avrg = 0
    for elt in liste:
        avrg += elt/len(liste)
    return avrg
# Gr19-1
# Altruism-Darwinism-simulation
A simulation software of altruism and darwinism written in python with pygame library

- For an updated software please check this github [link](https://github.com/chemousesi/Altruism-Darwinism-simulation)\


- To run the simulation, you need to run the file : `altruisme.py`.
- You can edit the parameters in paramaters.json
- If the number of food spots in `parameters.json` is 0, we have a blank universe and put food with the mouse and then click `enter` key on the keyboard
- To display the graphic of the whole simulation at any moment you click the `g` key on the keyboard




the parameters of the simulation can be changed in the file parameters.json

it is possible to see the evolution of the different populations by pressing the key "g" during the simulation



```
cd existing_repo
git remote add origin https://gitlab.telecom-paris.fr/PAF/2223/gr19-1.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [x] [Set up project integrations](https://gitlab.telecom-paris.fr/PAF/2223/gr19-1/-/settings/integrations)

## The team
- Chems-eddine Benaziza
- Romain David
- Yanis Aît El Kadi
- Joseph Maillard
- Achraf Jarrar


## Test and Deploy

Use the built-in continuous integration in GitLab.

- you need python installed to deploy this, using pygame library
- a makefile will be available soon

***




## Description


This project aims to study whether altruistic behaviour is viable from a Darwinian evolution

perspective. The modelled world features a number of food sources, placed randomly, with predefined quantities and sizes of occupied surfaces. When a food source is depleted (i.e. eaten) it reappears in a

different location (randomly picked). A set of agents (organisms) can move through the world (e.g. random walks or levy walks). If food is on the patch they are on, they can eat it, thus increasing their energy. When an agent reaches a certain level of energy, it replicates. When its energy becomes too low, it dies-off.

There are three species of agents: 1. Basic agents: search for food by walking around; 2. Altruistic agents: signal food presence upon finding it, via a chemical diffused in the environment; and, are able to walk up the gradient of the chemical produced by another agent to find food faster. The agents consume energy to produce the signalling chemical; 3. Profiteer agents: can walk up the gradient of the chemical produced by another agent to find food faster; but do not produce the chemical when finding food themselves, thus saving energy.

An agent of either Altruistic or Profiteer type will produce an offspring of either the same type (with probability p) or of the opposite type (with probability 1-p). This probability p mutates slightly at each generation.

Starting with different mixes of populations and various configuration settings, analyse whether the altruists can survive or are always wiped out by the profiteers.


## Visuals
- UI made using pygame
- picture of the final result here



## Installation
nothing to install except python and pygame : 
`pip install pygame`

## Usage
lanch `altruisme.py`
- to put you parameters you have to edit the file `parameteres.json`
- To display a graph type 'g'
- To dislpay genoms type 'h'
  Note : If the number of food spots in 'parameters.json' then you can use the mouse to put the food spots   
## Roadmap
[] This first release modelizes the movement of agents in a nature. 
[] modelize three types of agents
[] modelize the ag 



## Authors and acknowledgment
We a team of five at telecom paris !
Thanks to all teachers who helped us work :

- Chems-eddine Benaziza
- Romain David
- Yanis Aît El Kadi
- Joseph Maillard
- Achraf Jarrar

Big thanks to the teachers who supervised us:
- Ada Diaconescu
- Jean-Louis Dessales

## License
Open source code, but please cite us
## Project status

This is a [télécom paris](https://www.telecom-paris.fr/) end of the year school project, e are not sure of 
but if you have any suggesting ideas you can contact us mainters or drop an email at : 
chems.benaziza [at] gmail.com
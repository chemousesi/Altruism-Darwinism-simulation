import pygame, sys, random
from pygame.locals import *


class Device:
    def __init__(self, id, x, y , z, x_vel, y_vel, z_vel):
            self.__id = id
            self.__x = x
            self.__y = y
            self.__z = z
            self.__x_vel = x_vel
            self.__y_vel = y_vel
            self.__z_vel = z_vel
            print('Created a new device', id, 'at x:', x, 'y:',y, 'z:',z, '')

    def info(self):
        print('This is an instance of device', self.__id, 'at x:', self.__x, 'y:', self.__y, 'z:', self.__z, '')

    def returnDeviceInfo(self):
        return(self.__id,self.__x,self.__y,self.__z)

    def Setdevicevelocity(self, x_vel, y_vel, z_vel):
        self.__x_vel = x_vel
        self.__y_vel = y_vel
        self.__z_vel = z_vel

    def Moveobjectbasedonvelocity(self):
        self.__x = self.__x + self.__x_vel
        self.__y = self.__y + self.__y_vel
        self.__z = self.__z + self.__z_vel

pygame.init()  # initialize pygame

# Colours RGB
BACKGROUND = (255, 255, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
DEVICES = 200

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('DNA Spaces - Analysis')

# The main function that controls the game

def main(d):
    looping = True

    # The main game loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # processing code inside to rendering loop to save cpu

        # Render elements
        for i in range(len(d)):
            d[i].Setdevicevelocity(random.randrange(0, 10, 1) -1 ,random.randrange(0, 10, 1) -1, 0) # do a random walk
            ident, x, y, z = d[i].returnDeviceInfo()
            d[i].Moveobjectbasedonvelocity()
            pygame.draw.circle(WINDOW, (0,0,0), (x, y), 1)
        pygame.display.update()
        WINDOW.fill(BACKGROUND)
        fpsClock.tick(FPS)


d = []

for i in range(0,DEVICES,1):
    d.append(Device(i,random.randrange(0,WINDOW_WIDTH,1),random.randrange(0,WINDOW_HEIGHT,1),0,0,0,0)) # add instances of Device(s) to array
main(d)
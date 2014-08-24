import random 
from global_vars import *
from gameobjects.util import euclidean
import pygame

class Planet(object):
    free_id = 0

    #creates a random planet
    def __init__(self):
        self.__pl_id = Planet.free_id
        Planet.free_id+=1

        self.x = random.choice( range(16, DISP_W-16)  )
        self.y = random.choice( range(16, DISP_H-16)  )
        self.rad = random.choice( range( MIN_PLANET_RAD, MAX_PLANET_RAD) )

	#return True/False whether the considered planet overlaps with another one
    def overlaps(self, t_planet):
        return ( euclidean( (t_planet.x,t_planet.y),(self.x,self.y) ) < self.rad+t_planet.rad+MIN_EMPTY_SPACE )

    def is_bad_pick( self,existing_planets) :
        if (self.x+self.rad>=DISP_W-1) or (self.x-self.rad<=0):
            return True
        if (self.y+self.rad>=DISP_H-1) or (self.y-self.rad<=BORDER_UP):
            return True
        for t_planet in existing_planets:
            if self.__overlaps(t_planet ):
                return True
        return False
    
    def getId(self):
        return self.__pl_id

    def draw(self,window,alt_color=False):
        if(not alt_color):
            pygame.draw.circle(window, DARK_BLUE, (self.x,self.y), self.rad,  0 ) #last arg means disk instead of circle
            return
        pygame.draw.circle(window, LIGHT_BLUE, (self.x,self.y), self.rad,  0 ) #last arg means disk instead of circle

    #given the (mx,my) position of click, returns whether the planet is cliked or not
    def isClicked(self, mx,my):
        return euclidean((mx,my),(self.x,self.y))<= self.rad+UI_PIX_TOLERANCE
    

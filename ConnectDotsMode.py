# -*- coding: utf8 -*-

from ldt_blocks.GameMode import *
from global_vars import *
import pygame
from pygame.locals import *

from EndGameMode import *


( STEP_PROMPT,  STEP_DEST ) = range(2)

( ACT_EXIT, ACT_TEST_LK, ACT_ADD_LK, ACT_SEL_DECT ) = range(4)

class ConnectDotsMode( GameMode ):

    def __init__(self, universe):
        self.game_lost = False
        self.coord_pl_tested =None
        self.current_step = STEP_PROMPT
        self.act = None

        #init selection
        self.universe = universe
        self.l_planets = universe.getPlanets()
        self.id_p_selected = universe.getIdPlayersPlanet()

        for planet in self.l_planets:
            if(self.id_p_selected==planet.getId()):
                self.org_x = planet.x
                self.org_y = planet.y
                self.org_rad = planet.rad
                break

        self.id_p_over = None
        self.over_p_x = None
        self.over_p_y = None
        self.simu_link = None

        self.id_p_chosen = None
        self.chosen_p_x= None
        self.chosen_p_y = None
    
        self.new_dest = None
        self.reboot_landing = False


    def handle(self, events):
        for event in events:
            if event.type == QUIT:
                self.act= ACT_EXIT
                return

            if self.current_step==STEP_PROMPT and (event.type == MOUSEBUTTONDOWN ):
                self.vect_m = pygame.mouse.get_pos()
                self.act= ACT_ADD_LK
               

            if self.current_step==STEP_PROMPT and (event.type == MOUSEMOTION ):
                self.vect_m = pygame.mouse.get_pos()
                self.act= ACT_TEST_LK


            if(self.current_step== STEP_DEST) and (event.type== MOUSEBUTTONDOWN):
                (mx,my) = pygame.mouse.get_pos()
                for planet in self.l_planets:
                    if(not planet.getId() in self.universe.getIdsRP()  ):
                        continue
                    #if mouse-over other planet
                    if(planet.isClicked(mx,my) and planet.getId()!=self.id_p_selected ):
                        self.new_dest = planet.getId()
                

    def update(self, gm_model):
        from gameobjects.vector2 import Vector2

        if(self.act==ACT_EXIT):
            gm_model.signalQuit()
            return

        if self.act==ACT_ADD_LK: 
            id_p = det_planet_clicked( self.l_planets, self.vect_m)
            if(id_p!=None):
                #retrieve pl coordinates
                for pl in self.l_planets:
                    if pl.getId()==id_p:
                        coord_pl = pl.x, pl.y
                        break
                #adding link
                gm_model.addIdRP( id_p )
                gm_model.addLink( coord_pl )
                self.current_step = STEP_DEST
            else:
                #click in the void!
                self.act=None

        if self.act==ACT_TEST_LK:
            id_p = det_planet_clicked( self.l_planets, self.vect_m)
            if(id_p!=None):
                #retrieve pl coordinates
                for pl in self.l_planets:
                    if pl.getId()==id_p:
                        self.coord_pl_tested = pl.x, pl.y
                        break
            else:
                #move in the void!
                self.coord_pl_tested =None

        #updating bars
        gm_model.update()

        if gm_model.isGameLost():
            self.game_lost = True
            return


        if(self.current_step==STEP_DEST and self.new_dest!=None):
            self.id_p_selected = self.new_dest
            gm_model.setIdPlayersPlanet( self.new_dest)
            self.reboot_landing = True
            

    def shouldChangeMode(self):
        return self.reboot_landing or self.game_lost

    def getNextMode(self):
        if(self.game_lost):
            return EndGameMode()

        from LandingMode import LandingMode
        return LandingMode()

    def drawScreen(self, window, gm_model):
        y_border = generic_screen(window, gm_model)
        for lk in self.universe.getLinks():
            pygame.draw.line(window, LIGHT_BLUE, lk[0], lk[1] )

        
        if(self.current_step==STEP_PROMPT):
            addmsg_line(window, "Choose a planet to build a teleporter.")

            if(self.coord_pl_tested!=None):
                pygame.draw.line(window, LIGHT_BLUE,
                    gm_model.getCurrentCoord(),
                    self.coord_pl_tested )
            return
    
        if(self.current_step== STEP_DEST):
            addmsg_line(window, "Where do you want to travel now?")


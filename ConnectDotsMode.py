# -*- coding: utf8 -*-

from ldt_blocks.GameMode import *
from global_vars import *
import pygame
from pygame.locals import *

from EndGameMode import *



( ACT_EXIT, ACT_TEST_LK, ACT_ADD_LK, ACT_SEL_DEST, ACT_WARP ) = range(5)

class ConnectDotsMode( GameMode ):

    def __init__(self, universe):
        self.warp_possible = False
        self.game_lost = False
        self.coord_pl_tested =None
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
        self.super_reboot = False


    def handle(self, events):
        for event in events:
            if event.type == QUIT:
                self.act= ACT_EXIT
                return

            if (event.type == KEYDOWN ):
                self.act = ACT_WARP

            if (event.type == MOUSEBUTTONDOWN ):
                self.vect_m = pygame.mouse.get_pos()
                if( event.button==1): #left click
                    self.act = ACT_ADD_LK
                elif( event.button==3): #right click
                    self.act = ACT_SEL_DEST
                return

            if (event.type == MOUSEMOTION ):
                self.vect_m = pygame.mouse.get_pos()
                self.act= ACT_TEST_LK
                

    def update(self, gm_model):
        if( gm_model.hasMaxTeleporters() ):
            self.warp_possible = True

        from gameobjects.vector2 import Vector2

        if(self.act==ACT_EXIT):
            gm_model.signalQuit()
            return

        if self.act==ACT_ADD_LK or self.act==ACT_SEL_DEST: 
            # retrieving clickd pl coordinates
            id_p = det_planet_clicked( self.l_planets, self.vect_m)
            coord_pl = None
            is_reachable = False
            for pl in self.l_planets:
                if pl.getId()==id_p:
                    coord_pl = pl.x, pl.y
                    is_reachable = (id_p in self.universe.getIdsRP()  )
                    break

            if coord_pl!=None:
                if self.act==ACT_ADD_LK:
                    if not gm_model.hasMaxTeleporters():
                        #adding link
                        gm_model.addLink( coord_pl, id_p )
                if self.act==ACT_SEL_DEST and is_reachable and id_p!=gm_model.getIdPlayersPlanet() :
                    #we save the new destination only if its a reachable planet
                    self.new_dest = id_p

        if self.act==ACT_WARP:
            gm_model.pause()
            gm_model.resetLinks()
            self.reboot_landing = True
            self.super_reboot = True
                        


        if self.act==ACT_TEST_LK:
            id_p = det_planet_clicked( self.l_planets, self.vect_m)
            if(id_p!=None and not gm_model.hasMaxTeleporters() ):
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

        if(  self.new_dest!=None):
            self.id_p_selected = self.new_dest
            gm_model.setIdPlayersPlanet( self.new_dest)
            self.reboot_landing = True
            

    def shouldChangeMode(self):
        return self.reboot_landing or self.game_lost

    def getNextMode(self):
        if(self.game_lost):
            return EndGameMode()

        from LandingMode import LandingMode
        if(self.super_reboot):
            return LandingMode( True)

        return LandingMode()

    def drawScreen(self, window, gm_model):
        y_border = generic_screen(window, gm_model)
        for lk in self.universe.getLinks():
            pygame.draw.line(window, LIGHT_BLUE, lk[0], lk[1] )

        
        addmsg_line(window, "Build a teleporter (l-click) or move to a new destination (r-click)")

        if(self.coord_pl_tested!=None):
            pygame.draw.line(window, LIGHT_BLUE,
                gm_model.getCurrentCoord(),
                self.coord_pl_tested )
    

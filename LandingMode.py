from ldt_blocks.GameMode import *
from global_vars import *
import random
import pygame
from pygame.locals import *
from gameobjects import util
from ProgressBar import *
from ConnectDotsMode import *
from EndGameMode import *

from FontTool import *
from World import *

( STEP_LAND, STEP_WAITING, STEP_RESULT, STEP_CHANGING_M ) = range(4)

( ACT_EXIT, ACT_PICK_LANDING, ACT_CONFIRM_RESULT ) = range(3)

class LandingMode(GameMode ):

    def __init__(self, first_run=False, already_visited=False):
        self.game_lost = False
        self.act = None
        self.current_step = None

        if(not first_run):
            self.current_step = STEP_WAITING
            if(not already_visited):
                self.prog_bar = ProgressBar( FIGHT_DUR, "Fighting aliens:" ) 
            else:
                self.prog_bar = ProgressBar(  0)  #finished direct
        else:
            self.current_step = STEP_LAND
            self.prog_bar = None

    def handle(self, events):
        for event in events:
            if event.type == QUIT:
                self.act = ACT_EXIT
                return
            if (self.current_step==STEP_LAND and event.type == pygame.MOUSEBUTTONDOWN):
                self.act = ACT_PICK_LANDING
                self.mx,self.my = pygame.mouse.get_pos()
                continue
            if (self.current_step==STEP_RESULT and event.type == pygame.KEYDOWN):
                self.act = ACT_CONFIRM_RESULT
                continue

    def shouldChangeMode(self):
        return self.current_step==STEP_CHANGING_M or self.game_lost
        
    def getNextMode(self):
        if(self.game_lost):
            return EndGameMode()

        return ConnectDotsMode( self.__saved_gm_model )

    def update(self, gm_model):
        if( gm_model.isPaused()  ):
            gm_model.unpause()

        if (self.act==ACT_EXIT):
            gm_model.signalQuit()
            return
        if (self.act==ACT_PICK_LANDING):
            #do we clicked a valid planet?
            tmp_id = det_planet_clicked( gm_model.getPlanets(), (self.mx,self.my) )
            if( tmp_id==None):
                return

            # init sounds + starting MUSIC !
            SfxPlayer.start()

            #we change the current step only if a planet has been clicked
            gm_model.setIdPlayersPlanet( tmp_id )
            self.act=None
            self.current_step = STEP_WAITING
            self.prog_bar = ProgressBar()
            return

        if (self.act==ACT_CONFIRM_RESULT):
            #gm_model.unpause()
            self.current_step = STEP_CHANGING_M
            self.act=None

        if self.current_step==STEP_WAITING:
            if self.prog_bar.isFinished():
                if( not gm_model.isGameLost() ):
                    gm_model.produceReward()
                    #gm_model.pause()
                    self.current_step = STEP_RESULT
                return

            # sounds of fight
            pygame.time.delay(400)
            SfxPlayer.fight()

            if not self.prog_bar.isFinished():
                self.prog_bar.update()


        #in all other cases, we have to update player infos
        if(self.current_step!=STEP_LAND ):
            gm_model.update()
            if( gm_model.isGameLost() ):
                self.game_lost = True
                return



    def drawScreen(self, window, gm_model):
        self.__saved_gm_model = gm_model

        if self.current_step!=STEP_LAND:
            y_border = generic_screen(window, gm_model)
        else:
            y_border = screen_simple(window, gm_model.getPlanets() )

        if(self.current_step==STEP_LAND ):
            addmsg_line( window, "Click a planet to land!")
            return

        #if(self.current_step==STEP_LOST):
            #def_cause = gm_model.getDefeatCause()
            #rpg_msg = FontTool.draw_txt1( def_cause )
            #height_txt = rpg_msg.get_size()[1]
            #blit_center(window, rpg_msg, (DISP_H/2)-(height_txt/2)  )
            #return

        if(self.current_step==STEP_WAITING or self.current_step==STEP_RESULT ):
            addmsg_line( window, compl("Fighting aliens:")+ str(self.prog_bar) )

        if(self.current_step==STEP_RESULT):
            rpg_msg = FontTool.draw_txt1( "You have collected "+gm_model.getDescLastReward()  )
            height_txt = rpg_msg.get_size()[1]
            blit_center(window, rpg_msg, (DISP_H/2)-(height_txt/2)  )


        # diplays edges
        #for nodes_pair in assoc_matr:
        #    if( assoc_matr[ nodes_pair ] ): # the two nodes are linked
        #        x1,y1 = coord_nodes[ nodes_pair[0] ]
        #        x2,y2 = coord_nodes[ nodes_pair[1] ]
        #        pygame.draw.line(window, DISP_COLOR,
        #            (x1*CELL_PX_SIZE,y1*CELL_PX_SIZE),
        #            (x2*CELL_PX_SIZE,y2*CELL_PX_SIZE)  )
    
        #assoc_matr = dict()
        #for i in xrange( cnt_nodes):
        #for j in xrange(cnt_nodes):
        #if j>=i:
        #    continue
        #assoc_matr[ (i,j) ] = True if (random.choice(range(4))==0 ) else False


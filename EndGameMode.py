from ldt_blocks.GameMode import *
from global_vars import *
import pygame
from pygame.locals import *
from FontTool import *

( STEP_BAD_NEWS ) = range(1)
( ACT_EXIT ) = range(1)


class EndGameMode( GameMode ):
    def __init__(self):
        self.step = STEP_BAD_NEWS
        self.act=None
        self.model_stopped = False

    def handle(self, events):
        for event in events:
            if event.type == QUIT:
                self.act = ACT_EXIT
            if(self.step==STEP_BAD_NEWS and event.type == pygame.MOUSEBUTTONDOWN):
                self.act = ACT_EXIT

    def update(self, gm_model):

        if (self.act==ACT_EXIT):
            gm_model.signalQuit()
            return

        if(not self.model_stopped):
            gm_model.pause()
            self.model_stopped = True

    def drawScreen(self, window, gm_model):
        y_border = generic_screen(window, gm_model)
        def_cause = gm_model.getDefeatCause()
        rpg_msg = FontTool.draw_txt1( def_cause )
        height_txt = rpg_msg.get_size()[1]
        blit_center(window, rpg_msg, (DISP_H/2)-(height_txt/2)  )

    def shouldChangeMode(self):
        return False
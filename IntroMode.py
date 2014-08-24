
from ldt_blocks.GameMode import *
from global_vars import *
from LandingMode import *
import pygame
from pygame.locals import *

from FontTool import *

class IntroMode(GameMode ):
    def __init__(self):
        self.quit = False
        self.font_init = False
        self.ready_to_play= False

    def handle(self, events):
        for event in events:

            if event.type == QUIT:
                self.quit = True
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.ready_to_play= True

    def shouldChangeMode(self):
        return self.ready_to_play
        
    def getNextMode(self):
        return LandingMode(True)

    def update(self, gm_model):
        if(self.quit):
            gm_model.signalQuit()
            return

    def drawScreen(self, window, gm_model):

        if(not self.font_init):
            pygame.font.init()
            self.font_init=True

        window.fill(BLACK)

        dx = (DISP_W/2)
        dy = 140
        def draw_penta(window,color,offset):
            pygame.draw.polygon( window,color,
                ((dx,dy+0), (dx+145,dy+106), (dx+90,dy+277), (dx-90,dy+277), (dx-146,dy+106)))

        draw_penta(window, BLUE, 0)
        for i in xrange(0,DISP_H-(dy+230) ,4):
            pygame.draw.line( window, BLUE_GRAY, (0,dy+230+i), (DISP_W-1,dy+230+i), 4)

        title = FontTool.draw_txt1("SPACE ADDICT")
        author = FontTool.draw_txt2("a game created by @spartangeek" )
        author2 = FontTool.draw_txt2("in less than 48 hours for Ludum Dare 30" )
        start_msg = FontTool.draw_txt2( "-Press the mouse button to start-" )

        window.blit( title, (dx-146-32,170) )
        window.blit(  author, (dx-146-32,310) )
        window.blit(  author2, (dx-146-32,340) )
        window.blit( start_msg, (dx-146-32,460) )


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
                ((dx,dy+0-32-8), (dx+145,dy+106-32-8), (dx+90,dy+277-32-8), (dx-90,dy+277-32-8), (dx-146,dy+106-32-8)))

        draw_penta(window, BLUE, 0)
        for i in xrange(0,DISP_H-(dy+230) ,4):
            pygame.draw.line( window, BLUE_GRAY, (0,dy+230+i), (DISP_W-1,dy+230+i), 4)

        title = FontTool.draw_txt1("SPACE ADDICT")
        author = FontTool.draw_txt2("code - music - graphics by @spartangeek" )
        author2 = FontTool.draw_txt2("created for the Ludum Dare 30" )

        tuto1= FontTool.draw_txt2( "The aim of this game is to gather ressources")
        tuto2= FontTool.draw_txt2( "on various planets and survive as long as possible!")

        tuto3= FontTool.draw_txt2( "Use MOUSE with left/right clicks to teleport/build teleporters" )
        tuto4= FontTool.draw_txt2( "hit SPACE key after visiting a planet to continue")
        tuto5= FontTool.draw_txt2( "you have only 5 teleporter, hit ENTER to reclaim them all")

        window.blit( title, (dx-146,185) )
        window.blit(  author, (dx-146-32,310) )
        window.blit(  author2, (dx-146-32,340) )

        window.blit( tuto1, (dx-146-128-32,380 +25) )
        window.blit( tuto2, (dx-146-128-32,380 +50) )

        window.blit( tuto3, (dx-146-128-32,380 +100) )
        window.blit( tuto4, (dx-146-128-32,380 +125) )
        window.blit( tuto5, (dx-146-128-32,380 +150) )

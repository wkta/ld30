import pygame, sys
from pygame.locals import *
from ldt_blocks.GameMode import *
from global_vars import *
from IntroMode import *


pygame.init()
DISPLAYSURF = pygame.display.set_mode( (DISP_W, DISP_H), 0, 32  )
pygame.display.set_caption( GAME_CAPTION )

st = IntroMode()
mod = World()

# game loop based on the current state
while not mod.gameExit():
    st.handle( pygame.event.get() )
    # state update
    if(st.shouldChangeMode()):
        st = st.getNextMode()

    # game model update
    st.update( mod)

    # drawing
    st.drawScreen( DISPLAYSURF, mod)
    pygame.display.update()


pygame.quit()

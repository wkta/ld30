"""
Space Addict: the game

Copyright (C) 2014 Thomas IWASZKO
contact: tiwaszko@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see:
https://www.gnu.org/licenses/gpl-3.0.txt.
"""

import pygame, sys
from pygame.locals import *
from ldt_blocks.GameMode import *
from global_vars import *
from IntroMode import *


# - init.
pygame.init()
DISPLAYSURF = pygame.display.set_mode( (DISP_W, DISP_H), 0, 32  )
pygame.display.set_caption( GAME_CAPTION )

st = IntroMode()
mod = World()

license_msg = '\
Space Addict: the game.  Copyright (C) 2014.  Thomas IWASZKO\n\
This program comes with ABSOLUTELY NO WARRANTY;\n\
This is free software, and you are welcome to redistribute it\n\
under certain conditions; for details check:\n\
https://github.com/wkta/ld30/ or the GPL 3.0 LICENSE.'
print('-'*32)
print(license_msg)
print('-'*32)
print()

# - game loop
while not mod.gameExit():
    st.handle( pygame.event.get() )

    if(mod.gameRestart() ):
        mod = World()

    # state update
    if(st.shouldChangeMode()):
        st = st.getNextMode()

    # game model update
    st.update( mod)

    # drawing
    st.drawScreen( DISPLAYSURF, mod)
    pygame.display.update()

pygame.quit()

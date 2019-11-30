import pygame
from FontTool import *
from def_colors import *

DISP_W = 800
DISP_H = 600
GAME_CAPTION = 'Space Addict: the game - LudumDare#30'

#procedurally generated env
NB_PLANETS = 18
MIN_PLANET_RAD = 8
MAX_PLANET_RAD = 64
MIN_EMPTY_SPACE = 24.
BORDER_UP=90

#game balance
INCREMENT_DURATION = 6000
RESSOURCE_DUR = 18000
FIGHT_DUR = 1400
#TELE_DUR = 500
NB_EDGES = 5

#user interface
UI_PIX_TOLERANCE = 4
TXT_B4_BARS_LEN = 18
SIZE_BARS = 42

#misc functions
def blit_center(window, surf_to_draw, y ):
    (width,height)=surf_to_draw.get_size()
    window.blit( surf_to_draw, ( (DISP_W/2)-(width/2), y)   )

def screen_simple(window, l_planets):
    window.fill(BLACK)

    #display border
    if BORDER_UP%2==0:
        pos_y_border = (BORDER_UP/2)-1
    else:
        pos_y_border = BORDER_UP/2

    pygame.draw.line( window, BLUE_GRAY,
        (0, pos_y_border), (DISP_W-1, pos_y_border ), BORDER_UP  )

    for planet in l_planets:
        planet.draw(window)
    return pos_y_border

def addmsg_line(window, txt,line=1):
    info = FontTool.draw_txt2( txt )
    tmp_pos_y = (line-1)*info.get_size()[1] + 1
    blit_center(window, info, tmp_pos_y )

gl_start_t = None
gl_score = 0
gl_final_score = None

def reset_score():
    global gl_start_t
    global gl_score
    global gl_final_score
    gl_start_t = None
    gl_score = 0
    gl_final_score = None

def generic_screen(window, gm_model):

    l_planets = gm_model.getPlanets()
    ids_r_planets = gm_model.getIdsRP()
    id_p_selected = gm_model.getIdPlayersPlanet()

    pos_y_border = screen_simple(window, l_planets)

    #case where we landed and have reachable planets
    for planet in l_planets:
        if( planet.getId()==id_p_selected ):
            planet.draw(window,True)
            pygame.draw.rect( window, RED, ( (planet.x,planet.y), (8,8))  )
            continue
        if( planet.getId() in ids_r_planets ):
            planet.draw(window,True)

    for lk in gm_model.getLinks():
        pygame.draw.line(window, LIGHT_BLUE, lk[0], lk[1] )
    #print info player
    tmp_l = gm_model.getInfo()
    for i in range(2,5):
        addmsg_line(window, tmp_l[i-2], i)

    #compute and display score
    global gl_start_t
    global gl_score
    global gl_final_score
    if(gl_start_t==None):
        gl_start_t = pygame.time.get_ticks()
    score = (pygame.time.get_ticks() - gl_start_t )/100
    if( gm_model.isGameLost() ):
        if(gl_final_score==None ):
            gl_final_score=score
        score_rect = FontTool.draw_txt2( "score: "+str(gl_final_score) )
    else:
        score_rect = FontTool.draw_txt2( "score: "+str(score) )
        
    window.blit( score_rect,  (0,530)  )


def compl(txt):
    l_spaces = [ ' ' for i in range( TXT_B4_BARS_LEN- len(txt)) ]
    spaces = ''.join(l_spaces)
    return txt+spaces
    
def det_planet_clicked(l_planets, vect_m):
    #which planet has_been clicked ?
    (mx,my)=vect_m
    for t_planet in l_planets:
        if t_planet.isClicked( mx,my):
            return t_planet.getId()
    return None


import pygame
from def_colors import *

class FontTool:
    __font_st1 = None
    __font_st2 = None
    __class_rdy = False

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def draw_txt1( txt):
        FontTool.__check_init()
        return FontTool.__font_st1.render( txt,  2, WHITE)

    @staticmethod
    def draw_txt2( txt):
        FontTool.__check_init()
        return FontTool.__font_st2.render( txt,  2, WHITE)

    @staticmethod
    def __check_init():
        if(not FontTool.__class_rdy):
            pygame.font.init()
            FontTool.__font_st1 = pygame.font.SysFont("impact", 48)
            FontTool.__font_st2 = pygame.font.SysFont("courier", 18)

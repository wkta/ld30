# -*- coding: utf8 -*-

import pygame
from global_vars import SIZE_BARS, FIGHT_DUR

class ProgressBar(object):

    def __init__(self, duration_ms= FIGHT_DUR, gets_filled=True ):
        self.paused =False

        if(duration_ms<=0):
            raise ValueError('duration_ms should be positive!')

        self.nb_units = SIZE_BARS
        self.__start_time = pygame.time.get_ticks()
        self.__end_time = self.__start_time+duration_ms
        self.__finished = False
        self.gets_filled = gets_filled
        if(gets_filled):
            self.value = 0
        else:
            self.value = SIZE_BARS

    def addDuration(self,  val):
        self.__finished = False
        now = pygame.time.get_ticks()
        if(self.__start_time +val>now):
            total_duration = self.__end_time - self.__start_time
            self.__start_time = now
            self.__end_time = now+total_duration
            return
        self.__start_time += val
        self.__end_time += val

    def pause(self):
        self.paused=True
        self.__date_pause = pygame.time.get_ticks()

    def unpause(self):
        pause_dur = pygame.time.get_ticks() - self.__date_pause
        self.__start_time += pause_dur
        self.__end_time += pause_dur
        self.paused=False

    def isFinished(self):
        return self.__finished

    def update(self):
        if(self.paused):
            return

        if(self.isFinished() ):
            return

        now = pygame.time.get_ticks()
        if(now>self.__end_time):
            self.__finished=True
            if(self.gets_filled):
                self.value = self.nb_units
            else:
                self.value = 0
            return

        total_duration = self.__end_time - self.__start_time
        if(self.gets_filled):
            time_gone = now - self.__start_time
            self.value = int( float(self.nb_units)*time_gone/total_duration)
            return
        time_remaining = self.__end_time - now
        self.value = int( float(self.nb_units)*time_remaining/total_duration)

    def getProbability(self):
        return (float(self.value)/SIZE_BARS)

    def __str__(self):
        #computes nb star equivalence
        # TODO

        #displays stars
        res = "["
        for i in xrange(0,self.value):
            res += "x"
        for i in xrange(self.value, self.nb_units):
            res += " "
        res += "]"

        return res

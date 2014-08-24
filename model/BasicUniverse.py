


class BasicUniverse(object):

    def __init__(self):
        self.__pl_list = list()
		__populate_universe( self.__pl_list)

	def getNbPlanets(self):
		return len(self.__pl_list)

	@staticmethod
	def __populate_universe( pl_list ):
        ''' populating the list of nodes+associated radii '''
        while( len(pl_list) < NB_PLANETS):
            tmp = Planet()
            # if this doesnt fit our goals, we roll dices again!
            while __is_bad_pick( tmp, pl_list):
                tmp = Planet()
            pl_list.append(tmp)

    @staticmethod
    def __is_bad_pick( t_planet, pl_list):
        if (t_planet.x+t_planet.rad>=DISP_W-1) or (t_planet.x-t_planet.rad<=0):
            return True
        if (t_planet.y+self.rad>=DISP_H-1) or (t_planet.y-self.rad<=BORDER_UP):
            return True
        for oth_planet in pl_list:
            if t_planet.overlaps( self.__overlaps(t_planet ):
                return True
        return False

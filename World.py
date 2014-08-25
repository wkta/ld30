from global_vars import *
from Planet import *
from ProgressBar import *
from SfxPlayer import  *

REWARDS = (REWARD_O2, REWARD_FOOD, REWARD_WATER) = range(3)

class World:
    '''this class models the world where the player is located'''

    @classmethod
    def __populate_universe(cls, pl_list ):
        ''' populating the list of nodes+associated radii '''
        while( len(pl_list) < NB_PLANETS):
            tmp = Planet()
            # if this doesnt fit our goals, we roll dices again!
            while cls.__is_bad_pick(tmp,pl_list):
                tmp = Planet()
            pl_list.append(tmp)

    @classmethod
    def __is_bad_pick(cls, t_planet, pl_list):
        if (t_planet.x+t_planet.rad>=DISP_W-1) or (t_planet.x-t_planet.rad<=0):
            return True
        if (t_planet.y+t_planet.rad>=DISP_H-1) or (t_planet.y-t_planet.rad<=BORDER_UP):
            return True
        for oth_planet in pl_list:
            if t_planet.overlaps( oth_planet):
                return True
        return False


    #
    #   CONSTRUCTOR ---------------------------------------------
    #
    def __init__(self):

        self.__info_o2 = None
        self.__info_food = None
        self.__info_water = None
        self.__bars_init = False
        self.paused = False
        self.__lost = False
        self.__rewards = dict()
        self.__game_exit = False;
        self.__bars_init = False
        #the player has not landed at the beginning
        self.__id_p_player = None

        self.resetLinks()

        self.__l_planets = list()
        World.__populate_universe(  self.__l_planets )


    def signalQuit(self):
        self.__game_exit = True;

    def isGameLost(self):
        return self.__lost

    def getDefeatCause(self):
        if(not self.__lost):
            raise Exception('bad usage, player did not loose yet')

        if( self.__info_o2.isFinished() ):
            return "You died of hypoxemia!"
        if( self.__info_water.isFinished() ):
            return "You died of dehydration!"
        if( self.__info_food.isFinished() ):
            return "You died of starvation!"
        

    def gameExit(self):
        return self.__game_exit

    def resetLinks(self):
        self.__assoc_id_lk = dict()
        self.__ids_reachable_planets = list()
        #there are no teleport links in the beginning
        self.__links = list()


    def produceReward(self):

        #generating
        res = None
        if( self.__id_p_player in self.__rewards ):
            res = self.__rewards[ self.__id_p_player]
        else:
            res = random.choice(REWARDS)
            self.__rewards[ self.__id_p_player ] = res

        #updating bars
        if res==None:
            raise Exception('cannot produce reward!')
        if( res==REWARD_O2):
            self.incrOxygen()
        elif( res==REWARD_FOOD):
            self.incrFood()
        elif( res==REWARD_WATER):
            self.incrAmmu()
        self.last_reward = res

    def getDescLastReward(self):
        if( self.last_reward==REWARD_O2):
            return "oxygen."
        if( self.last_reward==REWARD_FOOD):
            return "food."
        if( self.last_reward==REWARD_WATER):
            return "water."


    def getPlanets(self):
        return self.__l_planets

    def getLinks(self):
        return self.__links

    def isPaused(self):
        return self.paused


    def isPlayerHere(self, planet):
        return planet.getId()==self.__id_p_player

    def getIdPlayersPlanet(self):
        return self.__id_p_player

    #landing  / teleporting 
    def setIdPlayersPlanet(self,p_id): 
        if not (p_id in self.__ids_reachable_planets):
            self.__ids_reachable_planets.append(p_id )
        else:
            #sound
            SfxPlayer.teleport()

        found = False
        for pl in self.__l_planets:
            if pl.getId()==p_id:
                found = True
                self.current_coords = (pl.x,pl.y)
                self.__id_p_player = p_id
                break
        if(not found ):
            raise Exception('cannot set players planet to '+str(p_id) )

        #init bars if the player just landed
        if not self.__bars_init:
            self.__info_o2 = ProgressBar( RESSOURCE_DUR ,False)
            self.__info_food = ProgressBar( RESSOURCE_DUR ,False)
            self.__info_water = ProgressBar( RESSOURCE_DUR ,False)
            self.__bars_init =True

    def pause(self):
        self.__info_o2.pause() 
        self.__info_food.pause() 
        self.__info_water.pause()
        self.paused = True
 
    def unpause(self):
        self.__info_o2.unpause() 
        self.__info_food.unpause() 
        self.__info_water.unpause()
        self.paused = False
 
        


    def incrOxygen(self):
        self.__info_o2.addDuration( INCREMENT_DURATION)

    def incrFood(self):
        self.__info_food.addDuration( INCREMENT_DURATION)

    def incrAmmu(self):
        self.__info_water.addDuration( INCREMENT_DURATION)

    def update(self):
        self.__info_o2.update()
        self.__info_food.update()
        self.__info_water.update()

        # if a progress bar arrived to 0, the player lost
        if( self.__info_o2.isFinished() ):
            self.__lost = True
        if( self.__info_food.isFinished() ):
            self.__lost = True
        if( self.__info_water.isFinished() ):
            self.__lost = True

    def getInfo(self):
        res = list()
        res.append( compl("Oxygen:")+ str(self.__info_o2) )
        res.append( compl("Water:")+ str(self.__info_water) )
        res.append( compl("Food:")+ str(self.__info_food) )
        return res

    def addLink(self, lk_dest, id_p  ):
        ''' lk_dest represents a pair of coord for the dest planet'''

        tmp_lk = (self.current_coords, lk_dest) 
        if( id_p in self.__assoc_id_lk.keys() and
            tmp_lk in self.__assoc_id_lk[id_p ]  ):
            return

        if(len(self.__links) >= NB_EDGES ):
            raise Exception('max nb edges')

        #add a new edge
        try:
            self.__assoc_id_lk[ id_p ]
        except Exception:
            self.__assoc_id_lk[ id_p ]= list()
        self.__assoc_id_lk[ id_p ].append( tmp_lk)
        self.__links.append( tmp_lk )
        self.__ids_reachable_planets.append( id_p )

        #sound
        SfxPlayer.buildStuff()
    


    def hasMaxTeleporters(self):
        return (len(self.__links) >= NB_EDGES )

    def getIdsRP(self):
        return self.__ids_reachable_planets

    def getCurrentCoord(self):
        return self.current_coords

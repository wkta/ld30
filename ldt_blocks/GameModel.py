
class GameModel(object):
    def __init__(self):
        self._game_exit = False;

    def signalQuit(self):
        self._game_exit = True;

    def gameExit(self):
        return self._game_exit



class GameMode(object):

    def handle(self, events):
        raise NotImplementedError("Please Implement this method")

    def update(self, gm_model):
        raise NotImplementedError("Please Implement this method")

    def drawScreen(self, window):
        raise NotImplementedError("Please Implement this method")

    def shouldChangeMode(self):
        return False

    def getNextMode(self):
        raise NotImplementedError("Please Implement this method")

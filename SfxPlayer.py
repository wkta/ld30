import pygame

class SfxPlayer(object):
    is_started = False
    sound_lib = None

    @classmethod
    def start(cls):
        #starting music
        cls.is_started = True
        pygame.mixer.music.load('assets/loop_zik.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)

        #loading sounds
        cls.sound_lib = {
            'build' : pygame.mixer.Sound('assets/build.wav'),
            'teleport' : pygame.mixer.Sound('assets/tele.wav'),
            'fight' : pygame.mixer.Sound('assets/big_gun.wav')
            }

    @classmethod
    def stop(cls):
        pygame.mixer.music.stop()
        cls.is_started = False

    @classmethod
    def stop(cls):
        pygame.mixer.music.stop()

    @classmethod
    def buildStuff(cls):
        soundObj = cls.sound_lib['build']
        soundObj.play()

    @classmethod
    def teleport(cls):
        soundObj = cls.sound_lib['teleport']
        soundObj.play()
    
    @classmethod
    def fight(cls):
        if( not cls.is_started ):
            cls.start()

        soundObj = cls.sound_lib['fight']
        soundObj.play()

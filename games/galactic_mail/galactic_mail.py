from pyhandru.game import *
import pygame

SPR_MOON        = 'images/Moon.gif'
SPR_EXPLOSION   = 'images/Explosion.gif'
SPR_ASTEROID    = 'images/Asteroid.gif'
SPR_LANDED      = 'images/Landed.gif'
SPR_FLYING      = 'images/Flying.gif'

SND_EXPLOSION   = 'sound/Explosion.wav'
SND_BONUS       = 'sound/Bonus.wav'
BG_MUSIC        = 'sound/Music.mp3'

FPS = 30

class SndExplosion(SoundObject):
    def __init__(self):
        super().__init__(SND_EXPLOSION, is_music=False)

class SndBonus(SoundObject):
    def __init__(self):
        super().__init__(SND_BONUS, is_music=False)

class SndMusic(SoundObject):
    def __init__(self):
        super().__init__(BG_MUSIC, is_music=True)

class ObjectMoon(GameObject):
    def __init__(self):
        super().__init__(SPR_MOON)


class RoomMain(RoomObject):
    def __init__(self):
        super(RoomMain, self).__init__(None, (800, 600))


class GameGalacticMail(Game):
    def __init__(self):
        super().__init__()

        self.object_moon = ObjectMoon()
        self.snd_music = SndMusic()
        self.snd_explosion = SndExplosion()
        self.snd_ = SndExplosion()

        self.room = RoomMain()
        self.room.add(self.object_moon)
        self.snd_music.play()


def go():
    game = GameGalacticMail()
    game.loop()


if __name__ == '__main__':
    go()
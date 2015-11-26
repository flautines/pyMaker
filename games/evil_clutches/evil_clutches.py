from pyhandru import game

__author__ = 'andriu'

from pyhandru.game import *
import random

# CONSTANTES
DRAGON_IMG_PATH     = 'images/Dragon.gif'
BOSS_IMG_PATH       = 'images/Boss.gif'
FIREBALL_IMG_PATH   = 'images/Fireball.gif'
DEMON_IMG_PATH      = 'images/Demon.gif'
ROOM_IMG_PATH       = 'images/Background.bmp'
BABY_IMG_PATH       = 'images/Baby.gif'

BG_MUSICFILE        = 'sound/Music.mid'
DEMON_SOUND_PATH    = 'sound/Demon.wav'
BABY_SOUND_PATH     = 'sound/Baby.wav'

COLOR_KEY_MOB       = ( 82,  46,  41)
COLOR_KEY_DRAGON    = (  0,   0, 255)
COLOR_KEY_FIREBALL  = ( 97,  14,   8)

ROOM_DIMENSIONS = (640, 480)

PLAYER_SPEED = 16
DEMON_SPEED = 12

MOVE_UP_LEFT = (-1, -1)
MOVE_LEFT = (-1, 0)
MOVE_DOWN_LEFT = (-1, 1)

FPS = 30
ROOM_FULLSCREEN = False

CHANCE_DEMON = 50
CHANCE_BABY = 100

score = 0

#----------------------------------------------------------------------
#   CLASES ESPECIFICAS PARA ESTE JUEGO
#----------------------------------------------------------------------
class DragonObject(GameObject):
    # Constructor
    def __init__(self, image_filename):
        GameObject.__init__(self, image_filename)
        self.set_colorkey(COLOR_KEY_DRAGON)

    def on_key_down(self, key):
        """
        Actualiza el desplazamiento en Y del jugador hacia arriba o
        abajo cuando se mantiene la teclas arriba o abajo respectivamente.
        :param key: Tecla pulsada
        :return:
        """
        # abajo
        if (key == K_DOWN):
            self.despl_y = PLAYER_SPEED
        # arriba
        elif (key == K_UP):
            self.despl_y = -PLAYER_SPEED
        # disparo
        elif (key == K_SPACE):
            fireball = FireballObject(FIREBALL_IMG_PATH,
                                (self.pos_x+100, self.pos_y+10))
            self.room.add (fireball)

    def on_key_up(self, key):
        """
        Actualiza a 0 el desplazamiento del jugador en Y cuando se deja
        de pulsar arriba o abajo, haciendo que el jugador se quede quieto
        cuando no se pulsa ninguna tecla.
        :param key:
        :return:
        """
        if (key == K_DOWN or key == K_UP):
            self.despl_y = 0

    def intersect_boundary(self):
        # La nueva posición será inválida si la parte superior del sprite <= 0
        # y estamos subiendo (despl_y < 0)
        # o si por la parte inferior del sprite supera la altura de la
        # habitación y estamos bajando (despl_y > 0)
        invalid_y_pos = (
        (self.pos_y + self.despl_y <= 0 and self.despl_y <0) or
        (self.pos_y + self.height + self.despl_y > self.room.height
            and self.despl_y > 0)
        )

        if invalid_y_pos:
            self.despl_y = 0


class BossObject(GameObject):
    # Constructor
    def __init__(self, image_filename):
        GameObject.__init__(self, image_filename)
        self.set_colorkey(COLOR_KEY_MOB)
        self.pos_x = ROOM_DIMENSIONS[0] - self.width
        self.pos_y = (ROOM_DIMENSIONS[1] - self.height) //2

    def on_create(self):
        self.bg_music = BgMusic(BG_MUSICFILE)
        self.bg_music.play(-1)
        self.despl_y = -8

    def intersect_boundary(self):
        self.despl_y *= -1

    def step(self):
        # genera objetos Demon una vez cada 'CHANCE_DEMON'
        # disminuyendo 'CHANCE_DEMON' se generan más Demons por segundo
        test_chance = random.randint(1,CHANCE_DEMON)
        if test_chance == CHANCE_DEMON:
            # Demon
            self.demon = DemonObject(DEMON_IMG_PATH,(self.pos_x, self.pos_y))
            self.room.add(self.demon)

        # genera objetos Baby una vez cada 'CHANCE_BABY'
        # disminuyendo 'CHANCE_BABY' se generan más Babies por segundo
        test_chance = random.randint(1, CHANCE_BABY)
        if test_chance == CHANCE_BABY:
            # Baby
            self.baby = BabyObject(BABY_IMG_PATH, (self.pos_x, self.pos_y))
            self.room.add(self.baby)


class FireballObject(GameObject):
    # Constructor
    def __init__(self, image_filename, pos_xy):
        GameObject.__init__(self, image_filename, pos_xy)
        self.set_colorkey(COLOR_KEY_FIREBALL)

    def on_create(self):
        self.despl_x = 32

    def out_of_bounds(self):
        # Elimina este objeto del grupo al que pertenece, normalmente
        # del grupo de objetos de la Habitación
        self.kill()


class DemonObject(GameObject):
    # Constructor
    def __init__(self, image_filename, pos_xy):
        GameObject.__init__(self, image_filename, pos_xy)
        self.set_colorkey(COLOR_KEY_MOB)
        self.bound_rect.top += 40
        self.bound_rect.height -=30
        self.bound_rect.left += 40
        self.bound_rect.width -= 40
        self.sound_demon = SoundDemon()

    def on_create(self):
        direction = random.randint(0,2)
        if direction == 0:
            despl_x, despl_y = MOVE_UP_LEFT
        elif direction == 1:
            despl_x, despl_y = MOVE_LEFT
        elif direction == 2:
            despl_x, despl_y = MOVE_DOWN_LEFT
        despl_x *= DEMON_SPEED
        despl_y *= DEMON_SPEED
        self.despl_x = despl_x
        self.despl_y = despl_y

    def out_of_bounds(self):
        self.kill()
        new_demon = DemonObject(DEMON_IMG_PATH,
                                  (ROOM_DIMENSIONS[0],
                                   ROOM_DIMENSIONS[1]//2))
        self.room.add(new_demon)

    def intersect_boundary(self):
        self.despl_y = -self.despl_y

    def collision(self, sprite_colliding):
        global score

        # Demon <-> Fireball --> Destroy both and +score
        if isinstance(sprite_colliding, FireballObject):
            self.sound_demon.play()
            self.kill()
            sprite_colliding.kill()
            score += 100
            print (score)

        # Demon <-> Player --> End of Game
        if isinstance(sprite_colliding, DragonObject):
            print ('El baby dragon te tocó')
            self.room.on_close()


class BabyObject(GameObject):
    def __init__(self, image_filename, pos_xy):
        GameObject.__init__(self, image_filename, pos_xy)
        self.set_colorkey(COLOR_KEY_MOB)

        self.sound_baby = SoundBaby()

    def on_create(self):
        self.despl_x = -8

    def out_of_bounds(self):
        self.kill()

    def collision(self, sprite_colliding):
        global score
        # Baby <-> Fireball --> se destruyen ambos y -score
        if isinstance(sprite_colliding, FireballObject):
            self.sound_baby.play()

            sprite_colliding.kill()
            self.kill()
            score -= 300
            print(score)

        # Baby <-> Player --> Se destruye el Baby y +score
        if isinstance(sprite_colliding, DragonObject):
            self.kill()
            score += 500
            print(score)


class Room(RoomObject):
    # Constructor
    def __init__(self, image_filename, room_dimensions, is_fullscreen=False):
        RoomObject.__init__(
            self,
            image_filename,
            room_dimensions,
            'Evil Clutches',
            FPS,
            is_fullscreen)

        # Establece los FPS del juego
        self.frames_per_second = FPS


class BgMusic(SoundObject):
    def __init__(self, music_file_name):
        SoundObject.__init__(self,music_file_name)


class SoundDemon(SoundObject):
    def __init__(self):
        # Inicializa como efecto sonoro
        super().__init__(DEMON_SOUND_PATH, False)


class SoundBaby(SoundObject):
    def __init__(self):
        super().__init__(BABY_SOUND_PATH, False)

class GameEvilClutches(Game):
    def __init__(self, fps=FPS):
        super().__init__(fps=FPS)

        # Create Room
        self.room = Room(ROOM_IMG_PATH, ROOM_DIMENSIONS, ROOM_FULLSCREEN)

        # Create Player
        self.dragon = DragonObject(DRAGON_IMG_PATH)

        # Create Boss
        self.boss = BossObject(BOSS_IMG_PATH)

        # Añade los objetos a la Room
        self.room.add(self.dragon)
        self.room.add(self.boss)


def main():
    game = GameEvilClutches()
    game.loop()

if __name__ == '__main__':
    main()


__author__ = 'andriu'


import pygame, random, sys
from pygame.locals import *

COLLISION_VISIBLE = False
DEFAULT_FPS = 60

class GameObject(pygame.sprite.Sprite):

    # Constructor.
    def __init__(self, img_path, pos_xy=(0, 0)):

        """
        Inicializa un objeto de juego, carga la imagen especificada
        para el sprite y actualiza las dimensiones del sprite segun el
        tamaño de la imagen. Opcionalmente puede pasarse una tupla con
        la posición inicial que tendrá el objeto en el juego al ser creado.

        :type img_path: String
        :param img_path: Ruta de la imagen a cargar para
        el sprite
        
        :type pos_xy: Tupla de dos elementos
        :param pos_xy: Posición X,Y inicial del objeto
        """
        # Llama al constructor padre
        pygame.sprite.Sprite.__init__(self)

        # Carga la imagen y la asigna al sprite
        self.image = pygame.image.load(img_path)

        # Asigna el 'Rect' con las dimensiones de la imagen
        # Actualiza tambien la posicion del objeto al asignar los valores
        # correspondientes a rect.x y rect.y
        self.rect = self.image.get_rect()

        # Suma la posición inicial si es que se ha especificado
        pos_inicial_x, pos_inicial_y = pos_xy
        self.rect.x += pos_inicial_x
        self.rect.y += pos_inicial_y

        # Desplazamientos en X,Y del objeto, se usan para actualizar la
        # posición del objeto.
        self.despl_x, self.despl_y = (0, 0)

        # Usamos un 'bound_rect' para comprobación de colisiones propio
        # independiente del sprite.rect de pygame. De esta forma
        # podemos modificar la forma del 'bound_rect' de colisiones sin
        # alterar el posicionado del sprite.
        # GameObject actualiza automáticamente y de forma correcta el
        # posicionado del 'bound_rect' cuando sus coordenadas x,y
        # cambian.
        #
        # Por defecto se asigna a una copia del sprite.rect actual.

        self.bound_rect = self.rect.copy()

        # Ejecuta el método 'on_create'
        self.on_create()

    @ property
    def pos_x (self):
        """
        Obtiene el valor actual de la coordenada X del sprite

        :return: Valor actual de la coordenada X
        """
        return self.rect.x

    @ pos_x.setter
    def pos_x (self, x):
        """
        Asigna valor a la coordenada X del sprite. Actualiza de forma
        correcta el bound_rect que envuelve al sprite.

        :param x: Nueva coordenada X

        """
        diff = self.bound_rect.left - self.rect.left
        self.rect.x = x
        self.bound_rect.x = self.rect.x + diff

    @ property
    def pos_y (self):
        """
        Obtiene el valor actual de la coordenada Y del sprite
        :return: Valor actual de la coordenada Y
        """
        return self.rect.y

    @ pos_y.setter
    def pos_y (self, y):
        """
        Asigna valor a la coordenada Y del sprite. Actualiza de forma
        correcta el 'bound_rect' que envuelve al sprite.

        :param y: Nueva coordenada Y

        """
        diff = self.bound_rect.top - self.rect.top
        self.rect.y = y
        self.bound_rect.y = self.rect.y + diff

    @ property
    def width (self):
        """
        Obtiene el ancho del sprite asociado al objeto
        :return: Ancho del sprite
        """
        return self.image.get_width()

    @ property
    def height (self):
        """
        Obtiene la altura del sprite asociado al objeto
        :return: Altura del sprite
        """
        return self.image.get_height()

    def set_colorkey (self, color_key):
        """
        Establece el color_key (color usado como transparencia)

        :param color_key: Tupla en formato (R, G, B)
        """
        self.image.set_colorkey (color_key)

    def draw(self, canvas, draw_rect=False):
        """
        Transfiere la imagen correspondiente al sprite a la superficie
        de trabajo.

        :param canvas: Superficie de trabajo donde copiar la imagen

        """
        canvas.blit(self.image, self.rect)
        if draw_rect:
            pygame.draw.rect(canvas, (255,255,255), self.bound_rect, 2)

    def procesa_evento (self, evento):
        """
        Procesa los eventos asociados al objeto llamando a la función
        on_xxxx correspondiente al evento.
        :param evento: Evento a procesar
        :return:
        """
        # KEYDOWN
        if evento.type == KEYDOWN:
            self.on_key_down (evento.key)
        # KEYUP
        if evento.type == KEYUP:
            self.on_key_up (evento.key)

    def update (self, width, height):
        """
        Actualiza el estado del objeto: cambios de posición, etc.
        También comprueba si el objeto toca los límites de la habitación
        donde está y si está fuera de los límites. En caso que se produzca
        algunas de estas situaciones ejecuta los eventos 'intersect_boundary'
        o 'out_of_bounds' respectivamente'
        :return:
        """

        # Comprueba si el objeto tocará los bordes de la habitación
        if (self.pos_x + self.despl_x >= width
            or self.pos_x + self.despl_x <= 0
            or self.pos_y+self.height + self.despl_y >= height
            or self.pos_y + self.despl_y <= 0):
            # Si es así, ejecuta el evento 'intersect_boundary'
            self.intersect_boundary()

        self.pos_x += self.despl_x
        self.pos_y += self.despl_y

        # Comprueba si el objeto está fuera de las dimensiones de la
        # habitación
        if (self.pos_x >= width or self.pos_x <= 0 or
            self.pos_y >= height or self.pos_y <= 0):
            # Si es así, ejecuta el evento 'out_of_bounds'
            self.out_of_bounds()

    def check_for_collisions(self):
        for sprite2 in self.room.objetos_de_juego:
            if (self != sprite2):
                self.check_for_collision (sprite2)

    def check_for_collision (self, sprite2):
        #if pygame.sprite.collide_rect(self, sprite2):
        # Utiliza pygame.Rect.colliderect entre dos pygame.Rect para
        # comprobar colisión entre dos sprites

        if self.bound_rect.colliderect(sprite2.bound_rect):
            self.collision(sprite2)

    def step(self):
        """
        Step() se ejecuta despues de procesar eventos pero antes de actualizar
        el estado de los objetos de juego.
        :return:
        """
        pass
    # -------------------------------------------------------------------
    # Metodos equivalentes a los objetos en GameMaker
    # -------------------------------------------------------------------

    #
    # Eventos a los que responden los objetos. Por defecto están vacíos
    # y es responsabilidad de las subclases proporcionar la funcionalidad
    # requerida para cada evento.
    #
    # on_create
    def on_create(self):
        """
        Evento que se ejecuta nada más crear el objeto. Este método es invocado
        justo al final de self.__init__ con lo que se garantiza que el objeto
        ya está inicializado en este punto.

        :return:
        """
        pass

    # intersect_boundary
    def intersect_boundary(self):
        """
        Este evento se ejecuta cuando la nueva posición del objeto al sumar
        su desplazamiento toca alguno de los bordes de la habitación.

        :return:
        """
        pass
    # out_of_bounds
    def out_of_bounds(self):
        """
        Este evento se ejecuta cuando una de las coordenadas x o y del objeto
        caen fuera de los límites de la habitación, indicando que el objeto
        ha salido del área visible del juego.
        :return:
        """
        pass

    # collision
    def collision(self, sprite_colliding):
        pass

    # on_key_down
    def on_key_down(self, key):
        pass

    # on_key_up
    def on_key_up(self, key):
        pass


class RoomObject():
    def __init__(
            self,
            img_path,
            dimensions,
            title='New Room',
            room_fps=DEFAULT_FPS,
            is_fullscreen=False,
            hw_surface=False):
        """
            Inicializa una habitación con las dimensiones y el fondo de
        pantalla indicados. Opcionalmente se puede especificar si se quiere
        mostrar a pantalla completa o en ventana, y si se desea una superficie
        con aceleración hardware

        :param img_path: Ruta completa del fichero imagen para el fondo de pantalla
        :type img_path: string

        :param dimensions: Ancho y alto de pantalla en formato tupla
        :type dimensions: Tuple

        :param title: Título de la ventana
        :type title: str

        :param room_fps: Fotogramas por segundo para ésta habitación, normalmente
        los mismos que para todo el juego
        :type room_fps: int

        :param hw_surface: Si se desea crear una superficie en hardware
        :type hw_surface: bool

        :param is_fullscreen: True para crear la habitación a pantalla completa
        , False para crearla en ventana
        :type is_fullscreen: bool

        :return: None
        """
        # Flags para la creación de la ventana
        self.display_flags = (HWSURFACE | DOUBLEBUF) if hw_surface else 0

        # Actualizar los flags según se desee crear una ventana
        # a pantalla completa
        self.is_fullscreen = is_fullscreen
        self.display_flags |= pygame.FULLSCREEN if self.is_fullscreen else 0

        # Crea la superficie de trabajo con los flags indicados
        self.canvas = pygame.display.set_mode (dimensions, self.display_flags)

        self.title = title
        # Establece el título
        pygame.display.set_caption (self.title)

        # Objetos en la Room
        self.objetos_de_juego = pygame.sprite.Group()

        if img_path is not None:
        # Imagen de fondo
            self.image_background = pygame.image.load (img_path).convert()
        else:
            self.image_background = pygame.Surface(dimensions)
            self.image_background.fill((20, 50, 210))

        # Dimensiones de la Room
        self.width, self.height = dimensions

        # Reloj para el control de FPS
        self.clock = pygame.time.Clock()

        # Fotogramas por segundo, por defecto 60
        self.frames_per_second = room_fps


    def blit (self):
        """
        Dibuja todos los elementos de juego
        :return:
        """
        # Primero dibuja el fondo
        self.canvas.blit (self.image_background, (0,0))

        # Ahora dibuja todos los objetos de la habitación
        # llamando al metodo 'blit' de cada objeto
        for objeto_de_juego in self.objetos_de_juego:
            objeto_de_juego.draw(self.canvas, COLLISION_VISIBLE)

        # Y finalmente muestra la superficie de trabajo
        pygame.display.flip()

    def add (self, objeto_de_juego):
        """
        Añade un elemento a la lista 'objetos_de_juego'
        :param objeto_de_juego: Objeto de juego a añadir
        :return:
        """
        assert self is not None, "No hay ninguna habitación creada"
        # Convierte la imagen del sprite al formato de pantalla para
        # acelerar las operaciones de blit.
        objeto_de_juego.image.convert()
        # Añade el objeto a la lista de objetos en la habitación actual
        self.objetos_de_juego.add (objeto_de_juego)
        # y añade una referencia a la habitación actual al objeto de juego
        # para así poder referenciar la habitación desde éste.
        objeto_de_juego.room = self

    def procesa_eventos (self):
        """
        Procesa los eventos del juego. Llama a cada objeto de
        la habitación para que procese los eventos que les corresponda.
        :return:
        """
        for evento in pygame.event.get():
            if (evento.type == QUIT or
                    (evento.type == KEYDOWN and
                     evento.key == K_ESCAPE)):
                self.on_close ()

            for objeto_de_juego in self.objetos_de_juego:
                objeto_de_juego.procesa_evento (evento)

    def actualiza_estado (self):
        """
        Actualiza el estado de todos los objetos pidiendo a cada objeto
        que actualice su estado.
        :return:
        """
        self.check_for_collisions()
        self.objetos_de_juego.update(self.width, self.height)

    def check_for_collisions(self):
        # Comprueba colisiones entre sprites dentro del grupo
        for object_sprite in self.objetos_de_juego:
            object_sprite.check_for_collisions()

    def loop(self):
        while True:
            # Procesa los eventos
            self.procesa_eventos()

            # Llama al metodo step
            self.step()

            # Actualiza el estado del juego
            self.actualiza_estado()

            # Muestra el contenido del juego por pantalla
            self.blit()

            self.clock.tick (self.frames_per_second)

    def step(self):
        """
        Step() se ejecuta despues de procesar eventos pero antes de actualizar
        el estado de los objetos de juego.
        :return:
        """
        for objeto_dejuego in self.objetos_de_juego:
            objeto_dejuego.step()

    #
    # Eventos a los que reacciona una Habitación
    #
    # on_close
    def on_close (self):
        """
        Evento por defecto cuando se pulsa el botón salir de la ventana.
        Cierra la aplicación y sale al sistema con código de error 0.
        :return:
        """
        pygame.mixer.quit()
        pygame.quit()
        sys.exit(0)


class SoundObject():
    def __init__(self, file_name, is_music=True):
        """
        SoundObject sirve tanto para música de fondo como para efectos
        sonoros. Si
            is_music = True

        el objeto se usará para controlar la música de fondo. Si
            is_music = False

        el objeto controlará efectos sonoros.

        :param file_name: Nombre completo del archivo a usar para el sonido
        :param is_music: True, crea un objeto para música de fondo, False
        para crear un objeto de efectos de sonido.
        :return: Nada
        """
        self.is_music = is_music
        self.__objeto_sonido = None

        #pygame.mix
        if is_music:
            # Load a mixer.music file
            pygame.mixer.music.load(file_name)

        else:
            # Load a mixer.sound file
            self.__objeto_sonido = pygame.mixer.Sound(file_name)
            self.__objeto_sonido.set_volume(0.5)

    def play(self, loop=0):
        if self.is_music:
            pygame.mixer.music.play(loop)
        else:
            assert self.__objeto_sonido is not None
            self.__objeto_sonido.play(loop)


class Game():
    def __init__(self, fps=60):
        """
        Inicializa PyGame y el mixer, random, etc.

        """
        # mixer.pre_init soluciona los problemas de lag que tenía con los
        # efectos sonoros.
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        random.seed()

        self.game_fps = fps
        self.room = None


    def loop(self):
        '''
        Bucle principal del juego, llama al bucle de la habitación.
        :return:
        '''
        assert self.room is not None, "No hay ninguna habitación creada"
        self.room.loop()
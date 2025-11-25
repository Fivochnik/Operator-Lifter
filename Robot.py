from ForGame import *
import os
import inspect
import time

#Константы:
#Константа доступа:
_ROBOT_INFO_CAN_BE_CHANGED = False

# Получаем путь к вызывающему модулю
caller_frame = inspect.stack()[1]
caller_filename = caller_frame.filename
caller_dir = os.path.basename(os.path.dirname(os.path.abspath(caller_filename)))

if os.path.exists('settings.py'):
    from settings import *
else:
    #Константы отображения:
    FPS = 60
    WIDTH, HEIGHT = 1200, 600
    ZOOM = 8
    PERIOD = 0.5
    with open('settings.py', 'wt', -1, 'utf-8') as f:
        f.write('#Константы отображения:\n' +
                f'{FPS = }\n' +
                f'{WIDTH, HEIGHT = }\n' +
                f'{ZOOM = }\n' +
                f'{PERIOD = }')
WIDTH_HALF = WIDTH >> 1
HEIGHT_HALF = HEIGHT >> 1

if caller_dir == 'levels':
    _ROBOT_INFO_CAN_BE_CHANGED = True

    
    #Окно приложения:
    screen = newScreen(width = WIDTH,
                       height = HEIGHT,
                       name = 'Оператор Грузчик',
                       img = '..\\images\\icon.png',
                       resizable = True)

    #Спрайты:
    spritesheet = game.image.load('..\\images\\sprites.png').convert_alpha()
    robot_list = [f'robot{i}{i}' for i in range(3)] + 'robot01 robot02 robot12'.split(' ') #- анимация гусениц робота
    platform_list = [f'platform|{p}' for p in ('iron stone box fragile damaged'.split(' ') + [f'conveyor{w}' for w in range(4)])] #- платформы
    pit_list = 'abyss pit'.split(' ') #- ямы
    object_list = [f'object|{o}' for o in ('wall stone box fragile damaged'.split(' ') + [f'factory|{t}' for t in 'robot box fragile'.split(' ')])] #- объекты
    zone_list = [f'zone|{"box" if i % 4 < 2 else "fragile"}|{True if i % 2 else False}' for i in range(4)] #- зоны доставки ящиков
    sprite = {}
    for i, List in enumerate([robot_list, platform_list, pit_list, object_list, zone_list]):
        y = i * 16
        for j, name in enumerate(List):
            x = j * 16
            sp = game.Surface((16, 16), game.SRCALPHA)
            sp.blit(spritesheet, (0, 0), (x, y, 16, 16))
            sprite[name] = sp
    for sp_name in robot_list[3 :]:
        sprite[f'{sp_name}|top'] = sprite[sp_name]
        fl_name = sp_name[: -2] + sp_name[-2 :][::-1]
        sprite[f'{fl_name}'] = sprite[f'{fl_name}|top'] = game.transform.flip(sprite[sp_name], True, False)
        for rot, way in [(270, 'right'), (180, 'bottom'), (90, 'left')]:
            sprite[f'{sp_name}|{way}'] = game.transform.rotate(sprite[sp_name], rot)
            sprite[f'{fl_name}|{way}'] = game.transform.rotate(sprite[fl_name], rot)
    for sp_name in robot_list[: 3] + platform_list[5 :] + object_list[5 :]:
        sprite[f'{sp_name}|top'] = sprite[sp_name]
        for rot, way in [(270, 'right'), (180, 'bottom'), (90, 'left')]:
            sprite[f'{sp_name}|{way}'] = game.transform.rotate(sprite[sp_name], rot)
    REDRAW_ALL = True

#Константы направления:
LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

#Константы платформ:
IRON = P_I = ЖЕЛЕЗО = П_Ж = 0
STONE = P_S = КАМЕНЬ = П_К = 1
BOX = P_B = ЯЩИК = П_Я = 2
FRAGILE_BOX = P_F = ХРУПКИЙ_ЯЩИК = П_Х = 3
DAMAGED_BOX = P_D = ПОВРЕЖДЁННЫЙ_ЯЩИК = П_П = 4
CONVEYOR_TO_THE_LEFT = P_CL = КОНВЕЕР_ВЛЕВО = П_К_Л = 5
CONVEYOR_TO_THE_RIGHT = P_CR = КОНВЕЕР_ВПРАВО = П_К_П = 6
CONVEYOR_TO_THE_TOP = P_CT = КОНВЕЕР_ВВЕРХ = П_К_В = 7
CONVEYOR_TO_THE_BOTTOM = P_CB = КОНВЕЕР_ВНИЗ = П_К_Н = 8
ABYSS = P_A = БЕЗДНА = Я_Б = 9
PIT = P_P = ЯМА = Я_Я = 10

#Константы объектов:
WALL = O_W = СТЕНА = О_С = 0
STONE = O_S = КАМЕНЬ = О_К = 1
BOX = O_B = ЯЩИК = О_Я = 2
FRAGILE_BOX = O_F = ХРУПКИЙ_ЯЩИК = О_Х = 3
DAMAGED_BOX = O_D = ПОВРЕЖДЁННЫЙ_ЯЩИК = О_П = 4
ROBOT_FACTORY_TO_THE_LEFT = O_RFL = ФАБРИКА_РОБОТОВ_ВЛЕВО = О_Ф_Р_Л = 5
ROBOT_FACTORY_TO_THE_RIGHT = O_RFR = ФАБРИКА_РОБОТОВ_ВПРАВО = О_Ф_Р_П = 6
ROBOT_FACTORY_TO_THE_TOP = O_RFT = ФАБРИКА_РОБОТОВ_ВВЕРХ = О_Ф_Р_В = 7
ROBOT_FACTORY_TO_THE_BOTTOM = O_RFB = ФАБРИКА_РОБОТОВ_ВНИЗ = О_Ф_Р_Н = 8
BOX_FACTORY_TO_THE_LEFT = O_BFL = ФАБРИКА_ЯЩИКОВ_ВЛЕВО = О_Я_Р_Л = 9
BOX_FACTORY_TO_THE_RIGHT = O_BFR = ФАБРИКА_ЯЩИКОВ_ВПРАВО = О_Я_Р_П = 10
BOX_FACTORY_TO_THE_TOP = O_BFT = ФАБРИКА_ЯЩИКОВ_ВВЕРХ = О_Я_Р_В = 11
BOX_FACTORY_TO_THE_BOTTOM = O_BFB = ФАБРИКА_ЯЩИКОВ_ВНИЗ = О_Я_Р_Н = 12
FRAGILE_BOX_FACTORY_TO_THE_LEFT = O_FFL = ФАБРИКА_ПОВРЕЖДЁННЫХ_ЯЩИКОВ_ВЛЕВО = О_П_Р_Л = 13
FRAGILE_BOX_FACTORY_TO_THE_RIGHT = O_FFR = ФАБРИКА_ПОВРЕЖДЁННЫХ_ЯЩИКОВ_ВПРАВО = О_П_Р_П = 14
FRAGILE_BOX_FACTORY_TO_THE_TOP = O_FFT = ФАБРИКА_ПОВРЕЖДЁННЫХ_ЯЩИКОВ_ВВЕРХ = О_П_Р_В = 15
FRAGILE_BOX_FACTORY_TO_THE_BOTTOM = O_FFB = ФАБРИКА_ПОВРЕЖДЁННЫХ_ЯЩИКОВ_ВНИЗ = О_П_Р_Н = 16
NOTHING = O_N = НИЧЕГО = О_НИЧЕГО = 17

#Константы зон:
EMPTY_ZONE = Z_E = ПУСТАЯ_ЗОНА = З_П = 0
BOX_ZONE = Z_B = ЗОНА_ЯЩИКА = З_Я = 1
FRAGILE_BOX_ZONE = Z_F = ЗОНА_ХРУПКОГО_ЯЩИКА = З_Х = 2

#Глобальные переменные:
Floor = Object = Zone = 0

#Классы исключений:
class PlacementError(Exception):
    """Ошибка размещения объетов в уровне."""

    def __init__(self, msg: str):
        self.message = msg

#Класс робота:
class Robot:
    """Робот-грузчик."""

    def __init__(self,
                 x: int,
                 y: int,
                 way: int = LEFT):
        self.__x = x
        self.__y = y
        self.__way = way
        self.is_alive = True

    @property
    def x(self):
        """Возвращает координату "x" положения робота."""
        if _ROBOT_INFO_CAN_BE_CHANGED:
            return self.__x

    @x.setter
    def x(self, value: int):
        """Устанавливает координату "x" положения робота."""
        if _ROBOT_INFO_CAN_BE_CHANGED:
            self.__x = value

    @property
    def y(self):
        """Возвращает координату "y" положения робота."""
        if _ROBOT_INFO_CAN_BE_CHANGED:
            return self.__y

    @y.setter
    def y(self, value: int):
        """Устанавливает координату "y" положения робота."""
        if _ROBOT_INFO_CAN_BE_CHANGED:
            self.__y = value

    @property
    def way(self):
        """Возвращает направление робота."""
        if _ROBOT_INFO_CAN_BE_CHANGED:
            return self.__way

    @way.setter
    def way(self, value: int):
        """Устанавливает направление робота."""
        if _ROBOT_INFO_CAN_BE_CHANGED:
            self.__way = value

    def forward(self):
        """Передаёт команду роботу двигаться вперёд. На выполнение этой команды робот тратит ход!"""
        send_msg('forward')

    def left(self):
        """Передаёт команду роботу поворачиваться влево. На выполнение этой команды робот не тратит ход!"""
        send_msg('left')

    def right(self):
        """Передаёт команду роботу поворачиваться вправо. На выполнение этой команды робот не тратит ход!"""
        send_msg('right')

    def check(self):
        """Передаёт команду роботу проверить. На выполнение этой команды робот не тратит ход!"""
        global Floor, Object, Zone
        send_msg('check')
        Floor, Object, Zone = (int(x) for x in get_msg('..\\info.msg').split(' '))

    def kick(self):
        """Передаёт команду роботу толкнуть. На выполнение этой команды робот не тратит ход!"""
        send_msg('kick')

    def __repr__(self):
        return f'Robot(x = {self.__x}, y = {self.__y}, way = {"LEFT RIGHT TOP BOTTOM".split(" ")[self.__way]})'

    def __str__(self):
        return self.__repr__()

class __CAMERA:
    """Камера."""

    def __init__(self, x: int, y: int, zoom: int = 1):
        self.x = x
        self.y = y
        self.zoom = zoom

    def apply(self, rect: game.Rect):
        """Возвращает прямоугольник, как он будет виден на экране через камеру."""
        if type(rect) is game.Rect:
            return game.Rect((rect.x - self.x) * self.zoom + WIDTH_HALF,
                             (rect.y - self.y) * self.zoom + HEIGHT_HALF,
                             rect.width * self.zoom,
                             rect.height * self.zoom)
        if type(rect) is tuple and \
           len(rect) == 2 and \
           type(rect[0]) is int and \
           type(rect[1]) is int:
            return (rect.x - self.x) * self.zoom + WIDTH_HALF, (rect.y - self.y) * self.zoom + HEIGHT_HALF

def robot_forward():
    """Передаёт команду роботу двигаться вперёд. На выполнение этой команды робот тратит ход!"""
    send_msg('forward')

def robot_left():
    """Передаёт команду роботу поворачиваться влево. На выполнение этой команды робот не тратит ход!"""
    send_msg('left')

def robot_right():
    """Передаёт команду роботу поворачиваться вправо. На выполнение этой команды робот не тратит ход!"""
    send_msg('right')

def robot_check():
    """Передаёт команду роботу проверить. На выполнение этой команды робот не тратит ход!"""
    global Floor, Object, Zone
    send_msg('check')
    Floor, Object, Zone = (int(x) for x in get_msg('..\\info.msg').split(' '))

def robot_kick():
    """Передаёт команду роботу толкнуть. На выполнение этой команды робот не тратит ход!"""
    send_msg('kick')

def send_msg(msg: str, path: str = '..\\msg.msg') -> bool:
    """Отправляет сообщение."""
    if not os.path.exists(path):
        with open(path, 'wt', -1, 'utf-8') as f:
            f.write(msg)
    else:
        while True:
            with open(path, 'rt', -1, 'utf-8') as f:
                s = f.read()
            if s == '':
                with open(path, 'wt', -1, 'utf-8') as f:
                    f.write(msg)
                break
    return True

def get_msg(path: str = '..\\msg.msg', now: bool = False) -> str:
    """Получает сообщение."""
    if not os.path.exists(path):
        with open(path, 'wt', -1, 'utf-8') as f:
            pass
    while True:
        with open(path, 'rt', -1, 'utf-8') as f:
            s = f.read()
        if s != '':
            with open(path, 'wt', -1, 'utf-8'):
                pass
            return s
        elif now:
            return None

def try_forward(robot, objects) -> bool:
    """Робот пробует переместиться вперёд. Тратит ход."""
    if robot.way == LEFT:
        pos = robot.x - 1, robot.y
        n_pos = robot.x - 2, robot.y
    elif robot.way == RIGHT:
        pos = robot.x + 1, robot.y
        n_pos = robot.x + 2, robot.y
    elif robot.way == TOP:
        pos = robot.x, robot.y - 1
        n_pos = robot.x, robot.y - 2
    elif robot.way == BOTTOM:
        pos = robot.x, robot.y + 1
        n_pos = robot.x, robot.y + 2
    obj = objects.get(pos, NOTHING)
    if obj in {WALL, O_RFL, O_RFR, O_RFT, O_RFB, O_BFL, O_BFR, O_BFT, O_BFB, O_FFL, O_FFR, O_FFT, O_FFB}:
        return False
    if obj == NOTHING:
        robot.x, robot.y = pos
    elif objects.get(n_pos, NOTHING) == NOTHING:
        robot.x, robot.y = pos
        objects[n_pos] = objects[pos]
        del objects[pos]
    else:
        return False
    return True

def rotate_left(robot):
    """Робот поворачивается влево."""
    if robot.way == LEFT:
        robot.way = BOTTOM
    elif robot.way == RIGHT:
        robot.way = TOP
    elif robot.way == TOP:
        robot.way = LEFT
    elif robot.way == BOTTOM:
        robot.way = RIGHT

def rotate_right(robot):
    """Робот поворачивается вправо."""
    if robot.way == LEFT:
        robot.way = TOP
    elif robot.way == RIGHT:
        robot.way = BOTTOM
    elif robot.way == TOP:
        robot.way = RIGHT
    elif robot.way == BOTTOM:
        robot.way = LEFT

def check(robot, platforms, objects, zones):
    """Робот проверяет клетку перед собой."""
    if robot.way == LEFT:
        pos = robot.x - 1, robot.y
    elif robot.way == RIGHT:
        pos = robot.x + 1, robot.y
    elif robot.way == TOP:
        pos = robot.x, robot.y - 1
    elif robot.way == BOTTOM:
        pos = robot.x, robot.y + 1
    send_msg(f'{platforms.get(pos, ABYSS)} {objects.get(pos, NOTHING)} {zones.get(pos, EMPTY_ZONE)}', '..\\info.msg')

def try_kick(robot, objects) -> bool:
    """Робот пробует толкнуть вперёд. Тратит ход."""
    if robot.way == LEFT:
        pos = robot.x - 1, robot.y
        n_pos = robot.x - 2, robot.y
    elif robot.way == RIGHT:
        pos = robot.x + 1, robot.y
        n_pos = robot.x + 2, robot.y
    elif robot.way == TOP:
        pos = robot.x, robot.y - 1
        n_pos = robot.x, robot.y - 2
    elif robot.way == BOTTOM:
        pos = robot.x, robot.y + 1
        n_pos = robot.x, robot.y + 2
    obj = objects.get(pos, NOTHING)
    if obj in {WALL, O_RFL, O_RFR, O_RFT, O_RFB, O_BFL, O_BFR, O_BFT, O_BFB, O_FFL, O_FFR, O_FFT, O_FFB}:
        return False
    if obj != NOTHING:
        if objects.get(n_pos, NOTHING) == NOTHING:
            objects[n_pos] = objects[pos]
            del objects[pos]
        else:
            return False
    return True

def act_is_ended(pos, platforms, objects, robot = None, objs_for_act = None) -> bool:
    """Объект в клетке "pos" или робот "pos" совершает действие по законам мира."""
    if objs_for_act is None:
        objs_for_act = set()
    if type(pos) is Robot:
        robot = pos
        pos = robot.x, robot.y
        plt = platforms.get(pos, ABYSS)
        if plt in {PIT, ABYSS}:
            robot.is_alive = False
        elif plt == FRAGILE_BOX:
            platforms[pos] = DAMAGED_BOX
        elif plt == DAMAGED_BOX:
            del platforms[pos]
            robot.is_alive = False
        elif plt in {P_CL, P_CR, P_CT, P_CB}:
            if plt == P_CL:
                n_pos = pos[0] - 1, pos[1]
            elif plt == P_CR:
                n_pos = pos[0] + 1, pos[1]
            elif plt == P_CT:
                n_pos = pos[0], pos[1] - 1
            elif plt == P_CB:
                n_pos = pos[0], pos[1] + 1
            if objects.get(n_pos, NOTHING) == NOTHING:
                robot.x, robot.y = n_pos
                plt = platforms.get(n_pos, ABYSS)
                if plt == FRAGILE_BOX:
                    platform[n_pos] = DAMAGED_BOX
                elif plt == DAMAGED_BOX:
                    del platforms[n_pos]
                    robot.is_alive = False
                elif plt in {PIT, ABYSS}:
                    robot.is_alive = False
            else:
                return False
        return True
    obj = objects.get(pos, NOTHING)
    plt = platforms.get(pos, ABYSS)
    if obj in {O_S, O_B, O_F, O_D}:
        if plt == P_F:
            platforms[pos] = P_D
            objs_for_act.remove(pos)
        elif plt in {P_D, PIT}:
            platforms[pos] = obj
            del objects[pos]
            objs_for_act.remove(pos)
        elif plt == ABYSS:
            del objects[pos]
            objs_for_act.remove(pos)
        elif plt in {P_CL, P_CR, P_CT, P_CB}:
            if plt == P_CL:
                n_pos = pos[0] - 1, pos[1]
            elif plt == P_CR:
                n_pos = pos[0] + 1, pos[1]
            elif plt == P_CT:
                n_pos = pos[0], pos[1] - 1
            elif plt == P_CB:
                n_pos = pos[0], pos[1] + 1
            if not robot is None and n_pos == (robot.x, robot.y):
                objs_for_act.remove(pos)
                return False
            n_obj = objects.get(n_pos, NOTHING)
            if n_obj == NOTHING:
                objects[n_pos] = obj
                del objects[pos]
                objs_for_act.remove(pos)
                return True
            elif n_pos not in objs_for_act:
                objs_for_act.remove(pos)
            return False
        else:
            objs_for_act.remove(pos)
    elif obj in {O_RFL, O_RFR, O_RFT, O_RFB,
                 O_BFL, O_BFR, O_BFT, O_BFB,
                 O_FFL, O_FFR, O_FFT, O_FFB}:
        if obj in {O_RFL, O_RFR, O_RFT, O_RFB}:
            goods = NOTHING
        elif obj in {O_BFL, O_BFR, O_BFT, O_BFB}:
            goods = BOX
        elif obj in {O_FFL, O_FFR, O_FFT, O_FFB}:
            goods = O_F
        if obj in {O_RFL, O_BFL, O_FFL}:
            n_pos = pos[0] - 1, pos[1]
        elif obj in {O_RFR, O_BFR, O_FFR}:
            n_pos = pos[0] + 1, pos[1]
        elif obj in {O_RFT, O_BFT, O_FFT}:
            n_pos = pos[0], pos[1] - 1
        elif obj in {O_RFB, O_BFB, O_FFB}:
            n_pos = pos[0], pos[1] + 1
        if not robot is None and n_pos == (robot.x, robot.y):
            objs_for_act.remove(pos)
            return False
        n_obj = objects.get(n_pos, NOTHING)
        if n_obj == NOTHING:
            objects[n_pos] = goods
            objs_for_act.remove(pos)
            return True
        elif n_pos not in objs_for_act:
            objs_for_act.remove(pos)
        return False
    return True

def rect_intersection(rect1: game.Rect, rect2: game.Rect) -> 'None|pygame.Rect':
    """Возвращает пересечение двух прямоугольников, если оно есть. Иначе - None."""
    if rect1.colliderect(rect2):
        return rect1.clip(rect2)
    return None

def my_blit(main_surf: game.Surface, blit_surf: game.Surface, pos: tuple, rect: game.Rect):
    """
    Рисует видимую часть уровня с автоматическим масштабированием.
    
    Args:
        main_surf: Целевая поверхность (экран)
        blit_surf: Поверхность уровня
        pos: Глобальные координаты topleft уровня
        rect: Видимая область камеры (глобальные координаты)
    """
    # 1. Находим видимую область уровня
    blit_rect = blit_surf.get_rect(topleft=pos)
    inter = rect_intersection(rect, blit_rect)
    if inter is None:
        return
    
    # 2. Создаем поверхность камеры (оригинальный масштаб)
    camera_surf = game.Surface(rect.size, game.SRCALPHA)
    
    # 3. Переносим видимую часть на камеру
    src_rect = inter.move(-pos[0], -pos[1])
    blit_pos = (max(inter.x - rect.x, 0), max(inter.y - rect.y, 0))
    camera_surf.blit(blit_surf.subsurface(src_rect), blit_pos)
    
    # 4. Масштабируем под размер экрана
    scaled_camera = game.transform.scale(camera_surf, main_surf.get_size())
    
    # 5. Отрисовка на экран
    main_surf.blit(scaled_camera, (0, 0))

#Функции обработки:
def before_redraw():
    """Выполнение программы до перерисовки."""
    pass

def after_redraw():
    """Выполнение программы после перерисовки."""
    pass

def before_robot_step():
    """Выполнение программы до шага робота."""
    pass

def after_robot_step():
    """Выполнение программы после шага робота."""
    pass

def before_physics():
    """Выполнение программы до расчётов физики."""
    pass

def after_physics():
    """Выполнение программы после расчётов физики."""
    pass

def level_run(platforms: {(int, int): int},
              objects: {(int, int): int},
              zones: {(int, int): int},
              robot: Robot,
              ignore_PlacementError: bool = False):
    """Запускает уровень."""
    global WIDTH, HEIGHT, REDRAW_ALL
    for pos, plt in platforms.items():
        if type(pos) is not tuple:
            raise TypeError(f'Положение платформы должно быть кортежём с двумя целыми числами, а не {pos}.')
        elif len(pos) != 2:
            raise ValueError(f'Положение платформы должно быть кортежём с двумя целыми числами, а не с {len(pos)} объектами.')
        elif type(pos[0]) is not int or type(pos[1]) is not int:
            raise TypeError(f'Координаты положения платформы должны быть целые числа, а не {type(pos[0])} и {type(pos[1])}.')
        elif type(plt) is not int:
            raise TypeError(f'Платформа должна быть целым числом, а не {type(plt)}')
        elif not 0 <= plt <= 10:
            raise ValueError(f'Не существует платформы под номером {plt}.')
    for pos, obj in objects.items():
        if type(pos) is not tuple:
            raise TypeError(f'Положение объекта должно быть кортежём с двумя целыми числами, а не {pos}.')
        elif len(pos) != 2:
            raise ValueError(f'Положение объекта должно быть кортежём с двумя целыми числами, а не с {len(pos)} объектами.')
        elif type(pos[0]) is not int or type(pos[1]) is not int:
            raise TypeError(f'Координаты положения объекта должны быть целые числа, а не {type(pos[0])} и {type(pos[1])}.')
        elif type(plt) is not int:
            raise TypeError(f'Объект должен быть целым числом, а не {type(plt)}')
        elif not 0 <= plt <= 17:
            raise ValueError(f'Не существует объекта под номером {plt}.')
    for pos, obj in zones.items():
        if type(pos) is not tuple:
            raise TypeError(f'Положение зоны должно быть кортежём с двумя целыми числами, а не {pos}.')
        elif len(pos) != 2:
            raise ValueError(f'Положение зоны должно быть кортежём с двумя целыми числами, а не с {len(pos)} объектами.')
        elif type(pos[0]) is not int or type(pos[1]) is not int:
            raise TypeError(f'Координаты положения зоны должны быть целые числа, а не {type(pos[0])} и {type(pos[1])}.')
        elif type(plt) is not int:
            raise TypeError(f'Зона должна быть целым числом, а не {type(plt)}')
        elif not 0 <= plt <= 2:
            raise ValueError(f'Не существует зоны под номером {plt}.')
    pos = robot.x, robot.y
    if not ignore_PlacementError:
        if platforms.get(pos, ABYSS) in {ABYSS, PIT}:
            raise PlacementError('Робот не может быть размещён над бездной или ямой: это приведёт к его стартовому разрушению.')
        if objects.get(pos, NOTHING) != NOTHING:
            raise PlacementError('Робот не может быть размещён в одной клетке с другим объектом.')
    platforms = {pos: plt for pos, plt in platforms.items() if plt != ABYSS}
    objects = {pos: obj for pos, obj in objects.items() if obj != NOTHING}
    camera_rect = game.Rect(0, 0, WIDTH // 4, HEIGHT // 4)
    camera_rect.center = robot.x * 16 + 8, robot.y * 16 + 8
    camera_speed = 0.03125
    camera_zoom_speed = 1.0625
    camera_velocity = (0, 0)
    platform_names = [f'platform|{p}' for p in 'iron stone box fragile damaged conveyor0|left conveyor0|right conveyor0|top conveyor0|bottom'.split(' ')]
    object_names = [f'object|{p}' for p in 'wall stone box fragile damaged factory|robot|left factory|robot|right factory|robot|top factory|robot|bottom factory|fragile|left factory|fragile|right factory|fragile|top factory|fragile|bottom factory|damaged|left factory|damaged|right factory|damaged|top factory|damaged|bottom'.split(' ')]
    zone_names = [None, 'zone|box|{}', 'zone|fragile|{}']
    camera_drag = False
    last_cursor_pos = None
    last_camera_pos = None
    follow_robot = True
    follow_koef = 0.125
    before_robot_step_runned = False
    last_act_time = time.time()
    running = True
    while running:
        clock.tick(FPS)
        #Случаи:
        for event in gameEvents():
            if event.type == game.QUIT:
                running = False
            elif event.type == game.VIDEORESIZE:
                center = camera_rect.center
                camera_rect.width = camera_rect.width * event.w / WIDTH
                camera_rect.height = camera_rect.height * event.h / HEIGHT
                camera_rect.center = center
                WIDTH = event.w
                HEIGHT = event.h
                REDRAW_ALL = True
            elif event.type == game.KEYDOWN:
                if event.key in {game.K_a, game.K_LEFT}:
                    camera_velocity = (camera_velocity[0] - 1, camera_velocity[1])
                elif event.key in {game.K_d, game.K_RIGHT}:
                    camera_velocity = (camera_velocity[0] + 1, camera_velocity[1])
                elif event.key in {game.K_w, game.K_UP}:
                    camera_velocity = (camera_velocity[0], camera_velocity[1] - 1)
                elif event.key in {game.K_s, game.K_DOWN}:
                    camera_velocity = (camera_velocity[0], camera_velocity[1] + 1)
                elif event.key == game.K_r:
                    follow_robot = True
            elif event.type == game.KEYUP:
                if event.key in {game.K_a, game.K_LEFT}:
                    camera_velocity = (camera_velocity[0] + 1, camera_velocity[1])
                elif event.key in {game.K_d, game.K_RIGHT}:
                    camera_velocity = (camera_velocity[0] - 1, camera_velocity[1])
                elif event.key in {game.K_w, game.K_UP}:
                    camera_velocity = (camera_velocity[0], camera_velocity[1] + 1)
                elif event.key in {game.K_s, game.K_DOWN}:
                    camera_velocity = (camera_velocity[0], camera_velocity[1] - 1)
            elif event.type == game.MOUSEBUTTONDOWN:
                if event.button == 3:
                    camera_drag = True
                    last_cursor_pos = event.pos
                    last_camera_pos = camera_rect.topleft
            elif event.type == game.MOUSEBUTTONUP:
                if event.button == 3:
                    camera_drag = False
                    last_cursor_pos = None
                    last_camera_pos = None
            elif event.type == game.MOUSEMOTION:
                if camera_drag:
                    drag = event.pos
                    drag = drag[0] - last_cursor_pos[0], drag[1] - last_cursor_pos[1]
                    drag = -drag[0] * camera_rect.width / WIDTH, -drag[1] * camera_rect.height / HEIGHT
                    camera_rect.topleft = last_camera_pos
                    camera_rect = camera_rect.move(drag)
                    follow_robot = False
                    REDRAW_ALL = True
            elif event.type == game.MOUSEWHEEL:
                if not camera_drag:
                    center = camera_rect.center
                    koef = camera_zoom_speed ** -event.y
                    camera_rect.width = camera_rect.width * koef
                    camera_rect.height = camera_rect.height * koef
                    camera_rect.center = center
                    REDRAW_ALL = True
        #Движение камеры:
        if not camera_drag and camera_velocity != (0, 0):
            camera_rect = camera_rect.move(camera_velocity[0] * camera_speed * camera_rect.width, camera_velocity[1] * camera_speed * camera_rect.height)
            follow_robot = False
            REDRAW_ALL = True
        if follow_robot:
            new_pos = robot.x * 16 + 8, robot.y * 16 + 8
            if camera_rect.center != new_pos:
                x, y = camera_rect.center
                camera_rect.center = x + follow_koef * (new_pos[0] - x), y + follow_koef * (new_pos[1] - y)
                REDRAW_ALL = True
        #Отображение:
        if REDRAW_ALL:
            before_redraw()
            screen.fill((0, 0, 0))
            min_x = max_x = min_y = max_y = None
            for pos in list(platforms) + list(objects) + list(zones):
                if min_x is None:
                    min_x, min_y = pos
                    max_x, max_y = pos
                else:
                    if pos[0] < min_x:
                        min_x = pos[0]
                    elif pos[0] > max_x:
                        max_x = pos[0]
                    if pos[1] < min_y:
                        min_y = pos[1]
                    elif pos[1] > max_y:
                        max_y = pos[1]
            min_x *= 16
            min_y *= 16
            w = 16 * (max_x + 1) - min_x
            h = 16 * (max_y + 1) - min_y
            layer = game.Surface((w, h), game.SRCALPHA)
            for pos, plat in platforms.items():
                glob_pos = pos[0] * 16, pos[1] * 16
                rect = game.Rect(*glob_pos, 16, 16)
                img = sprite[platform_names[plat]]
                layer.blit(img, rect)
            for pos, obj in objects.items():
                glob_pos = pos[0] * 16, pos[1] * 16
                rect = game.Rect(*glob_pos, 16, 16)
                img = sprite[object_names[obj]]
                layer.blit(img, rect)
            glob_pos = robot.x * 16, robot.y * 16
            rect = game.Rect(*glob_pos, 16, 16)
            img = sprite[f'robot00|{"left right top bottom".split(" ")[robot.way]}']
            layer.blit(img, rect)
            for pos, zone in zones.items():
                glob_pos = pos[0] * 16, pos[1] * 16
                rect = game.Rect(*glob_pos, 16, 16)
                img = sprite[zone_names[zone].format(objects.get(pos, NOTHING) - 1 == zone)]
                layer.blit(img, rect)
            my_blit(screen, layer, (min_x, min_y), camera_rect)
            game.display.flip()
            REDRAW_ALL = False
            after_redraw()

        if robot.is_alive:
            if time.time() - last_act_time < PERIOD:
                continue
            act = get_msg(now = True)
            if act is None:
                continue
            if not before_robot_step_runned:
                before_robot_step()
            before_robot_step_runned = True
            if act == 'forward':
                REDRAW_ALL = REDRAW_ALL or try_forward(robot, objects)
            elif act == 'left':
                rotate_left(robot)
                continue
            elif act == 'right':
                rotate_right(robot)
                continue
            elif act == 'check':
                check(robot, platforms, objects, zones)
                continue
            elif act == 'kick':
                REDRAW_ALL = REDRAW_ALL or try_kick(robot, objects)
            elif act.startwith('debug\n'):
                try:
                    exec(act[7:])
                except Exception as e:
                    print(f'При выполнении команды в режиме отладки произошла ошибка: {e}')
            else:
                print('Неизвестная команда "{act}".')
                continue
            before_robot_step_runned = False
            after_robot_step()
            before_physics()
            objs_for_act = [pos for pos, obj in objects.items() if obj not in {WALL, O_RFL, O_RFR, O_RFT, O_RFB}]
            prev = True
            while prev:
                prev = False
                i = 0
                while i < len(objs_for_act):
                    pos = objs_for_act[i]
                    if act_is_ended(pos, platforms, objects, robot, objs_for_act):
                        prev = True
                    else:
                        i += 1
            act_is_ended(robot, platforms, objects)
            after_physics()
            last_act_time = time.time()
    if not running:
        game.quit()

if __name__ == '__main__':
    if not os.path.exists('levels'):
        os.mkdir('levels')
        print('Каталог "levels" для уровней успешно создан!')
    if not os.path.exists('programms'):
        os.mkdir('programms')
        print('Каталог "programms" для программ успешно создан!')
    if not os.path.exists('levels\\my_new_level.py'):
        with open('levels\\my_new_level.py', 'wt', -1, 'utf-8') as f:
            f.write('import os\n' +
                    'import sys\n\n' +
                    'sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \'..\')))\n' +
                    'from Robot import *\n\n' +
                    'platforms = {(i % 20, i // 20): IRON for i in range(20 * 20)}\n' +
                    'objects = {(i % 20, i // 20): IRON for i in range(20 * 20) if i % 20 in {0, 19} or i // 20 in {0, 19}}\n' +
                    'objects[(11, 11)] = BOX\n' +
                    'zones = {(10, 10): BOX_ZONE}\n' +
                    'robot = Robot(10, 10, BOTTOM)\n\n' +
                    'if __name__ == \'__main__\':\n' +
                    '    level_run(platforms, objects, zones, robot)\n'
                    '    game.quit()')
        print('Создан пример уровня "my_new_level.py". Используйте его для создания своего уникального уровня.')
    else:
        print('Уровень "my_new_level.py" уже существует. Переименуйте или удалите его, чтобы я мог создать заного пример уровня для вас.')
    if not os.path.exists('programms\\my_new_programm.py'):
        with open('programms\\my_new_programm.py', 'wt', -1, 'utf-8') as f:
            f.write('import os\n' +
                    'import sys\n\n' +
                    'sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \'..\')))\n' +
                    'from Robot import *\n\n' +
                    'def robot_check():\n' +
                    '    """Передаёт команду роботу проверить. На выполнение этой команды робот не тратит ход!"""\n' +
                    '    global Floor, Objects, Zone\n' +
                    '    send_msg(\'check\')\n' +
                    '    get_msg(\'..\\\\info.msg\')\n' +
                    '    send_msg(\'check\')\n' +
                    '    Floor, Object, Zone = (int(x) for x in get_msg(\'..\\\\info.msg\').split(\' \'))\n\n' +
                    'if __name__ == \'__main__\':\n' +
                    '    input(\'Нажмите "Ввод" для старта программы.\\n\')\n' +
                    '    robot_forward()\n' +
                    '    robot_forward()\n' +
                    '    robot_left()\n' +
                    '    robot_forward()\n' +
                    '    robot_left()\n' +
                    '    robot_forward()\n' +
                    '    robot_right()\n' +
                    '    robot_forward()\n' +
                    '    robot_left()\n' +
                    '    robot_forward()\n' +
                    '    robot_left()\n' +
                    '    robot_forward()')
        print('Создан пример программы для оператора грузчика "my_new_programm.py". Используйте его для создания своей программы, решающей задачу.')
    else:
        print('Программа "my_new_programm.py" уже существует. Переименуйте или удалите её, чтобы я мог создать заного пример уровня для вас.')

import sys
import pygame as game

class Sprite(game.sprite.Sprite):
    """Класс игрового объекта."""

    def __init__(self, image, pos, rect = None):
        global all_sprites
        game.sprite.Sprite.__init__(self)
        self.image = Image(image)
        if rect == None:
            rect = self.image.get_rect()
        self.rect = rect
        self.rect.centerx = round(pos[0])
        self.rect.centery = round(pos[1])
        self.dpos = (pos[0] - round(pos[0]), pos[1] - round(pos[1]))
        all_sprites.add(self)

    def update(self):
        dx, dy = self.dpos
        self.dpos = (0, 0)
        self.move(dx, dy)

    def move(self, dx, dy):
        """Перемещает спрайт от своей текущей точки на (dx, dy)."""
        self.rect.centerx += round(dx)
        self.rect.centery += round(dy)
        self.dpos = (self.dpos[0] + dx - round(dx), self.dpos[1] + dy - round(dy))

    def moveTo(self, x, y):
        """Перемещает спрайт в точку (x, y)."""
        self.rect.centerx = round(x)
        self.rect.centery = round(y)
        self.dpos = (x - round(x), y - round(y))

    def img(self, image = None):
        """Возвращает изображение спрайта, если вызвано без аргументов, иначе - меняет изображение спрайта."""
        if image == None:
            return self.image
        else:
            self.image = Image(image)

    def draw(self, screen):
        screen.blit(self.img(), self.rect)

    def delete(self):
        """Удаляет объект полностью."""
        self.kill()
        del self

def newScreen(width: int, height: int, name: str = None, img: str = None, resizable: bool = False):
    """Возвращает игровое коно."""
    if resizable:
        screen = game.display.set_mode((width, height), game.RESIZABLE)
    else:
        screen = game.display.set_mode((width, height))
    if name != None:
        game.display.set_caption(name)
    if img != None:
        if type(img) is str:
            img = Image(img)
        game.display.set_icon(img)
    return screen

def Surface(sizes, color):
    """Возвращает поверхность."""
    surface = game.Surface(sizes)
    surface.fill(color)
    return surface

def Image(img):
    """Возвращает изображение."""
    if type(img) is str:
        if img[-4 :] == '.png':
            img = game.image.load(img).convert_alpha()
        else:
            img = game.image.load(img).convert()
    return img

def Rect(width, height):
    """Возвращает прямоугольник для спрайта."""
    return gameRect(0, 0, width, height)

def AllUpdate(screen, sprites, backColor, draw = True, text = None, pos = (0, 0), size = 1, cl = (0, 0, 0)):
    """Обновляет кадр и рисует текст text, если задан в pos размером size цвета cl."""
    screen.fill(backColor)
    if type(sprites) is list:
        for i in sprites:
            i.update()
            if draw:
                i.draw(screen)
    else:
        sprites.update()
        if draw:
            sprites.draw(screen)
    if text != None:
        write(screen, pos[0], pos[1], text, size, cl)
    game.display.flip()
    return None

linkCount = lambda obj: sys.getrefcount(obj) - 1
linkCount.__doc__ = 'Возвращает количество ссылок на объект obj.'

gameEvents = game.event.get
gameRect = game.rect.Rect
transform = game.transform
spriteCollide = game.sprite.spritecollide
groupCollide = game.sprite.groupcollide
getKeyPressed = game.key.get_pressed
getMousePressed = game.mouse.get_pressed
getMousePos = game.mouse.get_pos
newGroup = game.sprite.Group
draw = game.draw

game.init()
#game.mixer.init()
clock = game.time.Clock()

all_sprites = newGroup()

if __name__ == '__main__':
    class bounce(Sprite):

        def __init__(self, image, pos, rect = None, color = (0, 0, 0), speed = (0, 0)):
            Sprite.__init__(self, image, pos, rect)
            self.speed = list(speed)
            self.color = color
            self.cs = (1, 3, 5)

        def Move(self):
            speed = self.speed
            self.move(speed[0], speed[1])
            if self.rect.left < 0:
                self.rect.left = 0
                self.speed = [-speed[0], speed[1]]
            elif self.rect.top < 0:
                self.rect.top = 0
                self.speed = [speed[0], -speed[1]]
            elif self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.speed = [-speed[0], speed[1]]
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.speed = [speed[0], -speed[1]]

        def update(self):
            self.Move()
            r, g, b = self.color
            dr, dg, db = self.cs
            r += dr
            if r < 0 or r > 255:
                r = (255 - r) % 256
                dr = -dr
            g += dg
            if g < 0 or g > 255:
                g = (255 - g) % 256
                dg = -dg
            b += db
            if b < 0 or b > 255:
                b = (255 - b) % 256
                db = -db
            self.color = r, g, b
            self.cs = dr, dg, db
            surface = Surface((self.rect.width, self.rect.height), self.color)
            self.img(surface)

    FPS = 60
    WIDTH, HEIGHT = 1200, 600
    COUNT = 10

    screen = newScreen(WIDTH, HEIGHT)

    bs = []
    sizes = WIDTH // 20, HEIGHT // 20
    for i in range(COUNT):
        color = ((11 * COUNT * i) % 128 + 128, (19 * COUNT ** 2 * i) % 128 + 128, (31 * COUNT ** 3 * i) % 128 + 128)
        surface = Surface((sizes[0] * 2, sizes[1] * 2), color)
        pos = i / 3 * WIDTH, HEIGHT / 2
        speed = (-1) ** ((i * COUNT) % 29) * (i * COUNT * 101) % 29 + 5, (-1) ** ((i * COUNT ** 2) % 31) * (i * COUNT ** 2 * 199) % 31 + 5
        bs += [bounce(surface, pos, color = color, speed = speed)]

    running = True
    while running:
        clock.tick(FPS)
        for event in gameEvents():
            if event.type == game.QUIT:
                running = False

        AllUpdate(screen, all_sprites, (0, 0, 0))
    game.quit()

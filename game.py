import pygame as pg
from pathlib import Path
import math
from pygame.locals import Color


def load_image(file, scale=None):
    """ loads an image, prepares it for play
    """
    fpath = SPRITES_DIR / file
    assert fpath.exists()
    try:
        surface = pg.image.load(fpath.as_posix())
        if scale:
            surface = pg.transform.scale(surface, scale)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (fpath, pg.get_error()))
    return surface.convert_alpha()


class Player(pg.sprite.Sprite):
    acceleration = 0.1
    turn_deg = 4
    angle = 90
    speed = 0
    speed_x = 0
    car_size = (50, 40)
    max_speed = 10

    def __init__(self, terrain):
        super().__init__()
        self.original_image = load_image("car.png", self.car_size)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(midbottom=SCREEN_RECT.midbottom)
        self.terrain = terrain

    def speed_curve(self, x):
        return self.max_speed * 2 * ((1 / (1 + math.exp(-x / 10))) - 0.5)

    def update(self):
        keystrokes = pg.key.get_pressed()
        if keystrokes[pg.K_UP]:
            if self.speed + 0.01 < self.max_speed:
                self.speed_x += self.acceleration
                self.speed = self.speed_curve(self.speed_x)
        if keystrokes[pg.K_DOWN]:
            if self.speed - 0.01 > -self.max_speed:
                self.speed_x -= self.acceleration
                self.speed = self.speed_curve(self.speed_x)
        if keystrokes[pg.K_RIGHT]:
            self.angle -= self.turn_deg
            if self.angle < -180:
                self.angle += 360
        if keystrokes[pg.K_LEFT]:
            self.angle += self.turn_deg
            if self.angle > 180:
                self.angle -= 360

        # Rotate car and rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        # Move car
        self.rect.move_ip(self.speed * math.cos(math.radians(self.angle)),
                          -self.speed * math.sin(math.radians(self.angle)))
        self.rect = self.rect.clamp(SCREEN_RECT)

    def collide(self, xvel, yvel, terrain):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                if isinstance(p, FinishBlock):
                    pg.event.post(pg.event.Event(pg.QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class CameraAwareLayeredUpdates(pg.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pg.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_RECT.width/2
            y = -self.target.rect.center[1] + SCREEN_RECT.height/2
            self.cam += (pg.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-SCREEN_RECT.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-SCREEN_RECT.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty


class Terrain(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


class Grass(Terrain):
    def __init__(self, pos, *groups):
        super().__init__(Color("Green"), pos, *groups)


class FinishBlock(Terrain):
    def __init__(self, pos, *groups):
        super().__init__(Color("Black"), pos, *groups)


SPRITES_DIR = Path(__file__).resolve().parent / "sprites"
SCREEN_RECT = pg.Rect((0, 0, 800, 640))
TILE_SIZE = 16


def main():
    def show_text(text):
        text = font.render(text, True, Color("red"))
        display.blit(text, SCREEN_RECT.topleft)

    pg.init()
    display = pg.display.set_mode(SCREEN_RECT.size)
    pg.display.set_caption("Ultra Racr")
    clock = pg.time.Clock()
    font = pg.font.SysFont('Times New Roman', 20)
    level = [
        "GGGGGGGGGGGGGGGGGFFFFFFFFFGGGGGGGGGGGGGGGGGG",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
        "G                                          G",
    ]

    terrain = pg.sprite.Group()
    player = Player()
    entities = CameraAwareLayeredUpdates(player, pg.Rect(0, 0, len(level[0])*TILE_SIZE, len(level)*TILE_SIZE))
    x = y = 0
    for row in level:
        for col in row:
            if col == "G":
                Grass((x, y), terrain, entities)
            if col == "F":
                FinishBlock((x, y), terrain, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        entities.update()

        display.fill(Color("White"))
        entities.draw(display)
        display.blit(player.image, player.rect)
        pg.display.update()

        show_text(f"Speed : {player.speed:.2f} Current Angle : {player.angle:.2f} ")

        clock.tick(60)


if __name__ == "__main__":
    main()

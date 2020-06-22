import pygame as pg
import sys, os
from matplotlib.colors import to_rgb
from pathlib import Path
import time


def get_color(color_name: str) -> tuple:
    return tuple([val * 255 for val in to_rgb(color_name)])


def load_image(file, scale=None):
    """ loads an image, prepares it for play
    """
    fpath = sprites_folder / file
    assert fpath.exists()
    try:
        surface = pg.image.load(fpath.as_posix())
        if scale:
            surface = pg.transform.scale(surface, scale)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (fpath, pg.get_error()))
    return surface.convert()


sprites_folder = Path(__file__).resolve().parent / "sprites"

display_rect = pg.Rect(0, 0, 1000, 500)
pg.init()
display = pg.display.set_mode(display_rect.size)
display.fill(get_color("w"))


class Car(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = load_image("car.png", (40, 20))
        self.image = pg.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(midbottom=display_rect.bottomleft)

    def move(self, keystrokes):
        if keystrokes[pg.K_UP]:
            self.rect.move_ip(0, -1)
        if keystrokes[pg.K_DOWN]:
            self.rect.move_ip(0, 1)
        if keystrokes[pg.K_RIGHT]:
            self.rect.move_ip(1, 0)
        if keystrokes[pg.K_LEFT]:
            self.rect.move_ip(-1, 0)
        self.rect = self.rect.clamp(display_rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def main():
    player = Car()
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return
        pressed_keys = pg.key.get_pressed()
        player.move(pressed_keys)
        player.draw(display)

        pg.display.update()


if __name__ == "__main__":
    main()

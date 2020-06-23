from pathlib import Path
import pygame as pg
import random


def generate_level(width=40, length=200):
    level = list()
    for i in range(length):
        left = random.randint(0, width / 2)
        right = random.randint(0, width / 2)
        remainder = width - left - right
        level.append("G" * left + " " * remainder + "G" * right)
    return level

def load_image(file, scale=None):
    """
    Loads an image, prepares it for play
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


SPRITES_DIR = Path(__file__).resolve().parent / "sprites"
SCREEN_RECT = pg.Rect((0, 0, 800, 640))
TILE_SIZE = 32
level = generate_level()
level_width = len(level[0]) * TILE_SIZE
level_height = len(level) * TILE_SIZE

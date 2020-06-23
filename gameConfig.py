from pathlib import Path
import pygame as pg
import random
from noise import pnoise1


def generate_level(width=40, length=100, road_width=5):
    level = list()
    amplitude = 5
    noise = [pnoise1(x/length, 2, base=random.randint(0, 1000))
             for x in range(length)]
    max_val = max(abs(max(noise)), abs(min(noise)))
    left_start = int(width / 2 - road_width / 2)
    noise = [left_start + int(val * (amplitude / max_val)) for val in noise]

    import matplotlib.pyplot as plt
    plt.plot(noise)
    plt.show()

    for left in noise:
        right = width - road_width - left
        level.append("G" * left + " " * road_width + "G" * right)
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

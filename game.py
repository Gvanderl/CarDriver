from pygame.locals import *
import pygame
import sys
from matplotlib.colors import to_rgb
import time


def get_color(color_name: str) -> tuple:
    return tuple([val * 255 for val in to_rgb(color_name)])


pygame.init()
display = pygame.display.set_mode((600, 600))
display.fill(get_color("w"))
pygame.draw.rect(display, get_color("red"), (100, 100, 50, 100))

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

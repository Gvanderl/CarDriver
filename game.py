import pygame as pg
from matplotlib.colors import to_rgb
from pathlib import Path
import math


def get_color(color_name: str) -> tuple:
    return tuple([val * 255 for val in to_rgb(color_name)])


def load_image(file, scale=None):
    """ loads an image, prepares it for play
    """
    fpath = sprites_folder / file
    assert fpath.exists()
    try:
        surface = pg.image.load(fpath.as_posix()).convert_alpha()
        if scale:
            surface = pg.transform.scale(surface, scale)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (fpath, pg.get_error()))
    return surface.convert()


sprites_folder = Path(__file__).resolve().parent / "sprites"

display_rect = pg.Rect(0, 0, 1000, 500)
pg.init()
display = pg.display.set_mode(display_rect.size)


class Car(pg.sprite.Sprite):
    speed = 0.1
    cur_angle = 90
    car_size = (40, 20)

    def __init__(self):
        super().__init__()
        self.original_image = load_image("car.png", self.car_size)
        self.image = pg.transform.rotate(self.original_image, self.cur_angle)
        self.rect = self.image.get_rect(midbottom=display_rect.midbottom)
        self.speed_vector = [0.000001, 0.]

    def move(self, keystrokes):
        if keystrokes[pg.K_UP]:
            self.speed_vector[1] -= self.speed
        if keystrokes[pg.K_DOWN]:
            self.speed_vector[1] += self.speed
        if keystrokes[pg.K_RIGHT]:
            self.speed_vector[0] += self.speed
        if keystrokes[pg.K_LEFT]:
            self.speed_vector[0] -= self.speed

    def draw(self, surface):
        if abs(self.speed_vector[0]) + abs(self.speed_vector[1]) > 1:
            speed_vec_angle = (180 / math.pi) * math.atan2(-self.speed_vector[1], self.speed_vector[0])
            if abs(self.cur_angle - speed_vec_angle) > 0.01:
                print(f"Changing angle from {self.cur_angle:.2f} to {speed_vec_angle:.2f}")
                self.cur_angle = speed_vec_angle
                self.image = pg.transform.rotate(self.original_image, speed_vec_angle)
                self.rect = self.image.get_rect(topleft=self.rect.topleft)

        self.rect.move_ip(*self.speed_vector)
        surface.blit(self.image, self.rect)
        pg.draw.rect(display, get_color("red"), self.rect, 1)
        self.rect = self.rect.clamp(display_rect)


def main():
    player = Car()
    clock = pg.time.Clock()
    # font = pg.font.SysFont('Times New Roman', 30)
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return
        pressed_keys = pg.key.get_pressed()
        player.move(pressed_keys)
        player.draw(display)
        # text = font.render(f"Speed : {player.speed_vector[0]:.2f}, {player.speed_vector[1]:.2f} "
        #                    f"Current Angle : {player.cur_angle:.2f} "
        #                    f"Speed angle : "
        #                    f"{(180 / math.pi) * math.atan2(-player.speed_vector[1], player.speed_vector[0])}",
        #                    True, get_color("red"))
        #
        # display.blit(text, display_rect.topleft)
        pg.display.flip()
        display.fill(get_color("w"))
        clock.tick(60)


if __name__ == "__main__":
    main()

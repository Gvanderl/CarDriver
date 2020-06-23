import pygame as pg
from pathlib import Path
import math
from pygame.locals import Color


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
    return surface.convert_alpha()


sprites_folder = Path(__file__).resolve().parent / "sprites"

display_rect = pg.Rect(0, 0, 1000, 500)
pg.init()
display = pg.display.set_mode(display_rect.size)


class Car(pg.sprite.Sprite):
    acceleration = 0.1
    turn_deg = 2
    angle = 90
    speed = 0
    speed_x = 0
    car_size = (50, 25)
    max_speed = 10

    def __init__(self):
        super().__init__()
        self.original_image = load_image("car.png", self.car_size)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(midbottom=display_rect.midbottom)

    def speed_curve(self, x):
        return self.max_speed * 2 * ((1 / (1 + math.exp(-x/10))) - 0.5)

    def move(self, keystrokes):
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

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        self.rect.move_ip(self.speed * math.cos(math.radians(self.angle)),
                          -self.speed * math.sin(math.radians(self.angle)))
        surface.blit(self.image, self.rect)
        self.rect = self.rect.clamp(display_rect)

    def is_collided_with(self, other):
        self.rect.colliderect(other.rect)


def main():
    player = Car()
    clock = pg.time.Clock()
    font = pg.font.SysFont('Times New Roman', 30)
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return
        pressed_keys = pg.key.get_pressed()
        player.move(pressed_keys)
        player.draw(display)
        text = font.render(f"Speed : {player.speed:.2f} "
                           f"Current Angle : {player.angle:.2f} "
                           f"FPS: {clock.get_fps()} ",
                           True, Color("red"))

        display.blit(text, display_rect.topleft)
        pg.display.flip()
        display.fill(Color("White"))
        clock.tick(60)


if __name__ == "__main__":
    main()

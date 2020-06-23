import pygame as pg
import math
from pygame.locals import Color
from gameConfig import *

class Terrain(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


class Grass(Terrain):
    def __init__(self, pos, *groups):
        super().__init__(Color("PaleGreen"), pos, *groups)


class FinishLine(Terrain):
    def __init__(self, pos, *groups):
        super().__init__(Color("Black"), pos, *groups)


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
        self.rect = self.image.get_rect(midbottom=(level_width / 2, level_height - TILE_SIZE))
        self.terrain = terrain

    def speed_curve(self):
        # Use a sigmoid as a car speed function
        return self.max_speed * 2 * ((1 / (1 + math.exp(-self.speed_x / 10))) - 0.5)

    def update(self):
        keystrokes = pg.key.get_pressed()
        if keystrokes[pg.K_UP]:
            if self.speed + 0.01 < self.max_speed:
                self.speed_x += self.acceleration
                self.speed = self.speed_curve()
        if keystrokes[pg.K_DOWN]:
            if self.speed - 0.01 > -self.max_speed:
                self.speed_x -= self.acceleration
                self.speed = self.speed_curve()
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
        self.rect = self.rect.clamp(pg.Rect(0, 0, level_width, level_height))

        self.collide()

    def collide(self):
        for p in self.terrain:
            if pg.sprite.collide_rect(self, p):
                if isinstance(p, FinishLine):
                    pg.event.post(pg.event.Event(pg.QUIT))
                if isinstance(p, Grass):
                    self.speed_x = max(3, self.speed_x / 2)
                    self.speed = self.speed_curve()
                    p.image.fill(Color("DarkGreen"))
                    return


class CameraAwareLayeredUpdates(pg.sprite.LayeredUpdates):

    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pg.Vector2(0, 0)
        self.world_size = world_size
        self.font = pg.font.SysFont('Times New Roman', 60)
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
        dirty = self.lostsprites
        self.lostsprites = []
        for spr in self.sprites()[::-1]:
            rec = spritedict[spr]
            newrect = surface.blit(spr.image, spr.rect.move(self.cam))
            if rec is self._init_rect:
                dirty.append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty.append(newrect.union(rec))
                else:
                    dirty.append(newrect)
                    dirty.append(rec)
            spritedict[spr] = newrect
            if isinstance(spr, Player):
                text = self.font.render(f"Speed : {spr.speed:.2f}", True, Color("red"))
                surface.blit(text, SCREEN_RECT.topleft)
        return dirty

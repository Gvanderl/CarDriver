from gameEntities import *


def main():

    pg.init()
    font = pg.font.SysFont('Times New Roman', 60)
    display = pg.display.set_mode(SCREEN_RECT.size)
    pg.display.set_caption("Ultra Racr")
    clock = pg.time.Clock()

    terrain = pg.sprite.Group()
    player = Player(terrain)
    entities = CameraAwareLayeredUpdates(player, pg.Rect(0, 0, level_width, level_height))
    x = y = 0
    for row in level:
        for col in row:
            if col == "G":
                Grass((x, y), terrain, entities)
            if col == "F":
                FinishLine((x, y), terrain, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        entities.update()

        display.fill(Color("DarkGrey"))
        entities.draw(display)
        text = font.render(f"FPS : {clock.get_fps()}", True, Color("red"))
        display.blit(text, SCREEN_RECT.topleft)
        pg.display.update()

        clock.tick(60)


if __name__ == "__main__":
    main()

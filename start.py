import pygame as pg

CELL_SIZE = 25
W_CELL_COUNT, H_CELL_COUNT = 50, 30
W, H = W_CELL_COUNT * (CELL_SIZE + 1) + 1, H_CELL_COUNT * (CELL_SIZE + 1) + 1
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (50, 60, 50)
FPS = 30

clock = pg.time.Clock()


def draw_background(surface):
    surface.fill(BACKGROUND_COLOR)
    for x in range(0, W, (CELL_SIZE + 1)):
        pg.draw.line(surface, GRID_COLOR, (x, 0), (x, H))
    for y in range(0, H, (CELL_SIZE + 1)):
        pg.draw.line(surface, GRID_COLOR, (0, y), (W, y))


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption('ConwaysLife')

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        draw_background(sc)
        pg.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()

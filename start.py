import random
import pygame as pg

CELL_SIZE = 25
W_CELL_COUNT, H_CELL_COUNT = 50, 30
W, H = W_CELL_COUNT * (CELL_SIZE + 1) + 1, H_CELL_COUNT * (CELL_SIZE + 1) + 1
DELTA_COLOR = 15
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (50, 60, 50)
FPS = 30

clock = pg.time.Clock()


def create_cells():
    cells = {}
    for col in range(0, W_CELL_COUNT):
        for row in range(0, H_CELL_COUNT):
            cells[(row, col)] = {
                'content': random.randint(0, 9),
                'command': '',
                'rect': pg.Rect(col * (CELL_SIZE + 1) + 1, row * (CELL_SIZE + 1) + 1, CELL_SIZE, CELL_SIZE)
            }
    return cells


def draw_background(surface):
    surface.fill(BACKGROUND_COLOR)
    for x in range(0, W, (CELL_SIZE + 1)):
        pg.draw.line(surface, GRID_COLOR, (x, 0), (x, H))
    for y in range(0, H, (CELL_SIZE + 1)):
        pg.draw.line(surface, GRID_COLOR, (0, y), (W, y))


def draw_cells(surface, cells):
    for cell_data in cells.values():
        content = cell_data['content']
        if not content:
            continue
        color = (255 - (content - 1) * DELTA_COLOR,) * 3
        pg.draw.rect(surface, color, cell_data['rect'])


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption('ConwaysLife')

    cells = create_cells()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        draw_background(sc)
        draw_cells(sc, cells)
        pg.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()

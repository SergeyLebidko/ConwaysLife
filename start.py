import pygame as pg

CELL_SIZE = 25
W_CELL_COUNT, H_CELL_COUNT = 50, 30
W, H = W_CELL_COUNT * (CELL_SIZE + 1) + 1, H_CELL_COUNT * (CELL_SIZE + 1) + 1
PAUSE_MODE = 'pause'
PLAY_MODE = 'play'
DELTA_CELLS = [(d_row, d_col) for d_row in range(-1, 2) for d_col in range(-1, 2) if d_row != 0 or d_col != 0]
DELTA_COLOR = 20
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (50, 60, 50)
FPS = 30

clock = pg.time.Clock()


def create_cells():
    cells = {}
    for col in range(0, W_CELL_COUNT):
        for row in range(0, H_CELL_COUNT):
            cells[(row, col)] = {
                'content': 0,
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


def get_draw_mode_function():
    mode_surface = pg.Surface((W, H))
    mode_surface.set_colorkey((255, 0, 0))
    mode_surface.set_alpha(150)

    def draw_mode(surface, mode):
        mode_surface.fill((255, 0, 0))
        if mode == PAUSE_MODE:
            pg.draw.rect(mode_surface, (255, 255, 255), (10, 10, 20, 40))
            pg.draw.rect(mode_surface, (255, 255, 255), (40, 10, 20, 40))
        if mode == PLAY_MODE:
            pg.draw.polygon(mode_surface, (255, 255, 255), ((20, 10), (50, 30), (20, 50)))
        surface.blit(mode_surface, (0, 0))

    return draw_mode


def get_cell_at_point(x, y, cells):
    for _, cell_data in cells.items():
        if cell_data['rect'].collidepoint(x, y):
            return cell_data
    return None


def next_state(cells):
    for (row, col), cell_data in cells.items():
        # Подсчитываем количество соседей у клетки
        around_count = 0
        for d_row, d_col in DELTA_CELLS:
            beside_cell = cells.get((row + d_row, col + d_col), None)
            if not beside_cell:
                continue
            if beside_cell['content']:
                around_count += 1

        # В зависимости от количества соседей определяем состояние клетки в следующем "поколении"
        if cell_data['content']:
            if around_count < 2 or around_count > 3:
                cell_data['command'] = 'death'
            else:
                cell_data['command'] = '+age'
        else:
            if around_count == 3:
                cell_data['command'] = '+age'

    # Обновляем состояния клеток (переходим с следующему "поколению")
    for _, cell_data in cells.items():
        command = cell_data['command']

        if not command:
            continue
        if command == 'death':
            cell_data['content'] = 0
        elif command == '+age':
            cell_data['content'] = cell_data['content'] + 1 if cell_data['content'] < 9 else 0
        cell_data['command'] = ''


def check_population(cells):
    for _, cell_data in cells.items():
        if cell_data['content']:
            return True
    return False


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption('ConwaysLife')

    cells = create_cells()

    mode = PAUSE_MODE
    draw_mode = get_draw_mode_function()
    frame_count = 0
    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                mode = {PAUSE_MODE: PLAY_MODE, PLAY_MODE: PAUSE_MODE}[mode]
                break

            if event.type == pg.MOUSEBUTTONDOWN and mode == PAUSE_MODE:
                cell = get_cell_at_point(*event.pos, cells)
                if not cell:
                    continue
                if event.button == pg.BUTTON_LEFT:
                    cell['content'] = cell['content'] + 1 if cell['content'] < 9 else 0
                if event.button == pg.BUTTON_RIGHT:
                    cell['content'] = 0

        draw_background(sc)
        draw_cells(sc, cells)
        draw_mode(sc, mode)
        pg.display.update()

        clock.tick(FPS)

        if mode == PLAY_MODE:
            if not check_population(cells):
                mode = PAUSE_MODE
                continue

        if mode == PLAY_MODE:
            frame_count += 1
            if frame_count == FPS:
                next_state(cells)
                frame_count = 0


if __name__ == '__main__':
    main()

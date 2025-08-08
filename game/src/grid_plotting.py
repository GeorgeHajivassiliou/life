from game.src.core import draw, grids
import pygame


class Ploter:
    def __init__(self, canvas: draw.Canvas, grid_spacing: int = 20):
        self._grid_spacing = grid_spacing
        self._canvas = canvas

    def plot(self, grid: grids.Grid):
        self._plot_all_cells(grid)
        self._canvas.update()

    def _plot_cell(self, cell: grids.Cell):
        square_x = cell.coordinates.x * self._grid_spacing
        square_y = cell.coordinates.y * self._grid_spacing
        if cell.value:
            self._canvas.draw_square(square_x, square_y, self._grid_spacing)

    def _plot_all_cells(self, grid):
        for cell in grid.values():
            self._plot_cell(cell)


def hang_until_quit_event():
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True


if __name__ == "__main__":
    total_x = 800
    total_y = 400
    cv = draw.Canvas(total_x, total_y)
    cv.make()
    gd = grids.Grid((40, 20))

    for c in [
        (5, 5),
        (6, 5),
        (10, 10),
        (20, 7),
        (20, 8),
    ]:
        cell = grids.Cell(grids.Coordinates(*c), True)
        gd.set(cell)
    plotter = Ploter(cv, 20)
    plotter.plot(gd)

    hang_until_quit_event()
    pygame.quit()

from life import draw
from life.core import grids


class Plotter:
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
            self._canvas.add_square(square_x, square_y, self._grid_spacing)
        else:
            self._canvas.erase_square(square_x, square_y, self._grid_spacing)

    def _plot_all_cells(self, grid):
        for cell in grid.values():
            self._plot_cell(cell)

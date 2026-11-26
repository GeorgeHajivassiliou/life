from collections.abc import Iterable

from game.core import grids


class _NeighbourCalculator:
    def calculate(
        self,
        src: grids.Coordinates,
    ) -> Iterable[grids.Coordinates]:
        for dx, dy in self._displacements():
            neighbour = grids.Coordinates(src.x + dx, src.y + dy)
            yield neighbour

    def _displacements(self) -> Iterable[tuple]:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):
                    continue
                yield dx, dy


class _StateCalculator:
    def calculate(self, alive: bool, alive_neighbours: int):

        if alive:
            state = self._stay_alive(alive_neighbours)
        else:
            state = self._come_alive(alive_neighbours)

        return state

    def _stay_alive(self, alive_neighbours):
        return alive_neighbours in (2, 3)

    def _come_alive(self, alive_neighbours):
        return alive_neighbours == 3


class Game:
    def __init__(self, grid: grids.Grid):
        self._grid = grid

    def update(self):
        updated_cells = self._get_updated_cells()
        self._add_cells_to_grid(updated_cells)

    def _get_updated_cells(self):
        result = []
        for cell in self._grid.values():
            updated_cell = self._update_cell(cell)
            result.append(updated_cell)

        return result

    def _add_cells_to_grid(self, cells: Iterable[grids.Cell]):
        for cell in cells:
            self._grid.set(cell)

    def _update_cell(self, cell: grids.Cell) -> grids.Cell:
        neighbour_coordinates = _NeighbourCalculator().calculate(cell.coordinates)
        alive_neighbours = self._count_alive_neighbours(neighbour_coordinates)
        new_value = _StateCalculator().calculate(cell.value, alive_neighbours)
        updated_cell = grids.Cell(cell.coordinates, new_value)
        return updated_cell

    def _count_alive_neighbours(
        self, neighbour_coordinates: Iterable[grids.Coordinates]
    ) -> int:

        neighbours = [self._grid.get(neighbour) for neighbour in neighbour_coordinates]
        result = sum(neighbour.value for neighbour in neighbours)
        return result

    def get_grid(self) -> grids.Grid:
        return self._grid

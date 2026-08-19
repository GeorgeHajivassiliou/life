from collections.abc import Iterable

from game.src.core import grids


class NeighbourCalculator:
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


class StateCalculator:
    def calculate(self, alive: bool, neighbour_values: Iterable[bool]):
        if len(list(neighbour_values)) != 8:
            raise ValueError("each cell has 8 neighbours")

        alive_neightbours = sum(neighbour_values)

        if alive:
            state = self._stay_alive(alive_neightbours)
        else:
            state = self._come_alive(alive_neightbours)

        return state

    def _stay_alive(self, alive_neightbours):
        return alive_neightbours in (2, 3)

    def _come_alive(self, alive_neightbours):
        return alive_neightbours == 3


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
        neighbour_coordinates = NeighbourCalculator().calculate(cell.coordinates)
        neighbour_values = self._get_neighbour_values(neighbour_coordinates)
        new_value = StateCalculator().calculate(cell.value, neighbour_values)
        updated_cell = grids.Cell(cell.coordinates, new_value)
        return updated_cell

    def _get_neighbour_values(
        self, neighbour_coordinates: Iterable[grids.Coordinates]
    ) -> list[bool]:
        result = []
        for neighbour in neighbour_coordinates:
            n = self._grid.get(neighbour)
            result.append(n.value)
        return result

    def get_grid(self) -> grids.Grid:
        return self._grid

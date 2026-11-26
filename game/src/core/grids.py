from collections.abc import Iterable
from typing import NamedTuple


class Coordinates(NamedTuple):
    x: int
    y: int


class Cell(NamedTuple):
    coordinates: Coordinates
    value: bool


class Grid:
    """
    Cell container. Cells accessed by coordinate tuple (x,y).
    Unset coordinates return a dead Cell
    """

    def __init__(self, dimensions: tuple[int, int]):
        self._dimensions = dimensions
        self.__store: dict[Coordinates, Cell] = {}

    def get(self, cell_coordinates: Coordinates | tuple) -> Cell:
        cell_coordinates = self._cast_coordinates(cell_coordinates)
        result = self.__store.get(cell_coordinates, Cell(cell_coordinates, False))
        return result

    def set(self, cell: Cell):
        self.__store[cell.coordinates] = cell

    def items(self) -> Iterable[tuple[Coordinates, Cell]]:
        for coordinates in self.keys():
            yield (coordinates, self.get(coordinates))

    def values(self) -> Iterable[Cell]:
        for coordinates in self.keys():
            yield self.get(coordinates)

    def keys(self) -> Iterable[Coordinates]:
        for y in range(self._dimensions[1]):
            for x in range(self._dimensions[0]):
                result = Coordinates(x, y)
                yield result

    @property
    def dimensions(self):
        return self._dimensions

    def _cast_coordinates(self, coordinates: Coordinates | tuple) -> Coordinates:
        if isinstance(coordinates, tuple):
            coordinates = Coordinates(*coordinates)

        return coordinates

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return NotImplemented

        if self.dimensions != other.dimensions:
            return False

        return all(a == b for a, b in zip(self.items(), other.items(), strict=True))

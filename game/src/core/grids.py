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
        if cell_coordinates not in self.__store:
            self.__store[cell_coordinates] = Cell(cell_coordinates, False)

        result = self.__store[cell_coordinates]
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
        assert isinstance(other, Grid), "Grid can only be compared to grid"
        if self.dimensions != other.dimensions:
            print(f"Mismatch in dimensions: {self.dimensions} != {other.dimensions}")
            return False

        pairs = {a[0]: a == b for a, b in zip(self.items(), other.items(), strict=True)}
        if all(pairs.values()):
            return True
        else:
            mismatches = [
                coordinates for coordinates, match in pairs.items() if not match
            ]
            print(f"Mismatch in the following coordinates: {mismatches}")
            return False

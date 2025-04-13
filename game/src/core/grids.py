from typing import Iterable, NamedTuple


class Coordinates(NamedTuple):
    x: int
    y: int


class Cell(NamedTuple):
    coordinates: Coordinates
    value: bool


class Grid:
    """
    Cell container. Cells access by coordinate tuple (x,y).
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
        for x in range(self._dimensions[0]):
            for y in range(self._dimensions[1]):
                result = Coordinates(x, y)
                yield result

    def _cast_coordinates(self, coordinates: Coordinates | tuple):
        if isinstance(coordinates, tuple):
            coordinates = Coordinates(*coordinates)

        return coordinates

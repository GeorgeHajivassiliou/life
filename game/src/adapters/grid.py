from typing import NamedTuple

from game.src.core import grids

PositiveCoordinates = list[grids.Coordinates]


class SerialisedGrid(NamedTuple):
    positive_coordinates: PositiveCoordinates
    dimensions: tuple[int, int]


def serialise(grid: grids.Grid) -> SerialisedGrid:
    return SerialisedGrid(
        [c.coordinates for c in grid.values() if c.value], grid.dimensions
    )


def deserialise(serialised_grid: SerialisedGrid) -> grids.Grid:
    result = grids.Grid(serialised_grid.dimensions)
    for coordinates in serialised_grid.positive_coordinates:
        result.set(grids.Cell(coordinates, True))

    return result

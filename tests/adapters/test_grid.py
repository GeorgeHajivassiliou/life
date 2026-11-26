import pytest

from life.adapters import grid
from life.core import grids


@pytest.fixture
def serialised_grid():
    positive_cells = [grids.Coordinates(0, 1)]
    return grid.SerialisedGrid(positive_cells, (3, 3))


@pytest.fixture
def populated_grid():
    gd = grids.Grid((3, 3))
    c1 = grids.Cell(grids.Coordinates(0, 1), True)
    gd.set(c1)
    return gd


def test_serialise(serialised_grid, populated_grid):
    provided = populated_grid
    expected = serialised_grid

    observed = grid.serialise(provided)
    assert observed == expected


def test_deserialise(serialised_grid, populated_grid):
    provided = serialised_grid
    expected = populated_grid

    observed = grid.deserialise(provided)
    assert observed == expected

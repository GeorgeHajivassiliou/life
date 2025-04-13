import pytest
from game.src.core import grids


class TestGrid:
    @pytest.fixture
    def grid(self):
        result = grids.Grid((2, 2))
        cell = grids.Cell(grids.Coordinates(0, 1), True)
        result.set(cell)
        return result

    def test_get_values(self, grid):
        expected = [False, True, False, False]
        observed = [c.value for c in grid.values()]
        assert observed == expected

    def test_get_items(self, grid):
        expected = [
            ((0, 0), False),
            ((0, 1), True),
            ((1, 0), False),
            ((1, 1), False),
        ]
        observed = [((c[0]), c[1].value) for c in grid.items()]
        assert observed == expected

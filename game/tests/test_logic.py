import pytest
from game.src.core import logic
from game.src.core import grids


class TestNeighbourCalculator:
    _base_coordinates = (0, 0)
    _base_neighbours = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, 0),
        (1, -1),
    ]

    _TEST_CASES = [
        pytest.param({"src_cell": (0, 0)}),
        pytest.param({"src_cell": (5, 7)}),
        pytest.param({"src_cell": (-10, 1)}),
    ]

    @pytest.fixture(params=_TEST_CASES)
    def test_case(self, request):
        return request.param

    @pytest.fixture
    def src_cell(self, test_case):
        return test_case["src_cell"]

    @pytest.fixture
    def provided(self, src_cell):
        result = grids.Coordinates(*src_cell)
        return result

    @pytest.fixture
    def expected(self, src_cell):
        dx = src_cell[0] - self._base_coordinates[0]
        dy = src_cell[1] - self._base_coordinates[1]
        result = [(c[0] + dx, c[1] + dy) for c in self._base_neighbours]
        return result

    def test_calculate(self, provided, expected):
        observed = [tuple(c) for c in logic.NeighbourCalculator().calculate(provided)]
        assert sorted(observed) == sorted(expected)

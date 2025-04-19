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


class TestStateCalculator:
    _TEST_CASES = [
        pytest.param(
            {
                "neighbour_states": [False] * 8,
                "current_state": False,
                "new_state": False,
            }
        ),
        pytest.param(
            {
                "neighbour_states": [False] * 8,
                "current_state": True,
                "new_state": False,
            }
        ),
        pytest.param(
            {
                "neighbour_states": [False] * 6 + [True] * 2,
                "current_state": False,
                "new_state": False,
            }
        ),
        pytest.param(
            {
                "neighbour_states": [False] * 6 + [True] * 2,
                "current_state": True,
                "new_state": True,
            }
        ),
        pytest.param(
            {
                "neighbour_states": [False] * 5 + [True] * 3,
                "current_state": False,
                "new_state": True,
            }
        ),
        pytest.param(
            {
                "neighbour_states": [False] * 4 + [True] * 4,
                "current_state": True,
                "new_state": False,
            }
        ),
    ]

    @pytest.fixture(params=_TEST_CASES)
    def test_case(self, request):
        return request.param

    @pytest.fixture
    def provided(self, test_case):
        return test_case["current_state"], test_case["neighbour_states"]

    @pytest.fixture
    def expected(self, test_case):
        return test_case["new_state"]

    @pytest.fixture
    def state_calculator(self):
        result = logic.StateCalculator()
        return result

    def test_something(self, state_calculator, provided, expected):
        current_state, neighbour_states = provided
        observed = state_calculator.calculate(current_state, neighbour_states)
        assert observed == expected


class TestGame:
    _TEST_CASES = [
        pytest.param(
            {
                "alive_cells": [(2, 0), (2, 1), (2, 2)],
                "expected": [False] * 3 + [False, True, False] + [False, True, False],
            }
        ),
        pytest.param({"alive_cells": [], "expected": [False] * 9}),
        pytest.param({"alive_cells": [(1, 1)], "expected": [False] * 9}),
    ]

    @pytest.fixture(params=_TEST_CASES)
    def test_case(self, request):
        return request.param

    @pytest.fixture()
    def alive_cells(self, test_case):
        return test_case["alive_cells"]

    @pytest.fixture
    def grid(self, alive_cells):
        grid = grids.Grid((3, 3))
        for coordinates in alive_cells:
            cell = grids.Cell(grids.Coordinates(*coordinates), True)
            grid.set(cell)

        return grid

    @pytest.fixture
    def expected(self, test_case):
        return test_case["expected"]

    def test_update(self, grid, expected):
        game = logic.Game(grid)
        game.update()
        updated_grid = game.get_grid()
        observed = [cell.value for cell in updated_grid.values()]
        assert observed == expected

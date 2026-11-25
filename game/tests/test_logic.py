import itertools
from collections.abc import Iterable

import pytest

from game.src.core import grids, logic


def _sparse_to_dense(matrix: list[list[bool]]):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            value = matrix[y][x]
            if value:
                yield (x, y)


def _make_grid(alive_cells: Iterable[tuple]):
    grid = grids.Grid((3, 3))
    for coordinates in alive_cells:
        cell = grids.Cell(grids.Coordinates(*coordinates), True)
        grid.set(cell)

    return grid


class TestGame:
    _TEST_CASES = (
        pytest.param(
            {
                "alive_cells": [
                    [False, False, True],
                    [False, True, False],
                    [False, False, True],
                ],
                "expected": [
                    [False, False, False],
                    [False, True, True],
                    [False, False, False],
                ],
            },
            id="Two neighbours;stay alive",
        ),
        pytest.param(
            {
                "alive_cells": [
                    [False, False, True],
                    [False, False, True],
                    [False, False, True],
                ],
                "expected": [
                    [False, False, False],
                    [False, True, True],
                    [False, False, False],
                ],
            },
            id="Three neighbours;comes alive",
        ),
        pytest.param(
            {
                "alive_cells": [
                    [True, False, True],
                    [False, True, False],
                    [True, False, True],
                ],
                "expected": [
                    [False, True, False],
                    [True, False, True],
                    [False, True, False],
                ],
            },
            id="Overpopulation",
        ),
        pytest.param(
            {
                "alive_cells": [
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                ],
                "expected": [[False] * 3] * 3,
            },
            id="All dead; stay dead",
        ),
        pytest.param(
            {
                "alive_cells": [
                    [False, False, False],
                    [False, True, False],
                    [False, False, False],
                ],
                "expected": [[False] * 3] * 3,
            },
            id="lonely cell dies",
        ),
        pytest.param(
            {
                "alive_cells": [
                    [False, True, False],
                    [False, True, False],
                    [False, True, False],
                ],
                "expected": [
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                ],
            },
            id="blinker",
        ),
    )

    @pytest.fixture(params=_TEST_CASES)
    def test_case(self, request):
        return request.param

    @pytest.fixture()
    def alive_cells(self, test_case):
        sparse = test_case["alive_cells"]
        result = list(_sparse_to_dense(sparse))
        print(list(result))
        return result

    @pytest.fixture
    def grid(self, alive_cells):
        result = _make_grid(alive_cells)
        return result

    @pytest.fixture
    def expected(self, test_case):
        matrix = test_case["expected"]
        result = list(itertools.chain(*matrix))
        return result

    def test_update(self, grid, expected):
        game = logic.Game(grid)
        game.update()
        updated_grid = game.get_grid()
        observed = [cell.value for cell in updated_grid.values()]
        assert observed == expected

    def test_oscillate(self):
        state_A = [
            [False, True, False],
            [False, True, False],
            [False, True, False],
        ]

        state_B = [
            [False, False, False],
            [True, True, True],
            [False, False, False],
        ]

        grid = _make_grid(_sparse_to_dense(state_A))
        game = logic.Game(grid)
        game.update()

        updated_grid = game.get_grid()
        observed = [cell.value for cell in updated_grid.values()]
        expected = list(itertools.chain(*state_B))
        assert observed == expected

        game.update()

        updated_grid = game.get_grid()
        observed = [cell.value for cell in updated_grid.values()]
        expected = list(itertools.chain(*state_A))
        assert observed == expected

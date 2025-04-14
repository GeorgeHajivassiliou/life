from typing import Iterable
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
    def calculate(self, current_state: bool, neighbour_states: Iterable[bool]):
        n_alive = sum(neighbour_states)

        if not current_state:
            if n_alive == 3:
                return True
            else:
                return False

        if n_alive < 2:
            return False
        elif n_alive in (2, 3):
            return True
        else:
            return False

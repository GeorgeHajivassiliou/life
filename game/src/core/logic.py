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

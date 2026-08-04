import time

import pygame

from game.src import draw, grid_plotting
from game.src.core import grids, logic

if __name__ == "__main__":
    total_x = 800
    total_y = 400
    cv = draw.Canvas(total_x, total_y)
    cv.make()
    gd = grids.Grid((40, 20))

    for c in [
        (5, 5),
        (6, 5),
        (7, 5),
        (10, 10),
        (20, 7),
        (20, 8),
    ]:
        cell = grids.Cell(grids.Coordinates(*c), True)
        gd.set(cell)
    plotter = grid_plotting.Ploter(cv, 20)
    plotter.plot(gd)
    _ = pygame.event.get()
    game = logic.Game(gd)

    while True:
        time.sleep(0.1)
        game.update()
        updated_grid = game.get_grid()

        plotter.plot(updated_grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

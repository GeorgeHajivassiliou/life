import pygame


class Canvas:
    __slots__ = ("_background", "_height", "_rect_colour", "_screen", "_width")

    def __init__(
        self,
        width: int,
        height: int,
        background_colour: tuple[int, int, int] = (0, 0, 0),
        rect_colour=(200, 100, 100),
    ):
        self._width = width
        self._height = height
        self._background = background_colour
        self._rect_colour = rect_colour
        self._screen = None

    def make(self):
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._screen.fill(self._background)

    def draw_square(self, x: int, y: int, a: int = 20):
        transformed_y = (
            self._height - y - a
        )  # so that origin os on the bottom left of the screen and
        #  the square coordinated point to the bottom left of the square
        assert self._screen is not None, "Screen cannot be None at this stage"
        pygame.draw.rect(self._screen, self._rect_colour, [x, transformed_y, a, a])

    def erase_square(self, x: int, y: int, a: int = 20):
        transformed_y = (
            self._height - y - a
        )  # so that origin os on the bottom left of the screen and
        #  the square coordinated point to the bottom left of the square
        assert self._screen is not None, "Screen cannot be None at this stage"
        pygame.draw.rect(self._screen, self._background, [x, transformed_y, a, a])

    def update(self):
        pygame.display.flip()


def hang_until_quit_event():
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True


def draw_n_squares(n):
    a = 20
    for i in range(n):
        cv.draw_square(i * a, i * a, a)


if __name__ == "__main__":
    total_x = 800
    total_y = 400
    cv = Canvas(total_x, total_y)
    cv.make()
    draw_n_squares(n=15)
    cv.update()
    hang_until_quit_event()
    pygame.quit()

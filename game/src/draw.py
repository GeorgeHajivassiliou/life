import pygame

Colour = tuple[int, int, int]


class Canvas:
    __slots__ = ("_background", "_height", "_rect_colour", "_screen", "_width")

    def __init__(
        self,
        width: int,
        height: int,
        background_colour: Colour = (0, 0, 0),
        rect_colour: Colour = (200, 100, 100),
    ):
        self._width = width
        self._height = height
        self._background = background_colour
        self._rect_colour = rect_colour
        self._screen = None

    def make(self):
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._screen.fill(self._background)

    def add_square(self, x: int, y: int, a: int = 20):
        self._draw_square(x, y, a, self._rect_colour)

    def erase_square(self, x: int, y: int, a: int = 20):
        self._draw_square(x, y, a, self._background)

    def _draw_square(self, x: int, y: int, a: int, colour: Colour):
        transformed_y = (
            self._height - y - a
        )  # so that origin is on the bottom left of the screen and
        #  the square coordinates point to the bottom left of the square
        assert self._screen is not None, "Screen cannot be None at this stage"
        pygame.draw.rect(self._screen, colour, [x, transformed_y, a, a])

    def update(self):
        pygame.display.flip()


if __name__ == "__main__":

    def _hang_until_quit_event():
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def _draw_n_squares(n):
        a = 20
        for i in range(n):
            cv.add_square(i * a, i * a, a)

    total_x = 800
    total_y = 400
    cv = Canvas(total_x, total_y)
    cv.make()
    _draw_n_squares(n=15)
    cv.update()
    _hang_until_quit_event()
    pygame.quit()

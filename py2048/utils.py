import pygame.color as c


class Colors:

    BG = c.Color(187, 173, 160)
    BOX_EMPTY = c.Color(214, 205, 196)
    BOX_2 = c.Color(238, 228, 216)
    BOX_4 = c.Color(236, 224, 200)
    BOX_8 = c.Color(242, 177, 121)
    BOX_16 = c.Color(246, 148, 99)
    BOX_32 = c.Color(245, 124, 95)
    BOX_64 = c.Color(246, 93, 61)
    BOX_128 = c.Color(237, 206, 113)
    BOX_256 = c.Color(237, 204, 97)
    BOX_512 = c.Color(236, 200, 80)
    BOX_1024 = c.Color(237, 197, 63)
    BOX_2048 = c.Color(237, 197, 46)

    __COLORS = {
        -1: BG,
        0: BOX_EMPTY,
        2: BOX_2,
        4: BOX_4,
        8: BOX_8,
        16: BOX_16,
        32: BOX_32,
        64: BOX_64,
        128: BOX_128,
        256: BOX_256,
        512: BOX_512,
        1024: BOX_1024,
        2048: BOX_2048
    }

    def __getitem__(self, indices):
        return self.__COLORS[indices]

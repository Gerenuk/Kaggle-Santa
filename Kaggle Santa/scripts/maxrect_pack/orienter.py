from maxrect_pack.rect import DIM, make_rect


class Orienter:
    def __init__(self, base_rect):
        self.base_rect = base_rect
        self.x, self.y = base_rect[DIM]

    def get_fitting(self, free_rect):
        frx, fry = free_rect[DIM]
        a, b = self.x, self.y
        if a <= frx and b <= fry:
            yield make_rect((0, a), (0, b))
        if b <= frx and a <= fry:
            yield make_rect((0, b), (0, a))

    @staticmethod
    def orient_all(rects):
        return list(map(Orienter, rects))

from maxrect_pack.rect import Rectangle


class Orienter:
    def __init__(self, base_rect):
        self.base_rect = base_rect
        self.x, self.y = base_rect.dim

    def get_fitting(self, free_rect):
        frx, fry = free_rect.dim
        a, b = self.x, self.y
        if a <= frx and b <= fry:
            yield Rectangle((0, a), (0, b))
        if b <= frx and a <= fry:
            yield Rectangle((0, b), (0, a))

    @staticmethod
    def orient_all(rects):
        return list(map(Orienter, rects))

from maxrect_pack.rect import DIM, make_rect3d


class Orienter3D:
    def __init__(self, base_rect):
        self.base_rect = base_rect
        self.x, self.y, self.z = sorted(self.base_rect.coor)

    def __repr__(self):
        return "[[{}, {}, {}]]".format(self.x, self.y, self.z)

    def __hash__(self):
        return id(self)

    def get_fitting(self, free_rect):
        frx, fry = free_rect[DIM]

        for a, b, c in [(self.x, self.y, self.z), (self.x, self.z, self.y), (self.y, self.z, self.x)]:
            smaller_fitted = False
            if a <= frx and b <= fry:
                yield make_rect3d((0, a), (0, b), c, self.base_rect.id)
                smaller_fitted = True
            if b <= frx and a <= fry:
                yield make_rect3d((0, b), (0, a), c, self.base_rect.id)
                smaller_fitted = True
            if not smaller_fitted:
                break

    @staticmethod
    def orient_all(cubes):
        return list(map(Orienter3D, cubes))

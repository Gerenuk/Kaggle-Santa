from maxrect_pack.rect import Rectangle
from msilib.schema import Property


class Orienter3D:
    def __init__(self, base_rect):
        self.base_rect = base_rect
        self.x, self.y, self.z = sorted(self.base_rect.coor)

    def __repr__(self):
        return "[[{}, {}, {}]]".format(self.x, self.y, self.z)

    def get_fitting(self, free_rect):
        frx, fry = free_rect.dim

        for a, b in [(self.x, self.y), (self.x, self.z), (self.y, self.z)]:
            smaller_fitted = False
            if a <= frx and b <= fry:
                yield Rectangle((0, a), (0, b))
                smaller_fitted = True
            if b <= frx and a <= fry:
                yield Rectangle((0, b), (0, a))
                smaller_fitted = True
            if not smaller_fitted:
                break

    @staticmethod
    def orient_all(cubes):
        return list(map(Orienter3D, cubes))

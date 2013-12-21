from maxrect_layer.rect3d import Rectangle3D


class Orienter3D:
    def __init__(self, base_rect):
        self.base_rect = base_rect
        self.x, self.y, self.z = sorted(self.base_rect.coor)

    def __repr__(self):
        return "[[{}, {}, {}]]".format(self.x, self.y, self.z)

    def __hash__(self):
        return id(self)

    def get_fitting(self, free_rect):
        frx, fry = free_rect.dim

        for a, b, c in [(self.x, self.y, self.z), (self.x, self.z, self.y), (self.y, self.z, self.x)]:
            smaller_fitted = False
            if a <= frx and b <= fry:
                yield Rectangle3D((0, a), (0, b), c)
                smaller_fitted = True
            if b <= frx and a <= fry:
                yield Rectangle3D((0, b), (0, a), c)
                smaller_fitted = True
            if not smaller_fitted:
                break

    @staticmethod
    def orient_all(cubes):
        return list(map(Orienter3D, cubes))

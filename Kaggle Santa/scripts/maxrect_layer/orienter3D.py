from maxrect_pack.rect import Rectangle


class Orienter3D:
    def __init__(self, base_rect):
        self.base_rect = base_rect

    def __iter__(self):
        x, y, z = self.base_rect.coor
        yield Rectangle(0, 0, x, y)
        yield Rectangle(0, 0, y, x)
        yield Rectangle(0, 0, x, z)
        yield Rectangle(0, 0, z, x)
        yield Rectangle(0, 0, y, z)
        yield Rectangle(0, 0, z, y)

    @staticmethod
    def orient_all(cubes):
        return list(map(Orienter3D, cubes))

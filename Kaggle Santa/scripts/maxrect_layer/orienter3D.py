from maxrect_pack.rect import Rectangle


class Orienter3D:
    def __init__(self, base_rect):
        self.base_rect = base_rect

    def __iter__(self):
        x, y, z = self.base_rect.coor
        return iter([Rectangle((0, x), (0, y)),
                    Rectangle((0, y), (0, x)),
                    Rectangle((0, x), (0, z)),
                    Rectangle((0, z), (0, x)),
                    Rectangle((0, y), (0, z)),
                    Rectangle((0, z), (0, y))])

    @staticmethod
    def orient_all(cubes):
        return list(map(Orienter3D, cubes))

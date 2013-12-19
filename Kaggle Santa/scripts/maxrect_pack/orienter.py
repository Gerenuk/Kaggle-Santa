from maxrect_pack.rect import Rectangle


class Orienter:
    def __init__(self, base_rect):
        self.base_rect = base_rect

    def __iter__(self):
        return iter([Rectangle((self.base_rect.coor[0][0], self.base_rect.coor[0][1]), (self.base_rect.coor[1][0], self.base_rect.coor[1][1])),
                     Rectangle((self.base_rect.coor[0][0], self.base_rect.coor[0][0] + self.base_rect.dim[1]), (self.base_rect.coor[1][0], self.base_rect.coor[1][0] + self.base_rect.dim[0]))])

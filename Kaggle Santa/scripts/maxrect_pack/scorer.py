from maxrect_pack.rect import COOR


class Scorer:
    def __init__(self, preview_rects_to_place):
        pass

    def __call__(self):
        pass


def scorerBSSF(rect_inside, rect_outside):
    (ix1, ix2), (iy1, iy2) = rect_inside[COOR]
    (ox1, ox2), (oy1, oy2) = rect_outside[COOR]
    iw = ix2 - ix1
    ih = iy2 - iy1
    ow = ox2 - ox1
    oh = oy2 - oy1
    assert iw <= ow
    assert ih <= oh
    return -min(ow - iw, oh - ih)

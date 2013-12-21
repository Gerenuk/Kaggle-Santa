from maxrect_pack.rect import COOR
import maxrect_pack.rect as rectangle


class NoFit(Exception):
    pass


def simple_smallest_x_fit(fit_rect, rects):
    rects = sorted(rects, key=lambda r:r[COOR][0][0])
    for r in rects:
        if rectangle.fits_inside(fit_rect, r):
            return r
    raise NoFit()

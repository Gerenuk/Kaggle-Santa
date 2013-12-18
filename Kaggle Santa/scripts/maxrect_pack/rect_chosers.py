class NoFit(Exception):
    pass


def simple_smallest_x_fit(fit_rect, rects):
    rects = sorted(rects, key=lambda r:r.coor[0][0])
    for r in rects:
        if fit_rect.fits_inside(r):
            return r
    raise NoFit()

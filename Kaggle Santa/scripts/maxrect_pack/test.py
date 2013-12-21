import random

from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import make_rect
import maxrect_pack.rect as rectangle
from maxrect_pack.recthelper import random_rects


random.seed(3)

WIDTH = 20
HEIGHT = 20


if __name__ == '__main__':
    rects_free = make_rect((1, WIDTH), (1, HEIGHT))
    rects_cut = random_rects(WIDTH, HEIGHT, 4, 4, 3)

    for rc in rects_cut:
        new_rects_free = []
        for rf in rects_free:
            if rectangle.overlap(rc, rf):
                new_rects = rf.cut_off(rc)
                if new_rects:
                    new_rects_free.extend(new_rects)
            else:
                new_rects_free.append(rf)
        rects_free = new_rects_free

    plotrects(*(rects_cut + rects_free), random_color=[0] * len(rects_cut) + [1] * len(rects_free), area_w=WIDTH, area_h=HEIGHT)
    # plotrects(*(rects_cut),random_color=[0]*len(rects_cut), area_w=WIDTH, area_h=HEIGHT)

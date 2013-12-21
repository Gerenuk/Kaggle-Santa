from maxrect_pack import rect
from maxrect_pack.maxrect import MaxRect
from maxrect_pack.rect import COOR
from maxrect_pack.rect_chosers import simple_smallest_x_fit
from maxrect_pack.recthelper import random_rects


WIDTH = 20
HEIGHT = 20

if __name__ == '__main__':
    m = MaxRect(WIDTH, HEIGHT)

    rects_cut = random_rects(WIDTH, HEIGHT, 4, 4, 30)

    for r in rects_cut:
        container_rect = simple_smallest_x_fit(r, m.free_rects)
        r = rect.set_position(r, container_rect[COOR][0][0], container_rect[COOR][1][0])
        m.cut_off(r)

    m.plot()

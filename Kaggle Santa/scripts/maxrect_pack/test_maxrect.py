from maxrect_pack.maxrect import MaxRect
from maxrect_pack.recthelper import random_rects


WIDTH = 20
HEIGHT = 20

if __name__ == '__main__':
    m = MaxRect(WIDTH, HEIGHT)

    rects_cut = random_rects(WIDTH, HEIGHT, 4, 4, 3)
    for r in rects_cut:
        m.cut_off(r)

    m.plot()

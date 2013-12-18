import random

from maxrect_pack.defaults import DEFAULT_AREA_W, DEFAULT_AREA_H, \
    DEFAULT_RANDOM_NUM
from maxrect_pack.rect import Rectangle


def random_rects(area_w=DEFAULT_AREA_W, area_h=DEFAULT_AREA_H, max_width=DEFAULT_AREA_W, max_height=DEFAULT_AREA_H, num=DEFAULT_RANDOM_NUM):
    result = []
    for _ in range(num):
        while 1:
            x1, x2 = sorted((random.randint(1, area_w), random.randint(1, area_w)))
            if 0 < x2 - x1 <= max_width:
                break
        while 1:
            y1, y2 = sorted((random.randint(1, area_h), random.randint(1, area_h)))
            if 0 < y2 - y1 <= max_height:
                break
        result.append(Rectangle(x1, y1, x2, y2))
    return result

import random
from maxrect.defaults import DEFAULT_AREA_W, DEFAULT_AREA_H, DEFAULT_RANDOM_NUM, \
    SEED
from maxrect.rect import Rectangle


def random_rects(area_w=DEFAULT_AREA_W, area_h=DEFAULT_AREA_H, num=DEFAULT_RANDOM_NUM):
    result=[]
    random.seed(SEED)
    for _ in range(num):
        while 1:
            x1=random.randint(1,area_w)
            x2=random.randint(1,area_w)
            if x1<x2:
                break
        while 1:
            y1=random.randint(1,area_h)
            y2=random.randint(1,area_h)
            if y1<y2:
                break
        result.append(Rectangle(x1,y1,x2,y2))
    return result
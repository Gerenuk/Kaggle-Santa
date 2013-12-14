from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import Rectangle


if __name__ == '__main__':
    rect=Rectangle(1,1,5,5)
    rect_cut=Rectangle(4,0,8,6)
    cuts=rect.cut_rect(rect_cut)
    plotrects(rect, rect_cut, *cuts, random_color=[0,0]+[1]*len(cuts))
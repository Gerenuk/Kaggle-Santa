from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import Rectangle


class MaxRect:
    def __init__(self, w, h):
        self.width=w
        self.height=h
        self.free_rects=[Rectangle(0, 0, w, h)]

    def plot(self):
        plotrects(*self.free_rects, area_w=self.width, area_h=self.height)
        
    def cut_rect(self, rect):
        new_free_rects=[]
        for rf in self.free_rects:
            if rect.overlap(rf):
                new_rects=rf.cut_rect(rect)
                if new_rects:
                    new_free_rects.extend(new_rects)
            else:
                new_free_rects.append(rf)
        self.free_rects=new_free_rects

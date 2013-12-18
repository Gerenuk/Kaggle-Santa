import itertools
import reprlib

from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import Rectangle


class MaxRect:
    def __init__(self, width, height, free_rects=None):
        self.width = width
        self.height = height

        if free_rects is None:
            free_rects = [Rectangle(0, 0, width, height)]

        self.free_rects = free_rects

    def __repr__(self):
        return "Maxrect({} free; {})".format(len(self.free_rects), reprlib.repr(self.free_rects))

    def plot(self):
        plotrects(*self.free_rects, area_w=self.width, area_h=self.height)

    def cut_rect(self, rect):
        new_free_rects = []
        for rf in self.free_rects:
            if rect.overlap(rf):
                new_rects = rf.cut_rect(rect)
                if new_rects:
                    new_free_rects.extend(new_rects)
            else:
                new_free_rects.append(rf)
        self.free_rects = new_free_rects

        self._merge_wrapped_rect()

    def _merge_wrapped_rect(self):
        keep_rect = []
        for check_rect in self.free_rects:
            for outside_rect in self.free_rects:
                if check_rect is outside_rect:
                    continue
                if check_rect.is_inside(outside_rect):
                    keep_rect.append(False)
                    break
            else:
                keep_rect.append(True)
        self.free_rects = list(itertools.compress(self.free_rects, keep_rect))

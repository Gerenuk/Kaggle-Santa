import itertools
import reprlib

from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import Rectangle
from collections import deque


class MaxRect:
    def __init__(self, width, height, free_rects=None):
        self.width = width
        self.height = height

        if free_rects is None:
            free_rects = deque([Rectangle((0, width), (0, height))])

        self.free_rects = free_rects

    def __repr__(self):
        return "Maxrect({} free; {})".format(len(self.free_rects), reprlib.repr(self.free_rects))

    def plot(self):
        plotrects(*self.free_rects, area_w=self.width, area_h=self.height)

    def cut_off(self, rect):
        new_free_rects = deque()
        for rf in self.free_rects:
            if rf.overlap(rect):
                active, *cuts = rf.get_cuts(rect)
                if active:
                    new_free_rects.extend([rf.cut_off(rect, cut_type) for cut_type in cuts])
            else:
                new_free_rects.append(rf)
        self.free_rects = new_free_rects

        self.free_rects = self._merge_wrapped_rect(self.free_rects)

    @staticmethod
    def _merge_wrapped_rect(rects_to_merge):
        keep_rect = []
        for check_rect in rects_to_merge:
            for outside_rect in rects_to_merge:
                if check_rect is outside_rect:
                    continue
                if check_rect.is_inside(outside_rect):
                    keep_rect.append(False)
                    break
            else:
                keep_rect.append(True)
        return list(itertools.compress(rects_to_merge, keep_rect))

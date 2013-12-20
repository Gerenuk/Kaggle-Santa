from collections import deque, defaultdict
import itertools
import reprlib

from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import Rectangle


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

        to_merge_dict = defaultdict(deque)
        for rf in self.free_rects:
            if rf.overlap(rect):
                active, *cuts = rf.get_cuts(rect)
                if active:
                    for cut_type in cuts:
                        chopped_rect = rf.cut_off(rect, cut_type)
                        to_merge_dict[cut_type].append(chopped_rect)
                else:
                    if len(cuts) == 1:  # len>2 only when corners touching
                        to_merge_dict[cuts[0]].append(rf)
                    else:
                        new_free_rects.append(rf)
            else:
                new_free_rects.append(rf)

        for _cut, rects in to_merge_dict.items():
            new_free_rects.extend(self._merge_wrapped_rect(rects))

        self.free_rects = new_free_rects

    @staticmethod
    def _merge_wrapped_rect(rects_to_merge):
        keep_rect = deque()
        for check_rect in rects_to_merge:
            for outside_rect in rects_to_merge:
                if check_rect is outside_rect:
                    continue
                if check_rect.is_inside(outside_rect):
                    keep_rect.append(False)
                    break
            else:
                keep_rect.append(True)
        result = list(itertools.compress(rects_to_merge, keep_rect))
        # print("Merged {} of {} rectangles".format(len(rects_to_merge) - len(result), len(rects_to_merge)))
        return result

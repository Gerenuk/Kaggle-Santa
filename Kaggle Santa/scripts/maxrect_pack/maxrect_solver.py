import reprlib

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.plotrect import plotrects
from maxrect_pack.positioner import position, scorerBSSF


class MaxRectSolver:
    def __init__(self, width, height, rects_to_place):
        self.width = width
        self.height = height
        self.maxrect = MaxRect(width, height)
        self.rects_to_place = rects_to_place

        self.placed_rects = []

    def __repr__(self):
        # return "MaxRectSolver(Place {} rects into {}; {})".format(len(self.rects_to_place), self.maxrect, reprlib.repr(self.rects_to_place))
        return "MaxRectSolver({})".format(self.maxrect)

    def solve(self):
        while self.rects_to_place:
            new_rect_placed, _free_rect_used = position(self.rects_to_place, self.maxrect.free_rects, scorerBSSF)
            self.rects_to_place.remove(new_rect_placed)
            self.placed_rects.append(new_rect_placed)
            self.maxrect.cut_rect(new_rect_placed)
            # self.plot()

    def plot(self):
        plotrects(*(self.placed_rects + self.maxrect.free_rects), random_color=[0] * len(self.placed_rects) + [1] * len(self.maxrect.free_rects), area_w=self.width, area_h=self.height)

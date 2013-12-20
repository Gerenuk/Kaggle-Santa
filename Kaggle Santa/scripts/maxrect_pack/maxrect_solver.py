import itertools
from collections import deque

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.plotrect import plotrects
from maxrect_pack.positioner import NoFit

LOWER_BOUND = 0


class StopFit(Exception):
    pass


class MaxRectSolver:
    def __init__(self, width, height, rects_to_place, positioner, priority_pick=None):
        self.width = width
        self.height = height
        self.maxrect = MaxRect(width, height)
        self.positioner = positioner
        self.priority_pick = priority_pick
        self.rects_to_place = rects_to_place

        self.placed_rects = deque()

    def __repr__(self):
        # return "MaxRectSolver(Place {} rects into {}; {})".format(len(self.rects_to_place), self.maxrect, reprlib.repr(self.rects_to_place))
        return "MaxRectSolver({})".format(self.maxrect)

    def solve(self):
        rects_to_place = self.rects_to_place[:self.priority_pick]
        rects_to_place_rest = self.rects_to_place[self.priority_pick:]

        try:
            while rects_to_place:
                new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position(rects_to_place, self.maxrect.free_rects)
                rects_to_place.remove(rect_orientation_chosen)
                self.place_rect(new_rect_placed)
                self.maxrect.cut_off(new_rect_placed)
        except NoFit:
            self.rects_to_place = rects_to_place + rects_to_place_rest
            raise NoFit("Could place priority rects with {} left-overs".format(len(rects_to_place)))

        assert not rects_to_place, "Left-over: {}".format(len(rects_to_place))

        if rects_to_place_rest:
            try:
                rects_to_place = iter(rects_to_place_rest)
                for rect_to_place in rects_to_place:
                    new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position([rect_to_place], self.maxrect.free_rects)
                    self.place_rect(new_rect_placed)
                    self.maxrect.cut_off(new_rect_placed)
            except NoFit:
                self.rects_to_place = list(rects_to_place)
                print("Partly solved with packing density {:.0%}".format(self.packing_density()))
                return self.rects_to_place

        rects_to_place = list(rects_to_place)
        assert not rects_to_place, "Left-over: {}".format(len(rects_to_place))

        self.rects_to_place = []
        print("All solved with packing density {:.0%}".format(self.packing_density()))
        return []

    def place_rect(self, rect):
        assert all(LOWER_BOUND <= x <= self.width for x in itertools.chain.from_iterable(rect.coor)), "Rectangle {} outside Maxrect boundary".format(rect)
        self.placed_rects.append(rect)
        # print("Placed rects {}".format(len(self.placed_rects)))

    def packing_density(self):
        return sum(r.area() for r in self.placed_rects) / (self.width * self.height)

    def plot(self, plot_free_rect=False):
        rects_to_plot = list(self.placed_rects)
        random_color = [0] * len(self.placed_rects)

        if plot_free_rect:
            rects_to_plot.extend(self.maxrect.free_rects)
            random_color.extend([1] * len(self.maxrect.free_rects))

        plotrects(*rects_to_plot, random_color=random_color, area_w=self.width, area_h=self.height)

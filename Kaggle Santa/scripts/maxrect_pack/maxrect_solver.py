import itertools
from collections import deque

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.plotrect import plotrects

LOWER_BOUND = 0


class NoFit(Exception):
    pass


class MaxRectSolver:
    def __init__(self, width, height, positioner, priority_pick=None):
        self.width = width
        self.height = height
        self.maxrect = MaxRect(width, height)
        self.positioner = positioner
        self.priority_pick = priority_pick

        self.placed_rects = deque()

    def __repr__(self):
        return "MaxRectSolver({})".format(self.maxrect)

    def solve(self, rects_to_place):
        rects_to_place_prio = rects_to_place[:self.priority_pick]
        rects_to_place_rest = rects_to_place[self.priority_pick:]

        #------------------------------------------------------------- Place all
        while rects_to_place_prio:
            # print("Maxfree {}, To place {}".format(len(self.maxrect.free_rects), len(rects_to_place)))
            new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position(rects_to_place_prio, self.maxrect.free_rects)
            if new_rect_placed is None:
                raise NoFit("Could place priority rects with {} left-overs".format(len(rects_to_place_prio)))
            rects_to_place_prio.remove(rect_orientation_chosen)
            self.place_rect(new_rect_placed)
            self.maxrect.cut_off(new_rect_placed)

        if not rects_to_place_rest:
            return []

        rects_to_place = iter(rects_to_place_rest)
        #------------------------------ Place as many single consecutive as you can
        for rect_to_place in rects_to_place:
            new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position([rect_to_place], self.maxrect.free_rects)
            if new_rect_placed is None:
                print("Partly solved with packing density {:.0%}".format(self.packing_density()))
                return list(rects_to_place)  # resolve rest

            self.place_rect(new_rect_placed)
            self.maxrect.cut_off(new_rect_placed)

        print("All solved with packing density {:.0%}".format(self.packing_density()))
        return []

    def place_rect(self, rect):
        assert all(LOWER_BOUND <= x <= self.width for x in itertools.chain.from_iterable(rect.coor)), "Rectangle {} outside Maxrect boundary".format(rect)
        self.placed_rects.append(rect)
        # print("Placed rects {}".format(len(self.placed_rects)))

    def packing_density(self):
        return sum(r.area for r in self.placed_rects) / (self.width * self.height)

    def plot(self, plot_free_rect=False):
        rects_to_plot = list(self.placed_rects)
        random_color = [0] * len(self.placed_rects)

        if plot_free_rect:
            rects_to_plot.extend(self.maxrect.free_rects)
            random_color.extend([1] * len(self.maxrect.free_rects))

        plotrects(*rects_to_plot, random_color=random_color, area_w=self.width, area_h=self.height)

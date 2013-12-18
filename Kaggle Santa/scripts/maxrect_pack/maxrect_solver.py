import itertools
import reprlib

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.plotrect import plotrects
from maxrect_pack.positioner import NoFit


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

        self.placed_rects = []

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
                self.placed_rects.append(new_rect_placed)
                self.maxrect.cut_rect(new_rect_placed)
                # self.plot()
        except NoFit:
            self.rects_to_place = rects_to_place + rects_to_place_rest
            raise NoFit("No more fit with {} rects left-over".format(len(rects_to_place)))

        assert not rects_to_place, "Left-over: {}".format(len(rects_to_place))

        if rects_to_place_rest:
            try:
                rects_to_place = iter(rects_to_place_rest)
                for rect_to_place in rects_to_place:
                    new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position([rect_to_place], self.maxrect.free_rects)
                    self.placed_rects.append(new_rect_placed)
                    self.maxrect.cut_rect(new_rect_placed)
            except NoFit:
                self.rects_to_place = list(rects_to_place)
                print("Partly solved with packing density {:.0%}".format(self.packing_density()))
                raise StopFit("No more fit in second phase with {} rects left-over".format(len(self.rects_to_place)))

        rects_to_place = list(rects_to_place)
        self.rects_to_place = rects_to_place
        assert not rects_to_place, "Left-over: {}".format(len(rects_to_place))
        print("All solved with packing density {:.0%}".format(self.packing_density()))

    def packing_density(self):
        return sum(r.area() for r in self.placed_rects) / (self.width * self.height)

    def plot(self, plot_free_rect=False):
        rects_to_plot = list(self.placed_rects)
        random_color = [0] * len(self.placed_rects)

        if plot_free_rect:
            rects_to_plot.extend(self.maxrect.free_rects)
            random_color.extend([1] * len(self.maxrect.free_rects))

        plotrects(*rects_to_plot, random_color=random_color, area_w=self.width, area_h=self.height)

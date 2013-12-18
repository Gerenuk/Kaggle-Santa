import reprlib

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.plotrect import plotrects
from maxrect_pack.positioner import NoFit


class MaxRectSolver:
    def __init__(self, width, height, rects_to_place, positioner, orienter):
        self.width = width
        self.height = height
        self.maxrect = MaxRect(width, height)
        self.positioner = positioner
        self.rects_to_place = [orienter(r) for r in rects_to_place]

        self.placed_rects = []

    def __repr__(self):
        # return "MaxRectSolver(Place {} rects into {}; {})".format(len(self.rects_to_place), self.maxrect, reprlib.repr(self.rects_to_place))
        return "MaxRectSolver({})".format(self.maxrect)

    def solve(self):
        try:
            while self.rects_to_place:
                new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position(self.rects_to_place, self.maxrect.free_rects)
                self.rects_to_place.remove(rect_orientation_chosen)
                self.placed_rects.append(new_rect_placed)
                self.maxrect.cut_rect(new_rect_placed)
                # self.plot()
        except NoFit:
            print("No more fit with {} rects left-over".format(len(self.rects_to_place)))
            return
        print("All solved with packing density {:.0%}".format(sum(r.area() for r in self.placed_rects) / (self.width * self.height)))

    def plot(self, plot_free_rect=False):
        rects_to_plot = list(self.placed_rects)
        random_color = [0] * len(self.placed_rects)

        if plot_free_rect:
            rects_to_plot.extend(self.maxrect.free_rects)
            random_color.extend([1] * len(self.maxrect.free_rects))

        plotrects(*rects_to_plot, random_color=random_color, area_w=self.width, area_h=self.height)

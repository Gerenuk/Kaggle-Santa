import itertools

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.placer import Placer, TO_PLACE_RECT, FREE_RECT, TO_PLACE
from maxrect_pack.plotrect import plotrects
from maxrect_pack.rect import COOR, DEPTH
import maxrect_pack.rect as rectangle


LOWER_BOUND = 0


class NoFit(Exception):
    pass


class MaxRectSolver:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.placed_rects = []

    def __repr__(self):
        return "MaxRectSolver({})".format(self.positioner)

    @property
    def depth(self):
        assert self.placed_rects
        return max(r[DEPTH] for r in self.placed_rects)

    def solve(self, rects_to_place, start_index, scorer, priority_pick=None, presorter_key=None):
        len_rects_to_place = len(rects_to_place)

        rects_to_place_prio = rects_to_place[start_index:start_index + priority_pick]
        start_index_rest = start_index + priority_pick

        if presorter_key is not None:
            rects_to_place_prio.sort(key=presorter_key)

        maxrect = MaxRect(self.width, self.height)
        placer = Placer(maxrect.free_rects, rects_to_place_prio, scorer)
        while placer.rects_to_place:
            next_placement = placer.get_best()
            if next_placement is None:
                raise NoFit("Could place priority rects with {} left-overs".format(len(placer.rects_to_place)))
            new_placed_rect = next_placement[TO_PLACE_RECT]
            new_placed_rect = rectangle.set_position(new_placed_rect, next_placement[FREE_RECT][COOR][0][0], next_placement[FREE_RECT][COOR][1][0])
            self._place_rect(new_placed_rect)

            new_free_rects, removed_free_rects = maxrect.cut_off(new_placed_rect)
            placer.remove(removed_free_rects, next_placement[TO_PLACE])
            placer.insert(new_free_rects)

        for index in range(start_index_rest, len_rects_to_place):
            rect_to_place = rects_to_place[index]
            next_placement = placer.get_best_for(rect_to_place)
            if next_placement is None:
                print("Partly solved with packing density {:.0%}".format(self.packing_density()))
                return index  # resolve rest; do not prepend here or it will be slow
            new_placed_rect = next_placement[TO_PLACE_RECT]
            new_placed_rect = rectangle.set_position(new_placed_rect, next_placement[FREE_RECT][COOR][0][0], next_placement[FREE_RECT][COOR][1][0])
            self._place_rect(new_placed_rect)

            new_free_rects, removed_free_rects = maxrect.cut_off(new_placed_rect)
            placer.remove(removed_free_rects, None)
            placer.insert(new_free_rects)

        print("All solved with packing density {:.0%}".format(self.packing_density()))
        return index

    def _place_rect(self, rect):
        assert all(LOWER_BOUND <= x <= self.width for x in itertools.chain.from_iterable(rect[COOR])), "Rectangle {} outside Maxrect boundary".format(rect)
        self.placed_rects.append(rect)
        # print("Placed rects {}".format(len(self.placed_rects)))

    def packing_density(self):
        return sum(rectangle.area(r) for r in self.placed_rects) / (self.width * self.height)

    def plot(self):
        rects_to_plot = list(self.placed_rects)
        random_color = [0] * len(self.placed_rects)

        plotrects(*rects_to_plot, random_color=random_color, area_w=self.width, area_h=self.height)

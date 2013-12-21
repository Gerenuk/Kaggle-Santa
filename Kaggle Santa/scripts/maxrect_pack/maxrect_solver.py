from collections import deque
import itertools

from maxrect_pack.maxrect import MaxRect
from maxrect_pack.placer import Placer
from maxrect_pack.plotrect import plotrects


LOWER_BOUND = 0


class NoFit(Exception):
    pass


class MaxRectSolver:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.placed_rects = deque()

    def __repr__(self):
        return "MaxRectSolver({})".format(self.positioner)

    def solve(self, rects_to_place, scorer, priority_pick=None):
        rects_to_place_prio = rects_to_place[:priority_pick]
        rects_to_place_rest = rects_to_place[priority_pick:] if priority_pick is not None else []

        maxrect = MaxRect(self.width, self.height)
        placer = Placer(maxrect.free_rects, rects_to_place_prio, scorer)
        while placer.rects_to_place:
            # print("PR", len(placer.rects_to_place), "FR", len(placer.free_rects))
            next_placement = placer.get_best()
            if next_placement is None:
                raise NoFit("Could place priority rects with {} left-overs".format(len(placer.rects_to_place)))
            new_placed_rect = next_placement.to_place_rect
            new_placed_rect.set_position(next_placement.free_rect.coor[0][0], next_placement.free_rect.coor[1][0])
            self.place_rect(new_placed_rect)

            new_free_rects, removed_free_rects = maxrect.cut_off(new_placed_rect)
            placer.remove(removed_free_rects, next_placement.to_place)
            placer.insert(new_free_rects)

        if rects_to_place_rest:
            rects_to_place_rest_iter = iter(rects_to_place_rest)
            for rect_to_place in rects_to_place_rest_iter:
                next_placement = placer.get_best_for(rect_to_place)
                if next_placement is None:
                    print("Partly solved with packing density {:.0%}".format(self.packing_density()))
                    return list(rects_to_place_rest_iter)  # resolve rest
                new_placed_rect = next_placement.to_place_rect
                new_placed_rect.set_position(next_placement.free_rect.coor[0][0], next_placement.free_rect.coor[1][0])
                self.place_rect(new_placed_rect)

                new_free_rects, removed_free_rects = maxrect.cut_off(new_placed_rect)
                placer.remove(removed_free_rects, None)
                placer.insert(new_free_rects)

        print("All solved with packing density {:.0%}".format(self.packing_density()))
        return []

        #------------------------------------------------------------- Place all
#         while rects_to_place_prio:
#             # print("Maxfree {}, To place {}".format(len(self.maxrect.free_rects), len(rects_to_place)))
#             new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position(rects_to_place_prio, self.maxrect.free_rects)
#             if new_rect_placed is None:
#                 raise NoFit("Could place priority rects with {} left-overs".format(len(rects_to_place_prio)))
#             rects_to_place_prio.remove(rect_orientation_chosen)
#             self.place_rect(new_rect_placed)
#             self.maxrect.cut_off(new_rect_placed)
#
#         if not rects_to_place_rest:
#             print("All solved with packing density {:.0%}".format(self.packing_density()))
#             return []
#
#         rects_to_place = iter(rects_to_place_rest)
#         #------------------------------ Place as many single consecutive as you can
#         for rect_to_place in rects_to_place:
#             new_rect_placed, rect_orientation_chosen, _free_rect_used = self.positioner.get_best_position([rect_to_place], self.maxrect.free_rects)
#             if new_rect_placed is None:
#                 print("Partly solved with packing density {:.0%}".format(self.packing_density()))
#                 return list(rects_to_place)  # resolve rest
#
#             self.place_rect(new_rect_placed)
#             self.maxrect.cut_off(new_rect_placed)
#
#         print("All solved with packing density {:.0%}".format(self.packing_density()))
#         return []

    def place_rect(self, rect):
        assert all(LOWER_BOUND <= x <= self.width for x in itertools.chain.from_iterable(rect.coor)), "Rectangle {} outside Maxrect boundary".format(rect)
        self.placed_rects.append(rect)
        # print("Placed rects {}".format(len(self.placed_rects)))

    def packing_density(self):
        return sum(r.area for r in self.placed_rects) / (self.width * self.height)

    def plot(self):
        rects_to_plot = list(self.placed_rects)
        random_color = [0] * len(self.placed_rects)

        plotrects(*rects_to_plot, random_color=random_color, area_w=self.width, area_h=self.height)

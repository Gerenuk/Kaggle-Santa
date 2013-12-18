import itertools
import reprlib


class NoFit(Exception):
    pass


class Positioner:
    def __init__(self, scorer, use_num_top_rect_to_place=1):
        self.scorer = scorer
        self.use_num_top_rect_to_place = use_num_top_rect_to_place

    def get_best_position(self, rect_orientations_to_place, free_rects):
        assert rect_orientations_to_place

        rects_to_place_iter = iter(rect_orientations_to_place)

        cur_rects_to_place = list(itertools.islice(rects_to_place_iter, self.use_num_top_rect_to_place))

        best_score = float("-inf")
        best_free_rect = None
        best_rect_orientation_to_place = None
        best_rect_to_place = None

        while 1:
            for rect_orientation_to_place in cur_rects_to_place:
                for free_rect in free_rects:
                    for rect_to_place in rect_orientation_to_place:
                        if rect_to_place.fits_inside(free_rect):
                            score = self.scorer(rect_to_place, free_rect)
                            if score >= best_score:
                                best_score = score
                                best_free_rect = free_rect
                                rect_to_place.set_position(free_rect.coor[0][0], free_rect.coor[1][0])
                                best_rect_orientation_to_place = rect_orientation_to_place
                                best_rect_to_place = rect_to_place

            if best_rect_to_place is not None:
                break

            try:
                cur_rects_to_place.append(next(rects_to_place_iter))
            except StopIteration:
                raise NoFit("No more rectangles that could fit")

        assert best_rect_to_place is not None
        return (best_rect_to_place, best_rect_orientation_to_place, best_free_rect)


def scorerBSSF(rect_inside, rect_outside):
    (ix1, ix2), (iy1, iy2) = rect_inside.coor
    (ox1, ox2), (oy1, oy2) = rect_outside.coor
    iw = ix2 - ix1
    ih = iy2 - iy1
    ow = ox2 - ox1
    oh = oy2 - oy1
    assert iw <= ow
    assert ih <= oh
    return -min(ow - iw, oh - ih)

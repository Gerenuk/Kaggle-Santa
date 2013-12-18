import itertools
import reprlib


def position(rects_to_place, free_rects, scorer):
    best_score = float("-inf")
    best_free_rect = None
    best_rect_to_place = None
    for rect_to_place in rects_to_place:
        for free_rect in free_rects:
            if rect_to_place.fits_inside(free_rect):
                score = scorer(rect_to_place, free_rect)
                if score >= best_score:
                    best_score = score
                    best_free_rect = free_rect
                    rect_to_place.set_position(free_rect.coor[0][0], free_rect.coor[1][0])
                    best_rect_to_place = rect_to_place

    assert best_rect_to_place is not None
    return (best_rect_to_place, best_free_rect)


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

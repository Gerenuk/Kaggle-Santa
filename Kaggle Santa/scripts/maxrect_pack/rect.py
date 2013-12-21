CUT_TYPES = [(0, 0), (0, 1), (1, 0), (1, 1)]


COOR = 0
DIM = 1


def make_rect(x12, y12):
    return ((x12, y12), (x12[1] - x12[0], y12[1] - y12[0]))


def make_rect3d(x12, y12, height):
    return ((x12, y12), (x12[1] - x12[0], y12[1] - y12[0]), height)


def set_position(rect, x, y):
    return make_rect((x, x + rect[DIM][0]), (y, y + rect[DIM][1]))


def get_cuts(self, rect):
    """
    returns all valid cut (i.e. these cuts dont chop off all the rectangle)
    assumes an overlap is given
    return [1, (coorid_cut, coor_high)] or [0, <touchingcuts>] 
    """
    touching_coor = []
    for coorid_cut, cut_high in CUT_TYPES:
        if self[COOR][coorid_cut][1 - cut_high] == rect[COOR][coorid_cut][cut_high]:
            touching_coor.append((coorid_cut, cut_high))
    if touching_coor:
        return [0] + touching_coor

    result = [1]  # marker for non touching cuts
    for coorid_cut, coor_high in CUT_TYPES:
        coor_cut = rect[COOR][coorid_cut][coor_high]
        selfcoor = self[COOR][coorid_cut]
        assert (coor_high and coor_cut >= selfcoor[0]) or (not coor_high and coor_cut <= selfcoor[1]), "get_cuts() found no rectangle overlap for {} and {}".format(self, rect)

        rectcoor2 = rect[COOR][1 - coorid_cut]
        selfcoor2 = self[COOR][1 - coorid_cut]
        if selfcoor2[1] <= rectcoor2[0] or rectcoor2[1] <= selfcoor2[0]:  # missed sideways in second coordinate; for a valid program only the equality should be possible if overlap already checked
            continue

        if ((coor_high and coor_cut < selfcoor[1]) or
            (not coor_high and coor_cut > selfcoor[0])):
                result.append((coorid_cut, coor_high))

    return result


def overlap(self, rect):
    """
    touching edges (and corners) also count as overlap
    """
    return not (rect[COOR][0][1] < self[COOR][0][0] or
                self[COOR][0][1] < rect[COOR][0][0] or
                rect[COOR][1][1] < self[COOR][1][0] or
                self[COOR][1][1] < rect[COOR][1][0])


def cut_off(self, rect, cut_type):
    """
    performs no overlap checks. be sure the overlap is given.
    """
    coorid_cut, cut_high = cut_type
    coor_cut = rect[COOR][coorid_cut][cut_high]

    assert self[COOR][coorid_cut][0] < coor_cut < self[COOR][coorid_cut][1], "Cut not inside rectangle for rectangle {} and {} for cuttype {}".format(self, rect, cut_type)
    assert rect[COOR][1 - coorid_cut][1] > self[COOR][1 - coorid_cut][0], "Cut missed rectangle sideways for rectangle {} and {} for cuttype {}".format(self, rect, cut_type)
    assert rect[COOR][1 - coorid_cut][0] < self[COOR][1 - coorid_cut][1], "Cut missed rectangle sideways for rectangle {} and {} for cuttype {}".format(self, rect, cut_type)

    if cut_high:
        if coorid_cut:
            return make_rect(self[COOR][0], (coor_cut, self[COOR][1][1]))
        else:
            return make_rect((coor_cut, self[COOR][0][1]), self[COOR][1])
    else:
        if coorid_cut:
            return make_rect(self[COOR][0], (self[COOR][1][0], coor_cut))
        else:
            return make_rect((self[COOR][0][0], coor_cut), self[COOR][1])


def area(self):
    return self[DIM][0] * self[DIM][1]


def fits_inside(self, rect):
    return self[DIM][0] <= rect[DIM][0] and self[DIM][1] <= rect[DIM][1]


def is_inside(self, rect):
    return (self[COOR][0][0] >= rect[COOR][0][0] and
            self[COOR][0][1] <= rect[COOR][0][1] and
            self[COOR][1][0] >= rect[COOR][1][0] and
            self[COOR][1][1] <= rect[COOR][1][1])

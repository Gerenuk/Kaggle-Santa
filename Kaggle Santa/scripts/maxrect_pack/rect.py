CUT_TYPES = [(0, 0), (0, 1), (1, 0), (1, 1)]


class Rectangle:
    __slots__ = ["coor", "dim"]

    def __init__(self, x12, y12):
        assert x12[0] < x12[1]
        assert y12[0] < y12[1]
        self.coor = (x12, y12)
        self.dim = (x12[1] - x12[0], y12[1] - y12[0])  # for performance reasons

    def __repr__(self):
        return "[{},{} | {},{}]".format(self.coor[0][0], self.coor[1][0], self.coor[0][1], self.coor[1][1])

    def overlap(self, rect):
        """
        touching edges (and corners) also count as overlap
        """
        return not (rect.coor[0][1] < self.coor[0][0] or
                    self.coor[0][1] < rect.coor[0][0] or
                    rect.coor[1][1] < self.coor[1][0] or
                    self.coor[1][1] < rect.coor[1][0])

    def get_cuts(self, rect):
        """
        returns all valid cut (i.e. these cuts dont chop off all the rectangle)
        assumes an overlap is given
        return [1, (coorid_cut, coor_high)] or [0, <touchingcuts>] 
        """
        touching_coor = []
        for coorid_cut, cut_high in CUT_TYPES:
            if self.coor[coorid_cut][1 - cut_high] == rect.coor[coorid_cut][cut_high]:
                touching_coor.append((coorid_cut, cut_high))
        if touching_coor:
            return [0] + touching_coor

        result = [1]  # marker for non touching cuts
        for coorid_cut, coor_high in CUT_TYPES:
            coor_cut = rect.coor[coorid_cut][coor_high]
            selfcoor = self.coor[coorid_cut]
            assert (coor_high and coor_cut >= selfcoor[0]) or (not coor_high and coor_cut <= selfcoor[1]), "get_cuts() found no rectangle overlap for {} and {}".format(self, rect)

            rectcoor2 = rect.coor[1 - coorid_cut]
            selfcoor2 = self.coor[1 - coorid_cut]
            if selfcoor2[1] <= rectcoor2[0] or rectcoor2[1] <= selfcoor2[0]:  # missed sideways in second coordinate; for a valid program only the equality should be possible if overlap already checked
                continue

            if ((coor_high and coor_cut < selfcoor[1]) or
                (not coor_high and coor_cut > selfcoor[0])):
                    result.append((coorid_cut, coor_high))

        return result

    def cut_off(self, rect, cut_type):
        """
        performs no overlap checks. be sure the overlap is given.
        """
        coorid_cut, cut_high = cut_type
        coor_cut = rect.coor[coorid_cut][cut_high]

        assert self.coor[coorid_cut][0] < coor_cut < self.coor[coorid_cut][1], "Cut not inside rectangle for rectangle {} and {} for cuttype {}".format(self, rect, cut_type)
        assert rect.coor[1 - coorid_cut][1] > self.coor[1 - coorid_cut][0], "Cut missed rectangle sideways for rectangle {} and {} for cuttype {}".format(self, rect, cut_type)
        assert rect.coor[1 - coorid_cut][0] < self.coor[1 - coorid_cut][1], "Cut missed rectangle sideways for rectangle {} and {} for cuttype {}".format(self, rect, cut_type)

        if cut_high:
            if coorid_cut:
                return Rectangle(self.coor[0], (coor_cut, self.coor[1][1]))
            else:
                return Rectangle((coor_cut, self.coor[0][1]), self.coor[1])
        else:
            if coorid_cut:
                return Rectangle(self.coor[0], (self.coor[1][0], coor_cut))
            else:
                return Rectangle((self.coor[0][0], coor_cut), self.coor[1])

    @property
    def area(self):
        return self.dim[0] * self.dim[1]

    def set_position(self, x, y):
        self.coor = ((x, x + self.dim[0]), (y, y + self.dim[1]))

    def fits_inside(self, rect):
        return self.dim[0] <= rect.dim[0] and self.dim[1] <= rect.dim[1]

    def is_inside(self, rect):
        return (self.coor[0][0] >= rect.coor[0][0] and
                self.coor[0][1] <= rect.coor[0][1] and
                self.coor[1][0] >= rect.coor[1][0] and
                self.coor[1][1] <= rect.coor[1][1])

class Positioner:
    def __init__(self, scorer, subsample_to_place=None):
        self.scorer = scorer
        self.subsample_to_place = subsample_to_place

    def get_best_position(self, rect_orientations_to_place, free_rects):
        assert rect_orientations_to_place
        assert free_rects

        best_score = float("-inf")
        best_free_rect = None
        best_rect_to_place = None
        best_rect_orientation_to_place = None

        fitting_rects = self._get_fitting(rect_orientations_to_place, free_rects)
        if not fitting_rects:
            return (None, None, None)  # no rectangle fit found

        for rect_to_place, free_rect, rect_orientation_to_place in fitting_rects:
            score = self.scorer(rect_to_place, free_rect)
            if score >= best_score:
                best_score = score
                best_free_rect = free_rect
                rect_to_place.set_position(free_rect.coor[0][0], free_rect.coor[1][0])
                best_rect_orientation_to_place = rect_orientation_to_place
                best_rect_to_place = rect_to_place

        return (best_rect_to_place, best_rect_orientation_to_place, best_free_rect)

    def _get_fitting(self, rect_orientations_to_place, free_rects):
        # size sorting optimization was a bit slower than plain version

        for rect_orientation_to_place in rect_orientations_to_place:
            for free_rect in free_rects:
                for rect_to_place in rect_orientation_to_place.get_fitting(free_rect):
                    yield rect_to_place, free_rect, rect_orientation_to_place


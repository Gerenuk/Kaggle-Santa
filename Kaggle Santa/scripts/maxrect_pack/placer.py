from operator import itemgetter


class OrderedLinkedListNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_

    def edit(self, add, remove):
        pass


class EndOfList(Exception):
    pass


SCORE = 0
TO_PLACE = 1
TO_PLACE_RECT = 2
FREE_RECT = 3


class Placer:
    def __init__(self, free_rects, rects_to_place, scorer):
        self.free_rects = set(free_rects)
        self.rects_to_place = set(rects_to_place)
        self.scorer = scorer
        self.linked_list = OrderedLinkedListNode(None)

        placements = self._make_placements(free_rects, self.rects_to_place)

        head = self.linked_list
        for placement in placements:
            head.next = OrderedLinkedListNode(placement)
            head = head.next

    def __repr__(self):
        return "Placer({} free, {} to place)".format(len(self.free_rects), len(self.rects_to_place))

    def _make_placements(self, free_rects, rects_to_place, sort=True):
        placements = [(self.scorer(tp, fr), tpo, tp, fr) for fr in free_rects  # CAREFUL!!! cycling over a set introduce randomess! (ties in scorer will be split randomly)
                                                         for tpo in rects_to_place
                                                         for tp in tpo.get_fitting(fr)]
        if sort:
            placements.sort(key=itemgetter(0), reverse=True)
        return placements

    def get_best(self):
        if self.linked_list.next is None:
            return None
        return self.linked_list.next.elem

    def get_best_for(self, to_place):
        new_placements = self._make_placements(self.free_rects, [to_place], sort=False)
        if new_placements:
            return max(new_placements, key=itemgetter(0))
        else:
            return None

    def remove(self, free_rects, to_place_rect):
        self.free_rects -= set(free_rects)

        if to_place_rect is not None:
            self.rects_to_place.remove(to_place_rect)

        head = self.linked_list
        while head.next is not None:
            next_placement = head.next.elem
            if next_placement[TO_PLACE] is to_place_rect or next_placement[FREE_RECT] in free_rects:
                head.next = head.next.next
            else:
                head = head.next

    def insert(self, free_rects):
        self.free_rects |= set(free_rects)
        new_placements = self._make_placements(free_rects, self.rects_to_place)

        head = self.linked_list
        new_placements_iter = iter(new_placements)
        try:
            for placement in new_placements_iter:
                if head.next is None:
                    raise EndOfList()
                score = placement[SCORE]
                while head.next.elem[SCORE] > score:
                    head = head.next
                    if head.next is None:
                        raise EndOfList()
                head.next = OrderedLinkedListNode(placement, head.next)
                head = head.next
        except EndOfList:
            for placement in new_placements_iter:
                head.next = OrderedLinkedListNode(placement)
                head = head.next

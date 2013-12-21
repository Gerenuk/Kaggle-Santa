from collections import namedtuple
from operator import attrgetter


class OrderedLinkedListNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_

    def edit(self, add, remove):
        pass


Placement = namedtuple("Placement", "score to_place to_place_rect free_rect")


class EndOfList(Exception):
    pass


class Placer:
    def __init__(self, free_rects, rects_to_place, scorer):
        self.free_rects = set(free_rects)
        self.rects_to_place = set(rects_to_place)
        self.scorer = scorer
        self.linked_list = OrderedLinkedListNode(None)

        placements = [Placement(scorer(tp, fr), tpo, tp, fr) for fr in free_rects
                                                             for tpo in rects_to_place
                                                             for tp in tpo.get_fitting(fr)]
        placements.sort(key=attrgetter("score"), reverse=True)

        head = self.linked_list
        for placement in placements:
            head.next = OrderedLinkedListNode(placement)
            head = head.next

    def get_best(self):
        if self.linked_list.next is None:
            return None
        return self.linked_list.next.elem

    def remove(self, free_rects, to_place_rect):
        self.free_rects -= set(free_rects)
        self.rects_to_place.remove(to_place_rect)

        head = self.linked_list
        while head.next is not None:
            next_placement = head.next.elem
            if next_placement.to_place is to_place_rect or next_placement.free_rect in free_rects:
                head.next = head.next.next
            else:
                head = head.next

    def insert(self, free_rects):
        new_placements = [Placement(self.scorer(tp, fr), tpo, tp, fr) for tpo in self.rects_to_place
                                                                      for fr in free_rects
                                                                      for tp in tpo.get_fitting(fr)]
        new_placements.sort(key=attrgetter("score"), reverse=True)

        head = self.linked_list
        new_placements_iter = iter(new_placements)
        try:
            for placement in new_placements_iter:
                if head.next is None:
                    raise EndOfList()
                score = placement.score
                while head.next.elem.score > score:
                    head = head.next
                    if head.next is None:
                        raise EndOfList()
                head.next = OrderedLinkedListNode(placement, head.next)
                head = head.next
        except EndOfList:
            for placement in new_placements_iter:
                head.next = OrderedLinkedListNode(placement)
                head = head.next
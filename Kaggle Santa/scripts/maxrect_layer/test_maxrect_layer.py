import cProfile
from collections import deque

from maxrect_layer.orienter3D import Orienter3D
from maxrect_pack.maxrect_solver import MaxRectSolver, StopFit
from maxrect_pack.orienter import Orienter
from maxrect_pack.positioner import Positioner, scorerBSSF, NoFit
from maxrect_pack.recthelper import random_rects


USE_NUM_PRESENTS = 10000
WIDTH = 1000
HEIGHT = 1000


def solve_all(presents_to_place):
    layers = deque()
    priority_pick = 80
    while presents_to_place:
        new_layer = MaxRectSolver(WIDTH, HEIGHT, presents_to_place, Positioner(scorerBSSF), priority_pick=priority_pick)
        try:
            presents_to_place = new_layer.solve()
            if not presents_to_place:
                break
            layers.append(new_layer)
            print("Layer {} closed with {} rects; {} presents to place left".format(len(layers), len(new_layer.placed_rects), len(presents_to_place)))
        except NoFit:
            priority_pick -= 10
            assert priority_pick > 1
    return layers

if __name__ == '__main__':
    from load.load import Present, presents
    print("Starting")

    presents_to_place = Orienter3D.orient_all(presents()[:USE_NUM_PRESENTS])

    # layers = solve_all(presents_to_place)
    cProfile.run("layers = solve_all(presents_to_place)", sort="cumulative")

    densities = [l.packing_density() for l in layers]  # @UndefinedVariable
    print("Average layer packing: {:1%}".format(sum(densities) / len(densities)))
    # rects_to_place = random_rects(WIDTH, HEIGHT, 200, 200, 100)



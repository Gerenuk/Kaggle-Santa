import cProfile
from collections import deque

from maxrect_layer.orienter3D import Orienter3D
from maxrect_pack.maxrect_solver import MaxRectSolver, NoFit
from maxrect_pack.positioner import Positioner, scorerBSSF


PRIORITY_PICK = 80
USE_NUM_PRESENTS = 10000
WIDTH = 1000
HEIGHT = 1000


def solve_all(presents_to_place):
    layers = deque()
    priority_pick = PRIORITY_PICK
    while presents_to_place:
        new_layer = MaxRectSolver(WIDTH, HEIGHT, Positioner(scorerBSSF), priority_pick=priority_pick)
        try:
            presents_to_place = new_layer.solve(presents_to_place)
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
    pr = cProfile.Profile()
    pr.enable()
    layers = solve_all(presents_to_place)
    pr.disable()
    pr.dump_stats("test_maxrect_layer.profile")

    densities = [l.packing_density() for l in layers]  # @UndefinedVariable
    print("Average layer packing: {:1%}".format(sum(densities) / len(densities)))
    # rects_to_place = random_rects(WIDTH, HEIGHT, 200, 200, 100)



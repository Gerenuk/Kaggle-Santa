import cProfile

from config import results
from maxrect_layer.orienter3D import Orienter3D
from maxrect_pack.maxrect_solver import MaxRectSolver, NoFit
from maxrect_pack.scorer import scorerBSSF


PRIORITY_PICK = 80
USE_NUM_PRESENTS = 10000
WIDTH = 1000
HEIGHT = 1000


def solve_all(presents_to_place):
    layers = []
    priority_pick = PRIORITY_PICK
    while presents_to_place:
        new_layer = MaxRectSolver(WIDTH, HEIGHT)
        try:
            presents_to_place = new_layer.solve(presents_to_place, scorerBSSF, priority_pick)
            layers.append(new_layer)
            print("Layer {} closed with {} rects; {} presents to place left".format(len(layers), len(new_layer.placed_rects), len(presents_to_place)))
            if not presents_to_place:
                break
        except NoFit:
            priority_pick -= 10
            assert priority_pick > 1
    return layers

if __name__ == '__main__':
    from load.load import Present, presents
    print("Starting")

    presents_to_place = Orienter3D.orient_all(presents()[:USE_NUM_PRESENTS])

    pr = cProfile.Profile()
    pr.enable()
    layers = solve_all(presents_to_place)
    pr.disable()
    pr.dump_stats(results("default.profile"))

    densities = [l.packing_density() for l in layers]  # @UndefinedVariable
    print("Average layer packing: {:1%}".format(sum(densities) / len(densities)))
    # rects_to_place = random_rects(WIDTH, HEIGHT, 200, 200, 100)



from config import results, temp
from maxrect_layer.maxrect_layers import MaxrectLayers
from maxrect_layer.orienter3D import Orienter3D
from maxrect_pack.scorer import scorerBSSF


PROFILE = True
SUBMISSION_FILENAME = temp("submission.csv.gz")

PRIORITY_PICK = 0
USE_NUM_PRESENTS = None  # None for all
WIDTH = 1000
HEIGHT = 1000


if __name__ == '__main__':
    from load.load import Present, presents
    print("Starting")
    all_presents = presents()

    presents_to_place = Orienter3D.orient_all(all_presents[:USE_NUM_PRESENTS])

    maxrect_layers = MaxrectLayers(WIDTH, HEIGHT, scorerBSSF, priority_pick=PRIORITY_PICK, make_timer=True, gc_collect_cycle=1000)

    if PROFILE:
        import cProfile
        pr = cProfile.Profile()
        pr.enable()
        maxrect_layers.solve(presents_to_place)
        pr.disable()
        pr.dump_stats(results("default.profile"))
    else:
        maxrect_layers.solve(presents_to_place)

    densities = [l.packing_density() for l in maxrect_layers.layers]
    print("Average layer packing: {:1%}".format(sum(densities) / len(densities)))

    if SUBMISSION_FILENAME:
        maxrect_layers.make_submission(SUBMISSION_FILENAME)



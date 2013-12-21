import random

from maxrect_pack.maxrect_solver import MaxRectSolver
from maxrect_pack.orienter import Orienter
from maxrect_pack.recthelper import random_rects
from maxrect_pack.scorer import scorerBSSF


WIDTH = 1000
HEIGHT = 1000

if __name__ == '__main__':
    # random.seed(3)
    rects_to_place = random_rects(WIDTH, HEIGHT, 200, 200, 100)
    solver = MaxRectSolver(WIDTH, HEIGHT)
    solver.solve(Orienter.orient_all(rects_to_place), scorerBSSF, priority_pick=70)
    solver.plot()

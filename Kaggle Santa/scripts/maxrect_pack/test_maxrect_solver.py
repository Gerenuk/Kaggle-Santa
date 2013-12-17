from maxrect_pack.maxrect_solver import MaxRectSolver
from maxrect_pack.recthelper import random_rects


WIDTH=1000
HEIGHT=1000

if __name__ == '__main__':
    rects_to_place=random_rects(WIDTH, HEIGHT, 200, 200, 100)
    solver=MaxRectSolver(WIDTH,HEIGHT, rects_to_place)
    solver.solve()
    solver.plot()
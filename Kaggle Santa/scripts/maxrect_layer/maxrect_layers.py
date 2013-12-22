import csv
import gc
import gzip
import io
import webbrowser

from maxrect_pack.maxrect_solver import MaxRectSolver, NoFit
from maxrect_pack.rect import COOR, DEPTH, ID
from timer import Timer


class MaxrectLayers:
    def __init__(self, width, height, scorer, priority_pick=0, make_timer=True, gc_collect_cycle=None):
        self.width = width
        self.height = height
        self.scorer = scorer
        self.priority_pick = priority_pick
        self.layers = []
        self.layer_depth_pos = []
        self.total_depth = 0
        self.num_placed_cubes = 0
        self.make_timer = make_timer
        self.gc_collect_cycle = gc_collect_cycle

    def solve(self, presents_to_place):
        if self.make_timer:
            timer = Timer()
            num_total_presents = len(presents_to_place)
        gc_collect_count = 0
        presents_index = 0
        presents_last_index = len(presents_to_place)
        while 1:
            priority_pick = self.priority_pick
            new_layer = MaxRectSolver(self.width, self.height)
            try:
                presents_index = new_layer.solve(presents_to_place, presents_index, self.scorer, priority_pick)
                self._add_layer(new_layer)
                print("{} more presents".format(presents_last_index - presents_index))
                if presents_index == presents_last_index - 1:
                    break
            except NoFit:
                priority_pick -= 10
                assert priority_pick > 1
            if self.make_timer:
                ratio = presents_index / num_total_presents
                print("Time left: {}; End time: {}".format(timer.time_left(ratio), timer.time_end(ratio)))
        print("Solved with total depth {}".format(self.total_depth))
        if self.make_timer:
            print("Time taken: {}".format(timer.time_taken()))
        if self.gc_collect_cycle:
            gc_collect_count += 1
            if gc_collect_count == self.gc_collect_cycle:
                gc_collect_count = 0
                gc.collect()

    def _add_layer(self, layer):
        self.layers.append(layer)
        new_depth = layer.depth
        self.layer_depth_pos.append(self.total_depth)
        self.total_depth += new_depth
        self.num_placed_cubes += len(layer.placed_rects)
        print("Layer {} closed with {} cubes and height {} ({:.0f} score for 1e6 cubes)".format(len(self.layers), len(layer.placed_rects), self.total_depth, 2e6 * self.total_depth / self.num_placed_cubes))

    def make_submission(self, filename):
        cubes = []
        for layer, layer_depth_pos in zip(self.layers, self.layer_depth_pos):
            for cube in layer.placed_rects:
                x1, y1, z1 = cube[COOR][0][0] + 1, cube[COOR][1][0] + 1, layer_depth_pos + 1
                x2, y2, z2 = cube[COOR][0][1], cube[COOR][1][1], layer_depth_pos + cube[DEPTH]
                idnum = cube[ID]
                cubes.append((x1, y1, z1, x2, y2, z2, idnum))
        with gzip.open(filename, "w") as outfile:
            writer = csv.writer(io.TextIOWrapper(outfile, newline="", write_through=True))
            writer.writerow(["PresentId"] + ["{}{}".format(lett, num) for num in "12345678" for lett in "xyz"])
            for x1, y1, z1, x2, y2, z2, idnum in cubes:
                writer.writerow((idnum,
                                 x1, y1, z1,
                                 x1, y1, z2,
                                 x1, y2, z1,
                                 x1, y2, z2,
                                 x2, y1, z1,
                                 x2, y1, z2,
                                 x2, y2, z1,
                                 x2, y2, z2,
                                 ))
        print("Submission file {} created with {} cubes".format(filename, len(cubes)))
        webbrowser.open_new_tab("http://www.kaggle.com/c/packing-santas-sleigh/submissions/attach")

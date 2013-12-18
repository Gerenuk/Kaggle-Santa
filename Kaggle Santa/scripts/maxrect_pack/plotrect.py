import random

from helper import get_quali_color
import matplotlib.pyplot as plt
from maxrect_pack.defaults import JITTER_SIZE, DEFAULT_ALPHA, DEFAULT_AREA_W, DEFAULT_AREA_H


def plotrects(*rects, plot_options=None, random_color=None, area_w=DEFAULT_AREA_W, area_h=DEFAULT_AREA_H, jitter=True):
    def get_jitter():
        if jitter:
            return random.random() * JITTER_SIZE
        else:
            return 0

    if plot_options is None:
        if random_color:
            plot_options = [{"fc":get_quali_color(), "alpha":DEFAULT_ALPHA} if c else {"fc":"white", "ec":"black", "lw":3} for c in random_color]
        else:
            plot_options = [{"fc":get_quali_color(), "alpha":DEFAULT_ALPHA} for _ in rects]

    for rect, plot_option in zip(rects, plot_options):
        x = rect.coor[0][0]
        y = rect.coor[1][0]
        w = rect.coor[0][1] - x
        h = rect.coor[1][1] - y
        plt.gca().add_patch(plt.Rectangle((x + get_jitter(), y + get_jitter()), w + get_jitter(), h + get_jitter(), **plot_option))

    plt.xlim([0, area_w])
    plt.ylim([0, area_h])
    plt.axes().set_aspect("equal")
    plt.show()

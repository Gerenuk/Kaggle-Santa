from maxrect.plotrect import plotrects
from maxrect.rect import Rectangle


MAXRECT_PLOT_OPTIONS={"fc":"yellow","ec":"black", "alpha":0.1}


class MaxRect:
    def __init__(self, w, h):
        self.width=w
        self.height=h
        self.rects=[Rectangle(0, 0, w, h, plot_options=MAXRECT_PLOT_OPTIONS)]

    def plot(self):
        plotrects(self.rects, self.width, self.height)
        
        
if __name__ == '__main__':
    m=MaxRect(10,10)
    m.plot()
from maxrect_pack.rect import Rectangle


class Rectangle3D(Rectangle):
    __slots__ = ["height"]

    def __init__(self, x12, y12, height):
        Rectangle.__init__(self, x12, y12)
        self.height = height

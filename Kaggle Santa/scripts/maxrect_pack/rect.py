class NoCut(Exception):
    pass

class Rectangle:
    __slots__=["coor", "plot_options"]
    def __init__(self, x1, y1, x2, y2):
        assert x1<x2
        assert y1<y2
        self.coor=((x1, x2), (y1, y2))
        
    def overlap(self, rect):
        return (not(rect.x2<=self.x1 or self.x1<=rect.x2) and
                not(rect.y2<=self.y1 or self.y1<=rect.y2))
        
    def cut_rect(self, rect):
        result=[]
        for coorid1, take_high in [(0,0),(0,1),(1,0),(1,1)]:
            rect_cut=self.cut(rect, coorid1, take_high)
            if rect_cut is not None:
                result.append(rect_cut)
        return result
    
    def cut(self, rect, coorid1, take_high, check_coor1=True, check_coor2=True):
        coor1=rect.coor[coorid1][take_high]
        coor2_0=rect.coor[1-coorid1][0]
        coor2_1=rect.coor[1-coorid1][1]
        assert coor2_0<coor2_1
        selfcoor1=self.coor[coorid1]
        selfcoor2=self.coor[1-coorid1]
        if (check_coor1 and
            ((coor1<=selfcoor1[0] and take_high) or
             (coor1>=selfcoor1[1] and not take_high))
            ):
            raise NoCut()
        if (check_coor2 and
            (coor2_1<=selfcoor2[0] or coor2_0>=selfcoor2[1])
            ):
            raise NoCut()
        if coor1<=selfcoor1[0] and not take_high:
            return None
        if coor1>=selfcoor1[1] and take_high:
            return None
        if take_high:
            newcoor1_0=coor1
            newcoor1_1=selfcoor1[1]
        else:
            newcoor1_0=selfcoor1[0]
            newcoor1_1=coor1
        newcoor2_0=selfcoor2[0]
        newcoor2_1=selfcoor2[1]
        if coorid1==0:
            return Rectangle(newcoor1_0, newcoor2_0, newcoor1_1, newcoor2_1)
        else:
            return Rectangle(newcoor2_0, newcoor1_0, newcoor2_1, newcoor1_1)

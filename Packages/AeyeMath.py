class AeyeMath():
    def __init__(self) -> None:
        pass

    def calculate_area(self,x1, y1, x2, y2, x3, y3, x4, y4):

        area1 =  abs((x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3))
        area2 =  abs((x1 - x4) * (y3 - y4) - (x3 - x4) * (y1 - y4))
        area = area1 + area2
        return area
    
    def calculate_hand_area(self,vertices):

        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1]
            area -= vertices[j][0] * vertices[i][1]
        area = abs(area) / 2.0
        return area
    
    def find_middle_pos(self,ObjX1,ObjY1,ObjX2,ObjY2):

        X = ( ObjX1 + ObjX2 ) /2
        Y = ( ObjY1 + ObjY2 ) /2

        return X,Y
    
EYE_MATH = AeyeMath()
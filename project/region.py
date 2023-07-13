# imports
import point
import math
class region():
    # Initialization method of region
    def __init__(self,center:point.point,radius:float) -> None:
        self.center = center
        self.radius = radius
    
    # Checks if point lies in region
    def pointInRegion(self,queryPoint:point) -> bool:
        return math.sqrt((queryPoint.X-self.center.X)**2+(queryPoint.Y-self.center.Y)**2) <= self.radius
    
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
        #compute euclidean distance between center of region and point
        dist = math.sqrt(math.pow(queryPoint.X-self.center.X, 2)+math.pow(queryPoint.Y-self.center.Y, 2))
        return dist <= self.radius
    
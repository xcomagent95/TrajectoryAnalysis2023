# imports
import point
class trajectory():
    # Initialization method of trajectory with an unique id
    def __init__(self,number, points = None, unique_id = None) -> None:
        self.number = number
        self.unique_id = unique_id
        self.points = [] if points is None else points


    def __repr__(self) -> str:
        # Nice printing of trajectory
        resultString = 'Trajectory with number: ' + str(self.number) + ' and points '
        for p in self.points:
            resultString += str(p) + ' '
        return resultString

    # Adds a point to the list of points of the trajectory
    def addPoint(self,p:point) -> None:
        self.points.append(p)

    # Returns the number of points in the trajectory
    def __len__(self) -> int:
        return len(self.points)

    # Returns the point at the given index
    def __getitem__(self, index: int) -> point:
        return self.points[index]

    # Helper function to get points if needed 
    def getPoints(self) -> list:
        return self.points
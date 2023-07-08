# imports
import point
class trajectory():
    # Initialization method of trajectory with an unique id
    def __init__(self,number, points = [], unique_id = None) -> None:
        self.number = number
        self.points = points
        self.unique_id = unique_id

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
    def __getitem__(self, index: int):
        return self.points[index]
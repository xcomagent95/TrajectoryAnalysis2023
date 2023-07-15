# imports
import unittest
import trajectory
import point
import region
import utils
import functions_template as functions


class DouglasPeuckerTest(unittest.TestCase):
    def test1(self):
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        res_points = d.getPoints()
        res_pojnts_array = []
        for p in res_points:
            res_pojnts_array.append([p.X, p.Y])
        self.assertEqual(res_pojnts_array, [[1, 1], [4, 4]])

    def test2(self):
        traj_points = [
            [0.0, 0.0],
            [3.0, 8.0],
            [5.0, 2.0],
            [5.0, 4.0],
            [6.0, 20.0],
            [6.4, 15.5],
            [7.0, 25.0],
            [9.1, 16.9],
            [10.0, 10.0],
            [11.0, 5.5],
            [17.3, 3.2],
            [27.8, 0.1],
        ]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 1)
        res_points = d.getPoints()
        res_pojnts_array = []
        for p in res_points:
            res_pojnts_array.append([p.X, p.Y])
        self.assertEqual(
            res_pojnts_array,
            [[0.0, 0.0], [3.0, 8.0], [5.0, 2.0], [7.0, 25.0], [11.0, 5.5], [27.8, 0.1]],
        )

    def test3(self):
        traj_points = [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 2.0),
            (3.0, 1.0),
            (4.0, 0.0),
            (5.0, 1.0),
            (6.0, 2.0),
            (7.0, 1.0),
            (8.0, 0.0),
        ]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 1)
        res_points = d.getPoints()
        res_pojnts_array = []
        for p in res_points:
            res_pojnts_array.append([p.X, p.Y])
        self.assertEqual(
            res_pojnts_array,
            [[0.0, 0.0], [2.0, 2.0], [4.0, 0.0], [6.0, 2.0], [8.0, 0.0]]
        )
    #Edgecase Testing
    def test4(self):
        t = trajectory.trajectory(1, points=[])
        d = functions.douglasPeucker(t, 1)
        self.assertEqual(d,t)

    def test5(self):
        traj_points = [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 2.0),
            (3.0, 1.0),
            (4.0, 0.0),
            (5.0, 1.0),
            (6.0, 2.0),
            (7.0, 1.0),
            (8.0, 0.0),
        ]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        self.assertRaises(ValueError, functions.douglasPeucker, traj, -1)

    def test6(self):
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        self.assertIsInstance(d, trajectory.trajectory)

    def test7(self):
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        for p in d.getPoints():
            self.assertIsInstance(p, point.point)



class SlidingWindowTest(unittest.TestCase):
    pass

class solveQueryWithoutRTree(unittest.TestCase): 
    
    def test1(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        queryRegion = region.region(point.point(0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)
        
        foundTrajectories = functions.solveQueryWithoutRTree(queryRegion, listOfTrajectories)
        
        self.assertEqual(len(foundTrajectories), 5)
        
        self.assertEqual(any(x.number == 43 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 45 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 50 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 71 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 83 for x in foundTrajectories), True)


if __name__ == "__main__":
    unittest.main()

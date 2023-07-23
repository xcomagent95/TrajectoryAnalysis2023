# imports
from utils import segmentTrajectory
import datetime
import math
import unittest
import trajectory
import point
import region
import utils
import rtree
import functions_template as functions

class DouglasPeuckerTest(unittest.TestCase):
    def testPointRemoval(self): 
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

    def testSimplifocationA(self): 
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
            [[0.0, 0.0], [3.0, 8.0], [5.0, 2.0], [
                7.0, 25.0], [11.0, 5.5], [27.8, 0.1]],
        )

    def testSimplifocationB(self): 
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

    # Edgecase Testing
    def testEmptyTrajectory(self): 
        t = trajectory.trajectory(1, points=[])
        d = functions.douglasPeucker(t, 1)
        self.assertEqual(d, t)

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

    def testOutputObjectClassTraj(self):
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        self.assertIsInstance(d, trajectory.trajectory)

    def testOutputObjectClassPoint(self): 
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        for p in d.getPoints():
            self.assertIsInstance(p, point.point)


class DynamicTimeWarpingTest(unittest.TestCase):
    def testDTWDistance(self):
        # Define the trajectory data
        first_trajectoryTest = [
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            # Add more points if needed
        ]
        traj0 = trajectory.trajectory(1, points=[point.point(
            p[0], p[1], idx) for idx, p in enumerate(first_trajectoryTest)])

        second_trajectoryTest = [
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            # Add more points if needed
        ]
        traj1 = trajectory.trajectory(1, points=[point.point(
            p[0], p[1], idx) for idx, p in enumerate(second_trajectoryTest)])

        # Calculate the expected distance
        expected_distance = sum(math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)
                                for p0, p1 in zip(first_trajectoryTest, second_trajectoryTest))

        # Call the dynamicTimeWarping function
        actual_distance = functions.dynamicTimeWarping(traj0, traj1)

        # Assert the result
        self.assertAlmostEqual(actual_distance, expected_distance, places=6)

class SlidingWindowTest(unittest.TestCase):

    def testLengthZero(self):   # fails as traj with 0 points is not created
        points = None
        traj = trajectory.trajectory(1, points=points)
        epsilon = 1
        self.assertEqual(functions.slidingWindow(traj, epsilon).getPoints(),[])


    def testLengthOne(self):
        # build trajectory
        traj_points = [[1, 1]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        epsilon = 1
        self.assertEqual(functions.slidingWindow(traj, epsilon), traj)

    def testLengthTwo(self):
        # build trajectory
        traj_points = [[1, 1], [2, 2]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        epsilon = 1
        self.assertEqual(functions.slidingWindow(traj, epsilon), traj)
        # traj = [[0,0],[1,1]]
        # epsilon = 1
        self.assertEqual(functions.slidingWindow(traj, epsilon), traj)

    def testEpsilonNegativ(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        traj = listOfTrajectories[0]
        epsilon = -1
        self.assertRaises(ValueError, functions.slidingWindow, traj, epsilon)

    def testEpsilon0(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        traj = listOfTrajectories[0]
        epsilon = 0
        self.assertRaises(ValueError, functions.slidingWindow, traj, epsilon)

    def testIfCorrect(self):
        points = [
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            # Add more points if needed
        ]
        traj = trajectory.trajectory(1, points=[point.point(
            p[0], p[1], idx) for idx, p in enumerate(points)])

        controlPoints = [
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            (0.0014788576577, 0.0037183030576),
            # Add more points if needed    # switch to correct trajectory
        ]
        controlTraj = trajectory.trajectory(1, points=[point.point(
            p[0], p[1], idx) for idx, p in enumerate(controlPoints)])
        epsilon = 0
        
        self.assertRaises(ValueError, functions.slidingWindow, traj, epsilon)


class solveQueryWithoutRTree(unittest.TestCase):
    def testExamplaryQuery(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        queryRegion = region.region(point.point(
            0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)

        foundTrajectories = functions.solveQueryWithoutRTree(
            queryRegion, listOfTrajectories)
        self.assertEqual(len(foundTrajectories), 5)

        self.assertEqual(any(x.number == 43 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 45 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 50 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 71 for x in foundTrajectories), True)
        self.assertEqual(any(x.number == 83 for x in foundTrajectories), True)
        
    def testEmptyTrajectoryList(self):
        listOfTrajectories = []
        queryRegion = region.region(point.point(0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)
        self.assertRaises(ValueError, functions.solveQueryWithoutRTree, queryRegion, listOfTrajectories)
            
    def testMalformedRegion(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        queryRegion = region.region(point.point(0.0012601754558545508, 0.0027251228043638775, 0.0), -1)
        self.assertRaises(ValueError, functions.solveQueryWithoutRTree, queryRegion, listOfTrajectories)


class minimlaBoundingBox(unittest.TestCase):

    def testCreationMBB(self):
        p1 = point.point(0, 0, None)
        p2 = point.point(2, 2, None)

        self.assertRaises(ValueError, rtree.mbb, p1, p1)
        self.assertRaises(ValueError, rtree.mbb, p2, p1)
        self.assertIs(type(rtree.mbb(p1, p2)), rtree.mbb)

    def testInclusionOfPointInMBB(self):
        p1 = point.point(0, 0, None)
        p2 = point.point(2, 2, None)
        mbb = rtree.mbb(p1, p2)

        p3 = point.point(1, 1, None)
        p4 = point.point(0, 1, None)
        p5 = point.point(1, 0, None)
        p6 = point.point(3, 3, None)

        self.assertEqual(mbb.isPointInMbb(p3), True)
        self.assertEqual(mbb.isPointInMbb(p4), True)
        self.assertEqual(mbb.isPointInMbb(p5), True)
        self.assertEqual(mbb.isPointInMbb(p6), False)

    def getAreaofMinimalBoundingBox(self):
        p1 = point.point(0, 0, None)
        p2 = point.point(2, 2, None)
        mbb = rtree.mbb(p1, p2)

        self.assertEqual(mbb.getArea(), 4.0)


class TestSegmentTrajectory(unittest.TestCase):

    def testSegmentTrajectorySingleSegment(self):
        # Test case with a single segment
        trajectory_input = [
            point.point(10, 20, "2000-01-01:01:14:56"),
            point.point(15, 25, "2000-01-01:01:15:52"),
            point.point(18, 22, "2000-01-01:01:16:56"),
            point.point(12, 28, "2000-01-01:01:19:01"),
            point.point(8, 24, "2000-01-01:01:19:06")
        ]
        time_threshold_in_minutes = 5

        segmented_trajectory = segmentTrajectory(
            trajectory_input, time_threshold_in_minutes)

        self.assertEqual(len(segmented_trajectory), 1)
        self.assertEqual(len(segmented_trajectory[0]), len(trajectory_input))

    def testSegmentTrajectoryMultipleSegments(self):
        # Test case with multiple segments
        trajectory_input = [
            point.point(10, 20, "2000-01-01:01:14:56"),
            point.point(15, 25, "2000-01-01:01:15:52"),
            point.point(18, 22, "2000-01-01:01:16:56"),
            point.point(12, 28, "2000-01-01:01:19:01"),
            point.point(8, 24, "2000-01-01:01:19:06")
        ]
        time_threshold_in_minutes = 2

        segmented_trajectory = segmentTrajectory(
            trajectory_input, time_threshold_in_minutes)

        self.assertEqual(len(segmented_trajectory), 2)
        self.assertEqual(len(segmented_trajectory[0]), 3)
        self.assertEqual(len(segmented_trajectory[1]), 2)

if __name__ == "__main__":
    unittest.main()

# imports
from utils import segmentTrajectory
import math
import unittest
import trajectory
import point
import region
import utils
import functions_template as functions


class DouglasPeuckerTest(unittest.TestCase):
    def test1(self):  # add better name
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

    def test2(self):  # add better name
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

    def test3(self):  # add better name
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
    def test4(self):  # add better name
        t = trajectory.trajectory(1, points=[])
        d = functions.douglasPeucker(t, 1)
        self.assertEqual(d, t)

    def test5(self):  # add better name
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

    def test6(self):  # add better name
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        self.assertIsInstance(d, trajectory.trajectory)

    def test7(self):  # add better name
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        for p in d.getPoints():
            self.assertIsInstance(p, point.point)


class DynamicTimeWarpingTest(unittest.TestCase):
    def test_dtw_distance(self):
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


# TODo:
# check if result is correct
# check correct epsilon input (0<, 1?)
#
class SlidingWindowTest(unittest.TestCase):

    def test_length0(self):   # fails as traj with 0 points is not created
        points = None
        traj = trajectory.trajectory(1, points=points)
        epsilon = 1
        self.assertEqual(functions.slidingWindow(traj, epsilon).points, [])

    def test_length1(self):
        # build trajectory
        traj_points = [[1, 1]]
        points = []
        for idx, p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))
        traj = trajectory.trajectory(1, points=points)
        epsilon = 1
        self.assertEqual(functions.slidingWindow(traj, epsilon), traj)

    def test_length2(self):
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

    def test_epsilonNegativ(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        traj = listOfTrajectories[0]
        epsilon = -1
        self.assertRaises(ValueError, functions.slidingWindow, traj, epsilon)

    def test_epsilon0(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        traj = listOfTrajectories[0]
        epsilon = 0
        self.assertRaises(ValueError, functions.slidingWindow, traj, epsilon)

    def test_ifCorrect(self):
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
        queryRegion = region.region(point.point(
            0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)
        self.assertRaises(
            ValueError, functions.solveQueryWithoutRTree, queryRegion, listOfTrajectories)

    def testMalformedRegion(self):
        listOfTrajectories = utils.importTrajectories("Trajectories")
        queryRegion = region.region(point.point(
            0.0012601754558545508, 0.0027251228043638775, 0.0), -1)
        self.assertRaises(
            ValueError, functions.solveQueryWithoutRTree, queryRegion, listOfTrajectories)


class TestSegmentTrajectory(unittest.TestCase):

    def segment_trajectory_single_segmentTest(self):
        # Test case with a single segment
        trajectory_input = [
            point(10, 20, "2000-01-01:01:14:56"),
            point(15, 25, "2000-01-01:01:15:52"),
            point(18, 22, "2000-01-01:01:16:56"),
            point(12, 28, "2000-01-01:01:19:01"),
            point(8, 24, "2000-01-01:01:19:06")
        ]
        time_threshold_in_minutes = 5

        segmented_trajectory = segmentTrajectory(
            trajectory_input, time_threshold_in_minutes)

        self.assertEqual(len(segmented_trajectory), 1)
        self.assertEqual(len(segmented_trajectory[0]), len(trajectory_input))

    def segment_trajectory_multiple_segmentsTest(self):
        # Test case with multiple segments
        trajectory_input = [
            point(10, 20, "2000-01-01:01:14:56"),
            point(15, 25, "2000-01-01:01:15:52"),
            point(18, 22, "2000-01-01:01:16:56"),
            point(12, 28, "2000-01-01:01:19:01"),
            point(8, 24, "2000-01-01:01:19:06")
        ]
        time_threshold_in_minutes = 2

        segmented_trajectory = segmentTrajectory(
            trajectory_input, time_threshold_in_minutes)

        self.assertEqual(len(segmented_trajectory), 2)
        self.assertEqual(len(segmented_trajectory[0]), 3)
        self.assertEqual(len(segmented_trajectory[1]), 2)


if __name__ == "__main__":
    unittest.main()

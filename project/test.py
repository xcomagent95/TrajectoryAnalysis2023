#imports
import unittest
import trajectory
import point
import region
import utils
import functions_template as functions

class DouglasPeuckerTest(unittest.TestCase):
    def test_intern(self):
        traj_points = [[1, 1], [2, 2], [3, 3], [4, 4]]
        points = []
        for idx,p in enumerate(traj_points):
            points.append(point.point(p[0], p[1], idx))


        traj = trajectory.trajectory(1, points=points)
        d = functions.douglasPeucker(traj, 0)
        res_points = d.getPoints()
        res_pojnts_array= []
        for p in res_points:
            res_pojnts_array.append([p.X,p.Y])
        self.assertEqual(res_pojnts_array, [[1,1],[4,4]])



if __name__ == '__main__':
    unittest.main()
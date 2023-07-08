# imports
import trajectory
import point
import region
import utils


#Todo: Test me!
#Todo: Document me!
#Todo: Verify i work correctly! (I think i do)
def douglasPeucker(traj:trajectory,epsilon) -> trajectory:
    return trajectory.trajectory(-1, douglasPeucker_intern(traj,epsilon), unique_id=f"Douglas Peucker for Trajectory {traj.number}")

def douglasPeucker_intern(traj, epsilon):
    # Base case: if trajectory only has two points, return it
    if len(traj) <= 2:
        return traj
    # Find the point with the maximum distance
    dmax = 0
    index = 0
    for i in range(1, len(traj) - 1):
        d = utils.perpendicularDistance(traj[i], traj[0], traj[-1])
        if d > dmax:
            index = i
            dmax = d
    # If max distance is greater than epsilon, recursively simplify
    if dmax > epsilon:
        # Recursive call
        recResults1 = douglasPeucker_intern(traj[:index+1], epsilon)
        recResults2 = douglasPeucker_intern(traj[index:], epsilon)
        # Build the result list
        resultList = recResults1[:-1] + recResults2
        return resultList
    else:
        return [traj[0], traj[-1]]

def slidingWindow(traj:trajectory,epsilon) -> trajectory:
    return None

def closestPairDistance(traj0:trajectory,traj1:trajectory) -> float:
    return None

def dynamicTimeWarping(traj0:trajectory,traj1:trajectory) -> float:
    return None

def solveQueryWithRTree(r:region,trajectories:list) -> list:
    return None

def solveQueryWithoutRTree(r:region,trajectories:list) -> list:
    return None
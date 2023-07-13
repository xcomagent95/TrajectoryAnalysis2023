# imports
import trajectory
import point
import region
import utils
from tqdm import tqdm
import sys
import numpy as np


def douglasPeucker(traj,epsilon):
    """Function to execute Douglas-Peucker simplification on a trajectory

     Parameters:
     traj (trajectory): Trajectory to be simplified
     epsilon (float): Distance threshold to be applied during simplification
    
     Returns:
     trajectory: Simplified trajectory
    
    """
    if len(traj) <= 2:
        return traj
    if epsilon < 0:
        raise ValueError("Epsilon must be greater than 0")
    return trajectory.trajectory(-1, douglasPeucker_intern(traj,epsilon), unique_id=f"Douglas Peucker for Trajectory {traj.number}")

def douglasPeucker_intern(traj, epsilon):
    """Function facilitating Douglas-Peucker simplification on a trajectory

     Parameters:
     traj (trajectory): Trajectory to be simplified
     epsilon (float): Distance threshold to be applied during simplification
    
     Returns:
     trajectory: Simplified trajectory
    
    """
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


#Todo: Test me!
#Todo: Document me!
#Todo: Verify i work correctly!
# I implemented this on the base of me remembering the algorithm from the lecture. So it may (or may not) be totally wrong..
#Todo: Fix me! I run way to long!
def slidingWindow(traj, epsilon, recursive=False, rec_limit=999999):
    if recursive:
        sys.setrecursionlimit(rec_limit)
        result_list = slidingWindow_recursive(traj, epsilon, 0, [])
    else:
        result_list = slidingWindow_iter(traj, epsilon)
    return trajectory.trajectory(-1, result_list, unique_id=f"Sliding Window for Trajectory {traj.number}")


def slidingWindow_recursive(traj, epsilon, start_index, result_list):
    result_list.append(traj[start_index])
    if start_index == len(traj) - 1:
        return result_list
    for end_index in range(start_index + 1, len(traj)):
        d = utils.perpendicularDistance(traj[end_index], traj[start_index], traj[end_index - 1])
        if d > epsilon:
            return slidingWindow_recursive(traj, epsilon, end_index - 1, result_list)
        elif end_index == len(traj) - 1:
            result_list.append(traj[end_index])
            return result_list

def slidingWindow_iter(traj, epsilon):
    # Initialize variables
    i = 0
    resultList = [traj[i]]

    # Loop through trajectory
    while i < len(traj) - 1:
        j = i + 1
        while j < len(traj):

            d = utils.perpendicularDistance(traj[j], traj[i], traj[j - 1])

            if d > epsilon:

                resultList.append(traj[j - 1])
                i = j - 1
                break
            elif j == len(traj) - 1:
                resultList.append(traj[j])
                i = j
            j += 1
    return resultList

def closestPairDistance(traj0,traj1) -> float:
    """Function to compute closest pair difference between two trajectories

     Parameters:
     traj0 (trajectory): First trajectory of the trajectory pair
     traj1 (trajectory): Second trajectory of the trajectory pair
    
     Returns:
     float: Closest pair distance between first and second trajectory of the trajectory pair
    
    """
    min_distance = float('inf')
    for p0 in traj0:
        for p1 in traj1:
            distance = utils.euclideanDistance(p0, p1)
            if distance < min_distance:
                min_distance = distance
    return min_distance

def dynamicTimeWarping(traj0:trajectory,traj1:trajectory) -> float:
    return None

def solveQueryWithRTree(r:region,trajectories:list) -> list:
    return None

def solveQueryWithoutRTree(r:region,trajectories:list) -> list:
    return None
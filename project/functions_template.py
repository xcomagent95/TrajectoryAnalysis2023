# imports
import trajectory
import point
import region
import utils
from tqdm import tqdm
import sys
import numpy as np


# ---------------------- 2.1) -----------------------
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
# ---------------------------------------------------

# ---------------------- 2.2) -----------------------
def slidingWindow(traj, epsilon):
    """ Wrapper Function to execute Sliding Window simplification on a trajectory
    Parameters:
    traj (trajectory): Trajectory to be simplified
    epsilon (float): Distance threshold to be applied during simplification

    Returns:
    trajectory: Simplified trajectory
    """
    if len(traj) <= 2:
        return traj
    if epsilon <= 0:
        raise ValueError("Epsilon must be greater than 0")
    result_list = slidingWindow_recursive(traj, epsilon, 0, [])
    return trajectory.trajectory(-1, result_list, unique_id=f"Sliding Window for Trajectory {traj.number}")


def slidingWindow_recursive(traj, epsilon, start_index, result_list):
    """This function is the intern function for the sliding window algorithm. It is called recursively

    Parameters:
    traj (trajectory): Trajectory to be simplified
    epsilon (float): Distance threshold to be applied during simplification
    start_index (int): Index of the point where the sliding window starts
    result_list (list): List of points that are already in the simplified trajectory

    Returns:
    trajectory: Array of points
    """
    if(epsilon <= 0):
        raise ValueError("Epsilon must be greater than 0")
    result_list.append(traj[start_index])
    if start_index == len(traj) - 1:
        return result_list
    for end_index in range(start_index + 1, len(traj)):
        d = utils.perpendicularDistance(traj[start_index], traj[end_index - 1], traj[end_index])
        if d > epsilon:
            return slidingWindow_recursive(traj, epsilon, end_index, result_list)
        elif end_index == len(traj) - 1:
            result_list.append(traj[end_index])
            return result_list
# ---------------------------------------------------

# ---------------------- 3.1.1) -----------------------
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
# -----------------------------------------------------

# ---------------------- 3.1.2) -----------------------
def dynamicTimeWarping(firstTrajectory:trajectory,secondTrajectory:trajectory) -> float:
    """Function to execute dynamic time warping on two trajectories

     Parameters: 
     firstTrajectory (trajectory): First trajectory 
     secondTrajectory (trajectory): Second trajectory
    
     Returns:
     float: dynamic time warping distance between the two trajectories
    """
    # Compute the distance matrix
    distance_matrix = [[utils.euclideanDistance(point0, point1) for point1 in secondTrajectory] for point0 in firstTrajectory]

    # Initialize the cost matrix
    cost_matrix = [[float('inf')] * len(secondTrajectory) for _ in range(len(firstTrajectory))]
    cost_matrix[0][0] = distance_matrix[0][0]

    # Compute the cost matrix
    for i in range(1, len(firstTrajectory)):
        for j in range(1, len(secondTrajectory)):
            cost_matrix[i][j] = distance_matrix[i][j] + min(cost_matrix[i-1][j], cost_matrix[i][j-1], cost_matrix[i-1][j-1])

    # Calculate the optimal path
    i, j = len(firstTrajectory) - 1, len(secondTrajectory) - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            min_cost = min(cost_matrix[i-1][j], cost_matrix[i][j-1], cost_matrix[i-1][j-1])
            if min_cost == cost_matrix[i-1][j]:
                i -= 1
            elif min_cost == cost_matrix[i][j-1]:
                j -= 1
            else:
                i -= 1
                j -= 1
        path.append((i, j))

    # Compute the distance
    dtw_distance = cost_matrix[-1][-1]

    return dtw_distance
# -----------------------------------------------------

# ---------------------- 4.1) -----------------------
def solveQueryWithRTree(r:region,trajectories:list) -> list:
    """Function to execute a region query on RTree containing trajectories

    Parameters: 
    r (region): Region for which to query trajectory 
    trajectories (list(trajectories)): List of trajectories from which to build Rtree to answer region query

    Returns:
    list(trajectories): List of trajectories returned by the region query
    
    """
    return None
# ---------------------------------------------------

# ---------------------- 4.2) -----------------------
def solveQueryWithoutRTree(r:region,trajectories:list) -> list:
    """Function to execute a region query on list containing trajectories

     Parameters: 
     r (region): Region for which to query trajectory 
     trajectories (list(trajectories)): List of trajectories from which to answer region query
    
     Returns:
     list(trajectories): List of trajectories returned by the region query
    
    """
    if not len(trajectories) > 0:
        raise ValueError("List of trajectories is empty.")
    elif r.radius <= 0:
        raise ValueError("Region is malformed.")
    result = []
    for t in trajectories: #iterate over trajectories
        for p in t.points: #iterate over points
            if r.pointInRegion(p): #Check if point lies in region
                result.append(t) #append trajectory
                break #break loop
    return result #return trajectories with point in region
# imports
import point
import region
import utils
import functions_template as functions

# Import trajectories
listOfTrajectories = utils.importTrajectories("Trajectories")
# for trajectory in listOfTrajectories:
#     for point in trajectory:
#         print(point)

# Visualize trajectories
# utils.visualizeTrajectories(listOfTrajectories)
# utils.visualizeTrajecotriesPyPlot(listOfTrajectories)

# Simplify at least one of the trajectories with Douglas Peucker and/or Sliding Window Algorithm
# douglas_peucker_simp = functions.douglasPeucker(listOfTrajectories[1], 0.00003)
# sliding_window_simp = functions.slidingWindow(listOfTrajectories[1],0.0001, recursive=False, numba=True)
# utils.visualizeTrajectories([listOfTrajectories[1], douglas_peucker_simp])
# utils.visualizeTrajectories([listOfTrajectories[1], sliding_window_simp])#

# Visualize original trajectory and its two simplifications

# Calculate the distance between at least two trajectories with Closest-Pair-Distance and/or Dynamic Time Warping

# Calculate the distance between two trajectories with Closest Pair Distance

dist_calc_with_closest_pair = functions.closestPairDistance(
    listOfTrajectories[0], listOfTrajectories[1])
print(
    f'The minimum as calculated by applying Closest Pair Distance is {dist_calc_with_closest_pair}')

# Calculate the distance between two trajectories with Dynamic Time Warping
dist_calc_with_dynamic_time_warping = functions.dynamicTimeWarping(
    listOfTrajectories[0], listOfTrajectories[1])
print(
    f'The minimum as calculated by applying Dynamic Time Warping is {dist_calc_with_dynamic_time_warping}')

# Perform Dynamic Time Warping on pairs of trajectories
for i in range(len(listOfTrajectories) - 1):
    for j in range(i + 1, len(listOfTrajectories)):
        firstTrajectory = listOfTrajectories[i]
        secondTrajectory = listOfTrajectories[j]
        dynamic_time_warping_distance = functions.dynamicTimeWarping(
            firstTrajectory, secondTrajectory)
        print(
            f"DTW distance between trajectory {i} and trajectory {j} is: {dynamic_time_warping_distance}.")

# Build R-tree with all given 62 trajectories

# Query the trajectories using the built R-tree and the region. Which trajectories lie in the given region?
# This query should return the trajectories with ids 43, 45, 50, 71, 83
queryRegion = region.region(point.point(
    0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)
# foundTrajectories = functions.solveQueryWithRTree(queryRegion, listOfTrajectories)
foundTrajectories = functions.solveQueryWithoutRTree(
    queryRegion, listOfTrajectories)
if foundTrajectories != None:
    if len(foundTrajectories) == 0:
        print("No trajectories match the query.")
    for t in foundTrajectories:
        print(t.number)

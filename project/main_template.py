# imports
import point
import region
import utils
import functions_template as functions

# Import trajectories
listOfTrajectories = utils.importTrajectories("Trajectories")
print(listOfTrajectories)

# Visualize trajectories

# Simplify at least one of the trajectories with Douglas Peucker and/or Sliding Window Algorithm

# Visualize original trajectory and its two simplifications

# Calculate the distance between at least two trajectories with Closest-Pair-Distance and/or Dynamic Time Warping

# Build R-tree with all given 62 trajectories

# Query the trajectories using the built R-tree and the region. Which trajectories lie in the given region?
# This query should return the trajectories with ids 43, 45, 50, 71, 83
queryRegion = region.region(point.point(0.0012601754558545508,0.0027251228043638775,0.0),0.00003)
foundTrajectories = functions.solveQueryWithRTree(queryRegion,listOfTrajectories)
if foundTrajectories != None:
    if len(foundTrajectories)==0:
        print("No trajectories match the query.")
    for t in foundTrajectories:
        print(t)
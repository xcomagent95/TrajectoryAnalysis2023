# imports
import point
import region
import utils
import functions_template as functions
import rtree

# Import trajectories
listOfTrajectories = utils.importTrajectories("Trajectories")
#print(utils.pointDistance(listOfTrajectories[0][0], listOfTrajectories[0][2]))

#print(listOfTrajectories[0][0])
tree = rtree.rTree()
pointA = listOfTrajectories[0][0]
pointB = listOfTrajectories[0][20]
node1 = rtree.node(pointA, root=False, leaf=True)
node2 = rtree.node(pointB, root=False, leaf=True)
root = rtree.node(rtree.calculateSmallestRegion(node1, node2), children=[node1, node2], root=True, leaf=False)
tree.root = root
tree.children = tree.root.children # GESTOPPT hier evtl noch was anpassen, damit die tree root children automtaosch die tree children snd oder auf tree children verzichten
print(tree)
print(tree.children)

#print(type(tmp.points[0]))
#print([[pt.X, pt.Y] for pt in tmp.points])
#utils.buildRTree(listOfTrajectories)

'''
counter = 0
for object in listOfTrajectories:
    counter += len(object)
'''
#print(len(listOfTrajectories[0])) # The resulting list is quiet long


# Visualize trajectories
#utils.visualizeTrajectories(listOfTrajectories)
#utils.visualizeTrajectoriesPyPlot(listOfTrajectories)

# Simplify at least one of the trajectories with Douglas Peucker and/or Sliding Window Algorithm
#douglas_peucker_simp = functions.douglasPeucker(listOfTrajectories[1], 0.00003)
#sliding_window_simp = functions.slidingWindow(listOfTrajectories[1],0.0001, recursive=False, numba=True)
#utils.visualizeTrajectories([listOfTrajectories[1], douglas_peucker_simp])
#utils.visualizeTrajectories([listOfTrajectories[1], sliding_window_simp])#

# Visualize original trajectory and its two simplifications

# Calculate the distance between at least two trajectories with Closest-Pair-Distance and/or Dynamic Time Warping

# Build R-tree with all given 62 trajectories

# Query the trajectories using the built R-tree and the region. Which trajectories lie in the given region?
# This query should return the trajectories with ids 43, 45, 50, 71, 83
queryRegion = region.region(point.point(0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)
#foundTrajectories = functions.solveQueryWithRTree(queryRegion, listOfTrajectories)
'''foundTrajectories = functions.solveQueryWithoutRTree(queryRegion, listOfTrajectories)
if foundTrajectories != None:
    if len(foundTrajectories) == 0:
        print("No trajectories match the query.")
    for t in foundTrajectories:
        print(t.number)
'''

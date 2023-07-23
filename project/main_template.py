# imports
import point
import region
import utils
import functions_template as functions
import rtree

# Import trajectories
listOfTrajectories = utils.importTrajectories("Trajectories")
#print(utils.pointDistance(listOfTrajectories[0][0], listOfTrajectories[0][2]))

tree = rtree.rTree()
#print('l.13',tree)
nodes = [rtree.node(pointX, root=False, leaf=True) for pointX in listOfTrajectories[0]]
'''root = rtree.node(value=rtree.calculateSmallestMBB(nodes[0:5]), root=True, children=nodes[0:5], leaf=False)
for i in [1,10,20,30,50]:
    nodes[i].parent = root
tree.root = root
print(tree)
print(tree.findNode2(tree.root, nodes[55]))'''
#print(nodes[0].value.lowerLeft)
tree.insertPoint(listOfTrajectories[0][0])
#print('l.16',tree)
tree.insertPoint(listOfTrajectories[0][1])
#print('------------------------------------------------------')
#print('l.18',tree)
#print('------------------------------------------------------')
tree.insertPoint(listOfTrajectories[0][10])
#print('l.20',tree)
tree.insertPoint(listOfTrajectories[0][15])
#print('l.22',tree)
tree.insertPoint(listOfTrajectories[0][20])
#print('l.24',tree)
tree.insertPoint(listOfTrajectories[0][25])
#print('l.26',tree)
tree.insertPoint(listOfTrajectories[0][26])
#print('l.37',tree)
#print('----------------------------------------------------------------------------------------------------')

tree.insertPoint(listOfTrajectories[0][27])
#print('l.39',tree)
#print('----------------------------------------------------------------------------------------------------')
tree.insertPoint(listOfTrajectories[0][28])
#print('l.42',tree)
#print('----------------------------------------------------------------------------------------------------')
tree.insertPoint(listOfTrajectories[0][29])
#print('l.44',tree)
tree.insertPoint(listOfTrajectories[0][30])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][31])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][32])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][33])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][34])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][35])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][36])
#print('l.49',tree)
tree.insertPoint(listOfTrajectories[0][37])
print('l.49',tree)
'''pointA = listOfTrajectories[0][0]
pointB = listOfTrajectories[0][20]
pointC = listOfTrajectories[0][30]
pointD = listOfTrajectories[0][40]
pointE = listOfTrajectories[0][45]
pointF = listOfTrajectories[0][50]
node1 = rtree.node(pointA, root=False, leaf=True)
node2 = rtree.node(pointB, root=False, leaf=True)
node3 = rtree.node(pointC, root=False, leaf=True)
node4 = rtree.node(pointD, root=False, leaf=True)
node5 = rtree.node(pointE, root=False, leaf=True)
node6 = rtree.node(pointF, root=False, leaf=True)
childrensList = [node1, node2, node3, node4, node5]
node7 = rtree.node(rtree.calculateSmallestMBB(childrensList), children=childrensList, root=False, leaf=False)
'''
#print(rtree.splitNode(node7, pointF))
#print(rtree.splitNode(node7, pointF))

#print(rtree.calculateSmallestMBB([node1, node2]).lowerLeft)
#print(rtree.calculateSmallestMBB(leafsList=[node1, node2]).upperRight)
#root = rtree.node(rtree.calculateSmallestRegion(node1, node2), children=[node1, node2], root=True, leaf=False)
#tree.root = root
#tree.children = tree.root.children # GESTOPPT hier evtl noch was anpassen, damit die tree root children automatisch die tree children snd oder auf tree children verzichten
#print(tree)
#print(tree.children)
#print(tree.findLeaf(root, pointC).leaf)

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

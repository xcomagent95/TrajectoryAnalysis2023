import point
import trajectory
import region
import numpy as np 
import utils
import itertools as it
import plotly.express as px # remove
import plotly.graph_objects as go # remove


class mbb: 
	def __init__(self, lowerLeft:point.point, upperRight:point.point) -> None:
		"""Constructor for minimal bounding box (mbb)

		Parameters: 
		lowerLeft (point): Point at the lower left corner of the minimal bounding box
		upperRight (point): Point at the upper right corner of the minimal bounding box
		
		Returns:
		None: 
		"""
		if(lowerLeft.X >= upperRight.X):
			raise ValueError("X coordinate of upper right corner must be greater that X coordinate of the lower left corner")
		elif(lowerLeft.Y >= upperRight.Y):
			raise ValueError("Y coordinate of upper right corner must be greater that Y coordinate of the lower left corner")

		self.lowerLeft = lowerLeft
		self.upperRight = upperRight
	
	def isPointInMbb(self, point:point.point) -> bool:
		"""Function to test if a point is inside a minimal bounding box

		Parameters: 
		point (point): point for which to test inclusion in the minimal bounding box

		Returns:
		bool: Boolean signifying inclusion of point in the minimal bounding box
		"""
		if(point.X >= self.lowerLeft.X and
			point.X <= self.upperRight.X and
			point.Y >= self.lowerLeft.Y and
			point.Y <= self.upperRight.Y):
			return True
		else:
			return False
		
	def getArea(self) -> float:
		"""Function to compute the area of a minimal bounding box

		Returns:
		float: area of the minimal bounding box
		"""
		width = self.upperRight.X - self.lowerLeft.X
		height = self.upperRight.Y - self.lowerLeft.Y
		return width * height

# Nodes have 2 - 5 children, which can be Nodes or Leafs. 
'''
'''
class node:
	# value (mbb OR point)
	# children (None OR list)
	# leaf (boolean)
	def __init__(self, value, parent=None, children=None, root:bool=False, leaf:bool=False) -> None:
		self.leaf = leaf
		self.root = root
		self.parent = parent
		self.children = children
		self.value = value

		if self.leaf == True:
			if self.children != None:
				raise ValueError("Leafs do not have any children!")
			else: 
				self.children = children
			if type(self.value) != point.point:
				raise ValueError("Leafs has to be Points not Minimal Bounding Boxes!")
			else: 
				self.value = value

def calculateSmallestMBB(leafsList:list) -> mbb:
	# Test if leafsList contains only leaf nodes. If not, it throws an error
	"""Function to calculate the minimal bounding box for a list of leafs

	Parameters: 
	leafsList (list(node)): List of nodes from which to compute a minimal bounding box

	Returns:
	mbb: Minimal bounding box of a set of leafs
	"""
	for leaf in leafsList:
		if not (isinstance(leaf, node) and leaf.leaf == True):
			raise ValueError("Here is a mistake, the calculateSmallestMBB function only takes a list of leaf nodes!")
	
	smallestMBB_lowerLeft_X = min([leaf.value.X for leaf in leafsList])
	smallestMBB_lowerLeft_Y = min([leaf.value.Y for leaf in leafsList])
	smallestMBB_upperRight_X = max([leaf.value.X for leaf in leafsList])
	smallestMBB_upperRight_Y = max([leaf.value.Y for leaf in leafsList])

	smallestMBB_lowerLeft = point.point(x=smallestMBB_lowerLeft_X, y=smallestMBB_lowerLeft_Y, timestamp=0.0)
	smallestMBB_upperRight = point.point(x=smallestMBB_upperRight_X, y=smallestMBB_upperRight_Y, timestamp=0.0)
	smallestMBB = mbb(lowerLeft=smallestMBB_lowerLeft, upperRight=smallestMBB_upperRight)
	
	return smallestMBB

# This function will be called if a node has already 5 children, but another point should be added as well and therefore the node has to be splitted
def splitNodeTo2Parts(currentNode:node, point:point.point) -> tuple:
	#minPartition = ()
	# In case an error occurs and the children list ist unequal to length 5
	if len(currentNode.children) < 5:
		raise ValueError("Here is a mistake!")
	else: 
		# Build node out of new point and add it to the children nodes list
		newNode = node(value=point, leaf=True) 
		childrensList = currentNode.children
		childrensList.append(newNode)
		
		partitionsAndAreaSizes = [] # Will contain tuples (group1, group2, total_area)

		subpartitions = it.combinations(childrensList, 3)
		for partition in subpartitions:

			mbb1 = calculateSmallestMBB(list(partition))
			mbb1_size = mbb1.getArea()

			remaining_points = [childNode for childNode in childrensList if childNode not in partition]
			mbb2 = calculateSmallestMBB(list(remaining_points))
			mbb2_size = mbb2.getArea()

			total_area = mbb1_size + mbb2_size
			partitionsAndAreaSizes.append((list(partition), remaining_points, total_area))

		minPartition = min(partitionsAndAreaSizes, key = lambda partition: partition[2])
		'''
		# FOR VISUALIZATION
		fig = px.scatter(x=[child.value.X for child in childrensList], y=[child.value.Y for child in childrensList])
		bbox1 = calculateSmallestMBB(minPartition[0])
		bbox2 = calculateSmallestMBB(minPartition[1])
		fig.add_shape(type="rect",
			x0=bbox1.lowerLeft.X, y0=bbox1.lowerLeft.Y, x1=bbox1.upperRight.X, y1=bbox1.upperRight.Y, 
		)
		fig.add_shape(type="rect",
			x0=bbox2.lowerLeft.X, y0=bbox2.lowerLeft.Y, x1=bbox2.upperRight.X, y1=bbox2.upperRight.Y, 
		)
		fig.show()
		'''
		return minPartition

class rTree:
	def __init__(self, root:node=None, children=None) -> None:
		self.root = root
		self.children = children

	def fillRTree(self, listOfTrajectories:list) -> list:
		return None

	# This function iterates down to the leaf in whose region the given point falls
	def findLeaf(self, node:node, point:point.point) -> node:
		currentNode = node
		print("l.70")
		for child in currentNode.children:
			print("l.73")
			if child.leaf == False:
				print("l.75 child.leaf == False")
				if child.value.pointInRegion(point):
					print("l.77 child.value.pointInRegion == True")
					currentNode = child
			else: 
				print("l.80 child.leaf == True")
				return currentNode
		print("l.82 for loop left")
		return currentNode

	# This function inserts a given point
	def insertPoint(self, point:point.point) -> None: # Die idee ist ein rekursiver ansatz an dieser stelle
		newNode = node(value=point, parent=None, root=False, leaf=True)
		
		# If the tree got no root so far, the inserted point becomes the root
		if self.root == None:
			newNode.root = True
			self.root = newNode

		# If root got no children so far, this is the first child
		if self.children is None: 
			# In this case, the current root node has to become a children node, a leaf
			rootThatBecomesChild = self.root
			# and a new root node gets initialized.
			newRoot = node(value=calculateSmallestMBB(leafsList=[rootThatBecomesChild, newNode]), children=[], root=True)
			# The new root node gets referenced as the tree's root.
			self.root = newRoot
			# Since the old root is now a children of the new root, the old root's parent is the new root.
			rootThatBecomesChild.parent = newRoot
			# The old root is now no root anymore.
			rootThatBecomesChild.root = False
			# Also new node, that will be added to the tree gets the root as its parent.
			newNode.parent = newRoot
			# The trees children are the old root and the newly inserted node.
			self.children.append(rootThatBecomesChild)
			self.children.append(newNode)
		
		# If the tree has already more than 1 level:
		else:
			nodeWherePointShouldBeInserted = self.findLeaf(self.root, point)
			# After finding the node where the new point fits in spatially, the point can be added as a new node to the childrens list or the current node has to be splitted
			if len(nodeWherePointShouldBeInserted.children) < 5:
				newNode.parent = nodeWherePointShouldBeInserted
				nodeWherePointShouldBeInserted.children.append(newNode) 
			else: 
				(part1, part2, total_area) = splitNodeTo2Parts(currentNode=nodeWherePointShouldBeInserted, point=point)
				# If parental node got enough space for another child node:
				if len(nodeWherePointShouldBeInserted.parent.children) < 5:
					newNodeFor1stPart = nodeWherePointShouldBeInserted
					newNodeFor1stPart.children = part1
					newNodeFor1stPart.value = calculateSmallestMBB(part1)
					for child in newNodeFor1stPart.children:
						child.parent = newNodeFor1stPart
						child.leaf = True
					
					newNodeFor2ndPart = node(value=calculateSmallestMBB(part2), parent=newNodeFor1stPart.parent, children=part2)
					for child in newNodeFor2ndPart:
						child.parent = newNodeFor2ndPart
						child.leaf = True
				
				else:
					# WHAT TO DO, IF PARENTAL NODE HAS NOT ENOUGH SPACE FOR ANOTHER CHILD NODE?
					# HOW TO NOW FIND THE CORRECT PLACE?
					pass

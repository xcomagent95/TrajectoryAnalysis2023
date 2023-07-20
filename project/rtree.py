import point
import trajectory
import region
import numpy as np 
import utils
import itertools as it
import math
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
		''' Removed exception for the reason, that to points, that are identical in the coordinates but not in timestamps are also possible
		if lowerLeft.X >= upperRight.X:
			raise ValueError("X coordinate of upper right corner must be greater than X coordinate of the lower left corner!")
		elif lowerLeft.Y >= upperRight.Y:
			raise ValueError("Y coordinate of upper right corner must be greater than Y coordinate of the lower left corner!")
		'''
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
	
	def distancePointToMbb(self, point:point.point) -> float:
		dx = max(abs(point.X - self.lowerLeft.X) - (self.upperRight.X - self.lowerLeft.X) / 2, 0)
		dy = max(abs(point.Y - self.lowerLeft.Y) - (self.upperRight.Y - self.lowerLeft.Y) / 2, 0)

		distance = math.sqrt(dx**2 + dy**2)
		return distance
		
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

	def __str__(self) -> str:
		if self.leaf == True:
			string = f"({self.value.X},{self.value.Y})"
		else: 
			string = f"({self.value})"
		return string

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

	def __str__(self) -> str:
		string = ""
		if self.root != None:
			if self.root.leaf == True:
				string += f"Root: ({self.root.value.X}, {self.root.value.Y})\n"
			else:
				string += f"Root: ({self.root.value})\n"
			if self.children != None:
				print('len list', len(self.children))
				for child in self.children:
					if child.leaf == True:
						string += f"Children: {child.value.X}, {child.value.Y}, "
		return string

	def fillRTree(self, listOfTrajectories:list) -> list:
		return None

	# This function iterates down to the leaf in whose region the given point falls
	def findNode(self, point:point.point) -> node:
		foundNode = self.root
		if foundNode.leaf:
			return foundNode
		elif foundNode.children < 5:
			return foundNode
		else:
			nodesThatAreNotLeaf = []
			nodesThatAreLeafs = []
			# First check how many leafs and non-leafs are in the level
			for child in foundNode.children:
				if isinstance(child.value, mbb):
					nodesThatAreNotLeaf.append(child)
				elif isinstance(child.value, point.point):
					nodesThatAreLeafs.append(child)
			
			# If ONLY LEAFS are in this level 
			if len(nodesThatAreNotLeaf) == 0:
				distancesFromPointToChildren = []
				for child in foundNode.children:
					distancesFromPointToChildren.append(child, (utils.calculateDistance(child.value, point)))
				nearestChild = min(distancesFromPointToChildren, key = lambda child: child[1]) # nearestChild: tuple
				return nearestChild[0]
			
			elif len(nodesThatAreLeafs) == 0:
				pass
				# to do
		
			else: 
				pass
				# to do 
				

			mbbPointFallsInto = []
			distancesFromPointToChildren = []
			for child in foundNode.children:
				if isinstance(child.value, mbb):
					if child.value.isPointInMbb(point):
						mbbPointFallsInto.append(child)
					
		#print("l.70")
		for child in currentNode.children:
			pass # TO DO: The current version won't produce a height balanced tree.... !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

			'''#print("l.73")
			if child.leaf == False:
			#	print("l.75 child.leaf == False")
				if child.value.isPointInMbb(point): # here it also has to be tested with child mbb is closest to point
			#		print("l.77 child.value.pointInRegion == True")
					currentNode = child
			else: 
			#	print("l.80 child.leaf == True")
				return currentNode'''
		#print("l.82 for loop left")
		return foundNode

	# This function inserts a given point
	def insertPoint(self, point:point.point) -> None: # Die idee ist ein rekursiver ansatz an dieser stelle
		newNode = node(value=point, parent=None, root=False, leaf=True)
		
		# If the tree got no root so far, the inserted point becomes the root
		if self.root == None:
			newNode.root = True
			self.root = newNode
			return

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
			self.children = []
			self.children.append(rootThatBecomesChild)
			self.children.append(newNode)
			return
		
		# If the tree has already more than 1 level:
		else:
			nodeToAddNewNode = self.findNode(point) # returned node can be leaf or non-leaf
			if nodeToAddNewNode.leaf:
				newNonLeafNode = node(value=calculateSmallestMBB([nodeToAddNewNode, newNode]), parent=nodeToAddNewNode.parent, children=[nodeToAddNewNode, newNode])
				nodeToAddNewNode.parent = newNonLeafNode
			else:
				pass
				# mbb has to be mofied or split performed

			# If there are less than 5 children in this level, just add the new node here
			if len(self.children) < 5:
				self.children.append(newNode)
			# Only if this level is full, go to the next level 
			else: 
				self.findNode(point) # to continue

			print(f'Children list not NONE, but {len(self.children)}')
			nodeWherePointShouldBeInserted = self.findNode(point) # mistake location
			print('l.231',len(nodeWherePointShouldBeInserted.children))
			print('nodeWherePointShouldBeInserted',nodeWherePointShouldBeInserted)
			# After finding the node where the new point fits in spatially, the point can be added as a new node to the childrens list or the current node has to be splitted
			if len(nodeWherePointShouldBeInserted.children) < 5:
				print('len < 5')
				print(newNode)

				print('child list',nodeWherePointShouldBeInserted.children)
				newNode.parent = nodeWherePointShouldBeInserted
				nodeWherePointShouldBeInserted.children.append(newNode) 
				nodeWherePointShouldBeInserted.value = calculateSmallestMBB(nodeWherePointShouldBeInserted.children)
			else: 
				print('len >= 5')
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

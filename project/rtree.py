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
		None
		"""
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
		
	'''def isMBBInMBB(self, mbb) -> bool:
		"""Function to test if a MBB is inside a minimal bounding box

		Parameters: 
		mbb: minimal bounding box: point for which to test inclusion in the minimal bounding box

		Returns:
		bool: Boolean signifying inclusion of mbb in the minimal bounding box
		"""
		if (mbb.lowerLeft.X >= self.lowerLeft.X and 
			mbb.lowerLeft.Y >= self.lowerLeft.Y and
			mbb.upperRight.X <= self.upperRight.X and
			mbb.upperRight.Y <= self.upperRight.Y):
			return True
		else:
			return False'''

	def distancePointToMbb(self, point:point.point) -> float:
		"""Calculates the distance from a given point to a minimal bounding box object.

		Parameters: 
		point (point.point): A given point
		
		Returns:
		distance (float): The distance between point and MBB object.
		"""
		dx = max(abs(point.X - self.lowerLeft.X) - (self.upperRight.X - self.lowerLeft.X) / 2, 0)
		dy = max(abs(point.Y - self.lowerLeft.Y) - (self.upperRight.Y - self.lowerLeft.Y) / 2, 0)

		distance = math.sqrt(dx**2 + dy**2)
		return distance
		
	def getArea(self) -> float:
		"""Function to compute the area of a minimal bounding box

		Returns:
		areaSize (float): area of the minimal bounding box
		"""
		width = self.upperRight.X - self.lowerLeft.X
		height = self.upperRight.Y - self.lowerLeft.Y
		areaSize = width * height
		return areaSize


class node:
	def __init__(self, value, parent=None, children=None, root:bool=False, leaf:bool=False) -> None:
		"""Constructor for nodes.

		Parameters: 
		value (point.point | mbb): A point or a mbb object.
		parent (None | node): A reference to a parent node. It is None per default.
		children (None | list[node]): A list of children nodes. It is None per default.
		root (bool): If the node is the root of a tree it is set to True. Initially it is set to False.
		leaf (bool): If the node is a leaf it is set to True. Initially it is set to False.

		Returns:
		None
		"""
		self.leaf = leaf
		self.root = root
		self.parent = parent
		if isinstance(children, list):
			if len(children) > 5:
				raise ValueError("Node can have only five children max!")
		self.children = children
		if isinstance(value, point.point):
			self.value = mbb(lowerLeft=value, upperRight=value)
		elif isinstance(value, mbb):
			self.value = value

		if self.leaf == True:
			if self.children != None:
				raise ValueError("Leafs do not have any children!")
			else: 
				self.children = children

def calculateSmallestMBB(nodeList:list) -> mbb:
	"""Function to calculate the minimal bounding box for a list of nodes.

	Parameters: 
	nodeList (list[node]): List of nodes from which to compute a minimal bounding box

	Returns:
	smallestMBB (mbb): Minimal bounding box of a set of leafs
	"""

	smallestMBB_lowerLeft_X = min([node.value.lowerLeft.X for node in nodeList])
	smallestMBB_lowerLeft_Y = min([node.value.lowerLeft.Y for node in nodeList])
	smallestMBB_upperRight_X = max([node.value.upperRight.X for node in nodeList])
	smallestMBB_upperRight_Y = max([node.value.upperRight.Y for node in nodeList])

	smallestMBB_lowerLeft = point.point(x=smallestMBB_lowerLeft_X, y=smallestMBB_lowerLeft_Y, timestamp=0.0)
	smallestMBB_upperRight = point.point(x=smallestMBB_upperRight_X, y=smallestMBB_upperRight_Y, timestamp=0.0)
	smallestMBB = mbb(lowerLeft=smallestMBB_lowerLeft, upperRight=smallestMBB_upperRight)
	
	return smallestMBB

class rTree:
	def __init__(self, root:node=None) -> None:
		"""Constructor for R-Trees.

		Parameters: 
		root (node): Contains a reference to the root node. It is initially set to None.

		Returns:
		None
		"""
		self.root = root
	
	# This function is only working properly for a height less than 3
	def __str__(self) -> str:
		"""Constructs a string that prints an rtree object, 
		but this function is not working for all kind of situations
		and was mostly used during development.

		Returns:
		string (str): A string object.
		"""
		string = ""
		if self.root != None:
			if self.root.leaf == True:
				string += f"Root: (({self.root.value.lowerLeft.X},{self.root.value.lowerLeft.Y}), ({self.root.value.upperRight.X},{self.root.value.upperRight.Y}))\n"
			else:
				string += f"Root: ({self.root})\n"
			if self.root.children != None:
				string += f"Roots children amount: {len(self.root.children)}\n"
				for child in self.root.children:
					string += f"\n Child: ({child}), Parent: ({child.parent})"
					if isinstance(child.children, list):
						string += f", amount of childs children {len(child.children)}\n"
						for childsChildren in child.children:
							string += f"Childs children: ({childsChildren}), parent: {childsChildren.parent}\n"
							
							if isinstance(child.children, list):
								string += f", amount of childs children {len(child.children)}\n"
								for childsChildren in child.children:
									string += f"Childs children: ({childsChildren}), parent: {childsChildren.parent}\n"			
		return string

	def fillRTree(self, listOfTrajectories:list) -> None:
		"""This function fills a constructed rtree object.

		Parameters: 
		listOfTrajectories (list): A list of trajectories it gets initialized by the import trajectory function from utils.py

		Returns:
		None
		"""
		for trajectory in listOfTrajectories:
			for point in trajectory:
				self.insertPoint(point)

	def findNode(self, nodeToStartFrom:node, newNode:node) -> node:
		"""Find the node where a new node should be inserted.
		This function works recursively and terminates if the starting node got only leafs as children.

		Parameters: 
		nodeToStartFrom (node): A node inside the tree where the search should start from.

		Returns:
		foundNode (node): Returns a node where the given new node should be added.
		"""
		newNodesPoint = point.point(x=newNode.value.lowerLeft.X, y=newNode.value.lowerLeft.Y, timestamp=0.0)
		foundNode = nodeToStartFrom
		# If the root is a leaf, than the newNode should be added to the root directly
		if foundNode.leaf:
			return foundNode
		# If the root nodes children are leafs and the height is 2 (root and children, that are leafs)
		elif foundNode.children[0].leaf:
			return foundNode
		# If the children's nodes are not leafs, the child that's bbox will be the less enlarged should be found.
		# The function calls itself recursively after identifying the closest node
		else:
			distancesFromPointToChildren = []
			for child in foundNode.children:
				distancesFromPointToChildren.append((child, child.value.distancePointToMbb(newNodesPoint)))
			nearestChild = min(distancesFromPointToChildren, key = lambda child: child[1]) # nearestChild: tuple
			foundNode = nearestChild[0]
			return self.findNode(nodeToStartFrom=foundNode, newNode=newNode)

	def splitNode(self, givenNode:node) -> None:
		"""This function gets called, if the given node got its 6th child. 
		Than the given node has to be split into two nodes. 
		Therefore a separation has to be done.

		Parameters: 
		givenNode (node): A node who's children should be separated.

		Returns:
		None
		"""
		if len(givenNode.children) <= 5:
			raise ValueError("Here is a mistake!")
		else: 
			# Here the subpartition with the smallest area in sum will be find
			nodesChildren = givenNode.children
			partitionsAndAreaSizes = [] # Will contain tuples (group1, group2, total_area)
			subpartitions = it.combinations(nodesChildren, 3)
			for partition in subpartitions:

				mbb1 = calculateSmallestMBB(list(partition))
				mbb1_size = mbb1.getArea()

				remaining_points = [childNode for childNode in nodesChildren if childNode not in partition]
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
			givenNode.children = minPartition[0]
			# Just for safety: newly connected child nodes get the given node as parent linked
			for child in givenNode.children:
				child.parent = givenNode
			# An mbb gets newly calculated
			givenNode.value = calculateSmallestMBB(givenNode.children)
			# A sibling node for the second part of nodes gets invented
			siblingNode = node(value=calculateSmallestMBB(minPartition[1]), children=minPartition[1], root=False, leaf=False)
			# Its newly connected child nodes get him as new parent node
			for child in siblingNode.children:
				child.parent = siblingNode
			
			# If given node is root:
			if givenNode.root:
				# A new parent node gets invented
				newParentNode = node(value=calculateSmallestMBB([givenNode, siblingNode]), children=[givenNode, siblingNode], root=False, leaf=False)
				# And the parent links get corrected
				givenNode.parent = newParentNode
				siblingNode.parent = newParentNode
				givenNode.root = False
				newParentNode.root = True
				self.root = newParentNode
			# If given node is not the tree's node
			else: 
				siblingNode.parent = givenNode.parent
				givenNode.parent.children.append(siblingNode)
				
				# If the given node's parent has 5 OR LESS children after adding a new one:
				if len(givenNode.parent.children) <= 5:
					return
				# If the given node's parent now has MORE THAN 5 children:
				else: 
					self.splitNode(givenNode=givenNode.parent)

	# This function inserts a given point
	def insertPoint(self, point:point.point) -> None: 
		"""This function inserts a given point to the rtree object.

		Parameters: 
		point (point.point): A point that should be inserted to the rtree object.

		Returns:
		None
		"""
		pointToMbb = mbb(lowerLeft=point, upperRight=point)
		newNode = node(value=pointToMbb, parent=None, root=False, leaf=True)
		
		# If the tree got no root so far, the inserted point becomes the root
		if self.root == None:
			newNode.root = True
			self.root = newNode
			return

		# If root got no children so far, this is the first child
		if self.root.children is None: 
			# In this case, the current root node has to become a children node, a leaf
			rootThatBecomesChild = self.root
			# and a new root node gets initialized.
			newRoot = node(value=calculateSmallestMBB(nodeList=[rootThatBecomesChild, newNode]), children=[rootThatBecomesChild, newNode], root=True)
			# The new root node gets referenced as the tree's root.
			self.root = newRoot
			# Since the old root is now a children of the new root, the old root's parent is the new root.
			rootThatBecomesChild.parent = newRoot
			# The old root is now no root anymore.
			rootThatBecomesChild.root = False
			# Also new node, that will be added to the tree gets the root as its parent.
			newNode.parent = newRoot
			# The trees children are the old root and the newly inserted node.
			return
		
		# If the tree has already more than 1 level:
		else:
			nodeToAddNewNode = self.findNode(self.root, newNode) # returned node can only leaf or non-leaf
			nodeToAddNewNode.children.append(newNode)
			nodeToAddNewNode.value = calculateSmallestMBB(nodeToAddNewNode.children)
			newNode.parent = nodeToAddNewNode
			# If the node has already more than 5 children, it has to be split
			if len(nodeToAddNewNode.children) > 5:
				self.splitNode(nodeToAddNewNode)
			return
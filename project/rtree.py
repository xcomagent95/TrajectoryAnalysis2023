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
		
	def isMBBInMBB(self, mbb) -> bool:
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
			return False
	

	def distanceMbbToMbb(self, theOtherMbb) -> float:
		"""
		Not done
		"""	
		return #distance

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
	# value (point OR mbb)
	# children (None OR list)
	# leaf (boolean)
	def __init__(self, value, parent=None, children=None, root:bool=False, leaf:bool=False) -> None:
		self.leaf = leaf
		self.root = root
		self.parent = parent
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
			'''			
			if type(self.value) != point.point:
				raise ValueError("Leafs has to be Points not Minimal Bounding Boxes!")
			else: 
				self.value = value
			'''

	#def __str__(self) -> str:
		#string = f"(({self.value.lowerLeft.X},{self.value.lowerLeft.Y}),({self.value.upperRight.X},{self.value.upperRight.Y}))"
		#string = f"{self} "
		#return string

def calculateSmallestMBB(nodeList:list) -> mbb:
	# Test if leafsList contains only leaf nodes. If not, it throws an error
	"""Function to calculate the minimal bounding box for a list of leafs

	Parameters: 
	nodeList (list(mbb)): List of nodes from which to compute a minimal bounding box

	Returns:
	mbb: Minimal bounding box of a set of leafs
	"""

	smallestMBB_lowerLeft_X = min([node.value.lowerLeft.X for node in nodeList])
	smallestMBB_lowerLeft_Y = min([node.value.lowerLeft.Y for node in nodeList])
	smallestMBB_upperRight_X = max([node.value.upperRight.X for node in nodeList])
	smallestMBB_upperRight_Y = max([node.value.upperRight.Y for node in nodeList])

	smallestMBB_lowerLeft = point.point(x=smallestMBB_lowerLeft_X, y=smallestMBB_lowerLeft_Y, timestamp=0.0)
	smallestMBB_upperRight = point.point(x=smallestMBB_upperRight_X, y=smallestMBB_upperRight_Y, timestamp=0.0)
	smallestMBB = mbb(lowerLeft=smallestMBB_lowerLeft, upperRight=smallestMBB_upperRight)
	
	return smallestMBB

# DEPRECATED
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
	def __init__(self, root:node=None) -> None:
		self.root = root

	def __str__(self) -> str:
		string = ""
		if self.root != None:
			if self.root.leaf == True:
				string += f"Root: (({self.root.value.lowerLeft.X},{self.root.value.lowerLeft.Y}), ({self.root.value.upperRight.X},{self.root.value.upperRight.Y}))\n"
				#string += f"Root: {self.root.value}"
			else:
				#string += f"Root: ({self.root.value})\n"
				string += f"Root: ({self.root})\n"
			#print("roots children len ", len(self.root.children))
			#print("-x-x-x- ", self.root.children)
			#for child in self.root.children: 
			#	print(child)
			#print("----len roots children type ", len(self.root.children))
			if self.root.children != None:
				string += f"Roots children amount: {len(self.root.children)}\n"
				for child in self.root.children:
					string += f"\n Child: ({child}), Parent: ({child.parent})"#, its children len: {len(child.children)}"
					#print('xxxxxxx', type(child.children))
					#print('xxxxxxx', len(child.children))
					if isinstance(child.children, list):
						string += f", amount of childs children {len(child.children)}\n"
						for childsChildren in child.children:
							string += f"Childs children: ({childsChildren}), parent: {childsChildren.parent}\n"
							
							if isinstance(child.children, list):
								string += f", amount of childs children {len(child.children)}\n"
								for childsChildren in child.children:
									string += f"Childs children: ({childsChildren}), parent: {childsChildren.parent}\n"
					
		return string

	def fillRTree(self, listOfTrajectories:list) -> list:
		return None

	def findNode2(self, nodeToStartFrom:node, newNode:node) -> node:
		newNodesPoint = point.point(x=newNode.value.lowerLeft.X, y=newNode.value.lowerLeft.Y, timestamp=0.0)
		foundNode = nodeToStartFrom
		print("found node ",foundNode)
		if foundNode.children != None:
			print("found node children len ", len(foundNode.children))
			for child in foundNode.children:
				print(child.value)
		# If the root is a leaf, than the newNode should be added to the root directly
		if foundNode.leaf:
			print("found node is leaf")
			return foundNode
		# If the root nodes children are leafs and the height is 2 (root and children, that are leafs)
		elif foundNode.children[0].leaf:
			print("found nodes children is leaf ") # HERE IS SOME ERROR
			return foundNode
		# If the childrens nodes are not leafs, the child that's bbox will be the less enlarged should be found.
		# The function calls itself recursively after identifying the closest node
		else:
			print("recursive search started")
			distancesFromPointToChildren = []
			for child in foundNode.children:
				#tmp = child.value.distancePointToMbb(newNodesPoint)
				#print(tmp)
				distancesFromPointToChildren.append((child, child.value.distancePointToMbb(newNodesPoint)))
			nearestChild = min(distancesFromPointToChildren, key = lambda child: child[1]) # nearestChild: tuple
			#print(distancesFromPointToChildren)
			foundNode = nearestChild[0]
			return self.findNode2(nodeToStartFrom=foundNode, newNode=newNode)

	# DEPRECATED
	# This function iterates down to the leaf in whose region the given point falls
	def findNode(self, newNode:node) -> node:
		newNodesPoint = point.point(x=newNode.value.lowerLeft.X, y=newNode.value.lowerLeft.Y, timestamp=0.0)
		foundNode = self.root
		# If the root is a leaf, than the newNode should be added to the root directly
		if foundNode.leaf:
			return foundNode
		
		elif foundNode.children < 5:
			return foundNode
		
		else:
			nodesThatAreNotLeaf = []
			nodesThatAreLeafs = []
			# First check how many leafs and non-leafs are in the level
			for child in foundNode.children:
				if not child.leaf:
					nodesThatAreNotLeaf.append(child)
				elif child.leaf:
					nodesThatAreLeafs.append(child)
			
			# If ONLY LEAFS are in this level 
			if len(nodesThatAreNotLeaf) == 0:
				distancesFromPointToChildren = []
				for child in foundNode.children:
					distancesFromPointToChildren.append(child, (utils.calculateDistance(child.value, newNodesPoint)))
				nearestChild = min(distancesFromPointToChildren, key = lambda child: child[1]) # nearestChild: tuple
				return nearestChild[0]
			
			# If ONLY NON LEAFS are in this level
			elif len(nodesThatAreLeafs) == 0:
				enlargement = []
				childrenThatAreNotFull = []
				for child in foundNode.children:
					if len(child.children) < 5:
						childrenThatAreNotFull.append(child)
				# Finds the child node were adding the new node produces the smallest enlargement
				if len(childrenThatAreNotFull) > 0:
					for child in childrenThatAreNotFull.children:
						enlargement.append((calculateSmallestMBB([child, newNode]) - child.value.getArea(), child))
						# to do: calculate smallestMbb between child and newNode and find the one with the smallest enlargement 
						# than do something recursive
					childWithSmallestEnlargement = min(enlargement, key = lambda child: child[0])
				if childWithSmallestEnlargement.children[0].leaf:
					pass
				# to complete
		
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
		#for child in currentNode.children:
			#pass # TO DO: The current version won't produce a height balanced tree.... !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

	def splitNode(self, givenNode:node) -> None:
		if len(givenNode.children) <= 5:
			raise ValueError("Here is a mistake!")
		else: 
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
			
			'''# If the given node's parent has less than 5 children 
			if len(givenNode.parent.children) < 5:
				# Remove all childs from one partitions from given node
				for elem in minPartition[0]:
					givenNode.children.remove(elem)
				givenNode.value = calculateSmallestMBB(givenNode.children)
				siblingNode = node(value=calculateSmallestMBB(minPartition[1]), children=minPartition[1], root=False, leaf=False)
				newParentNode = node(value=calculateSmallestMBB([givenNode, siblingNode]), children=[givenNode, siblingNode], root=False, leaf=False)
				# If given node is root:
				if givenNode.root:
					givenNode.root = False
					newParentNode.root = True
					self.root = newParentNode
			
			# If the given node's parent node has already 5 children and we move up as far as required
			else: 
				pass'''

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
				givenNodesOldParent = givenNode.parent
				givenNode.parent = newParentNode
				siblingNode.parent = newParentNode
				givenNode.root = False
				newParentNode.root = True
				self.root = newParentNode
			# If given node is not the tree's node
			else: 
				siblingNode.parent = givenNode.parent
				givenNode.parent.children.append(siblingNode)
				#newParentNode.parent = givenNodesOldParent
				#newParentNode.parent.children.append(newParentNode)
				
				# If the given node's parent has 5 OR LESS children after adding a new one:
				if len(givenNode.parent.children) <= 5:
					print("len(givenNode.parent.children) <= 5:", len(givenNode.parent.children) <= 5)
					return
				# If the given node's parent now has MORE THAN 5 children:
				else: 
					self.splitNode(givenNode=givenNode.parent)

	# This function inserts a given point
	def insertPoint(self, point:point.point) -> None: # Die idee ist ein rekursiver ansatz an dieser stelle
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
			#self.root.children = []
			#self.root.children.append(rootThatBecomesChild)
			#self.root.children.append(newNode)
			return
		
		# If the tree has already more than 1 level:
		else:
			nodeToAddNewNode = self.findNode2(self.root, newNode) # returned node can only leaf or non-leaf
			#print("+++++",self.findNode2(self.root, newNode)) # returned node can only leaf or non-leaf
			print("####", nodeToAddNewNode)
			nodeToAddNewNode.children.append(newNode)
			nodeToAddNewNode.value = calculateSmallestMBB(nodeToAddNewNode.children)
			newNode.parent = nodeToAddNewNode
			if len(nodeToAddNewNode.children) > 5:
				print("------------------------------------------------")
				print("split has to be done")
				print("------------------------------------------------")
				#splitNodeTo2Parts(nodeToAddNewNode)
				self.splitNode(nodeToAddNewNode)
			return
			# OLD:'''
			if nodeToAddNewNode.leaf:
				newNonLeafNode = node(value=calculateSmallestMBB([nodeToAddNewNode, newNode]), parent=nodeToAddNewNode.parent, children=[nodeToAddNewNode, newNode])
				nodeToAddNewNode.parent = newNonLeafNode
				newNode.parent = newNonLeafNode
			else:
				nodeToAddNewNode.children.append(newNode)
				newNode.parent = nodeToAddNewNode
				if len(nodeToAddNewNode.children) > 5:
					pass #splitNode(nodeToAddNewNode)
				# mbb has to be mofied or split performed

			# OLD:
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

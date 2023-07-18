import point
import trajectory
import region
import numpy as np 
import utils


class mbb: 
	def __init__(self, lowerLeft:point.point, upperRight:point.point) -> None:
		self.lowerLeft = lowerLeft
		self.upperRight = upperRight
	
	def isPointInMbb(self, point:point.point) -> bool:
		
		return 

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

'''
def calculateSmallestRegion(leaf1:node, leaf2:node) -> region.region:
	if not (isinstance(leaf1.value, point.point) and isinstance(leaf2.value, point.point)):
		raise ValueError("calculateSmallestRegion could also be used for two leaf nodes!")
	else: 
		distance = utils.pointDistance(leaf1.value, leaf2.value)
		centerPointX = leaf1.value.X + (leaf2.value.X - leaf1.value.X) / 2
		centerPointY = leaf1.value.Y + (leaf2.value.Y - leaf1.value.Y) / 2
		centerPoint = point.point(centerPointX, centerPointY, 0.0)
		resultRegion = region.region(center=centerPoint, radius=distance/2)
		return resultRegion
'''
def calculateSmallestMBB(leaf1:node, leaf2:node) -> mbb:
	smallestMBB_X = min(leaf1.X, leaf2.X)
	smallestMBB_Y = min(leaf1.Y, leaf2.Y)
	smallestMBB = mbb(lowerLeft=smallestMBB_X, upperRight=smallestMBB_Y)
	return smallestMBB

class rTree:
	def __init__(self, root:node=None, children=None) -> None:
		self.root = root
		self.children = children

	def fillRTree(self, listOfTrajectories:list) -> list:
		return None

	# This function will be called if a node has already 5 children, but another point should be added as well and therefore the node has to be splitted
	def splitNode(self, currentNode:node, point:point.point) -> None:
		# In case an error occurs and the children list ist unequal to length 5
		if len(currentNode.children) != 5:
			raise ValueError("Here is a mistake!")
		else: 
			distanceArray = np.zeros([5,5])
			for row in range(0,5):	
				for col in range(0,5):
					distanceArray[row][col] = utils.pointDistance(currentNode.children.value) # TO CONTINUE
					# TBC

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
			newRoot = node(value=self.calculateSmallestRegion(leaf1=rootThatBecomesChild, leaf2=newNode), children=[], root=True)
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
				self.splitNode(currentNode=nodeWherePointShouldBeInserted, point=point)

			'''
			for child in self.children:
				currentNode = child
				if currentNode.leaf == False:
					if currentNode.value.pointInRegion(point):
						return

				# Loops down until the node is found which is the parent of a leaf and the region covers the new point
				while currentNode.leaf != True:
					if isinstance(currentNode.value, region.region):
						if currentNode.value.pointInRegion(point):
							break # should break while look from line 51
					else:
						raise ValueError("Here is a mistake, one node has a Region instance as value but is no leaf!")
				# If a leaf is found we have to go back to the parent node
				if currentNode.leaf == True:	
					currentNode = currentNode.parent

				if len(self.children) < 5:
					newNode = node(value=point, parent=currentNode, root=False, leaf=True)
					self.children.append(newNode)
				else:
					self.splitNode(self, currentNode, point)
			'''
			
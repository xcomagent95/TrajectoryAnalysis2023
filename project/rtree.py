import point
import trajectory
import region
import numpy as np 
import utils
	
# Nodes have 2 - 5 children, which can be Nodes or Leafs. 
'''
'''
class node:
	# value (region OR point)
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
				raise ValueError("Leafs has to be Points not Regions!")
			else: 
				self.value = value

		'''if root == False:
			if parent == None or type(parent) != node:
				raise ValueError("This node needs a Parent node!")
			else: 
				self.parent = parent'''


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

class rTree:
	def __init__(self, root:node=None, children=None) -> None:
		self.root = root
		self.children = children

	def fillRTree(self, listOfTrajectories:list) -> list:
		return None

	# This function will be called if a node has already 5 children, but another point should be added as well and therefore the node has to be splitted
	def splitNode(self, currentNode:node, point:point.point) -> None:
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
			rootThatBecomesChild = self.root
			newRoot = node(value=self.calculateSmallestRegion(leaf1=rootThatBecomesChild, leaf2=newNode), children=[], root=True)
			self.root = newRoot
			rootThatBecomesChild.parent = newRoot
			rootThatBecomesChild.root = False
			newNode.parent = newRoot

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
			
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

		if self.leaf == True:
			if self.children != None:
				raise ValueError("Leafs do not have any children!")
			else: 
				self.children = children
			if type(self.value) != point.point:
				raise ValueError("Leafs has to be Points not Regions!")
			else: 
				self.value = value

		if root == False:
			if parent == None or type(parent) != node:
				raise ValueError("This node needs a Parent node!")
			else: 
				self.parent = parent
	
		self.value = value
		self.parent = parent
		self.children = children

class rTree:
	def __init__(self, root:node=None, children=None) -> None:
		self.root = root
		self.children = children

	def fillRTree(self, listOfTrajectories:list) -> list:
		return None

	def splitNode(self, currentNode:node, point:point.point) -> None:
		if len(currentNode.children) != 5:
			raise ValueError("Here is a mistake!")
		else: 
			distanceArray = np.zeros([5,5])
			for row in range(0,5):	
				for col in range(0,5):
					distanceArray[row][col] = utils.pointDistance(currentNode.children.value) # TO CONTINUE
			
	def calculateSmallestRegion(self, leaf1:node, leaf2:node) -> region.region:
		if not (isinstance(leaf1.value, point.point) and isinstance(leaf2.value, point.point)):
			raise ValueError("calculateSmallestRegion could also be used for two leaf nodes!")
		else: 
			distance = utils.pointDistance(leaf1.value, leaf2.value)
			centerPointX = leaf1.value.X + (leaf2.value.X - leaf1.value.X) / 2
			centerPointY = leaf1.value.Y + (leaf2.value.Y - leaf1.value.Y) / 2
			centerPoint = point.point(centerPointX, centerPointY, 0.0)
			region = region.region(center=centerPoint, radius=distance/2)
			return region


	def insertPoint(self, point:point.point) -> None:
		newNode = node(value=point, parent=currentNode, root=False, leaf=True)
		# If the tree got no root so far, the inserted point becomes the root
		if self.root == None:
			newNode.root = True
			self.root = newNode
		# If root got no children so far, this is the first child
		if self.children is None: 
			self.children = []
			newNode.parent = self.root
			self.children.append(newNode)
		
		else:
			for child in self.children:
				currentNode = child
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
			
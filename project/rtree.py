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
	def __init__(self, value, parent=None, children=None, root:bool=False, leaf:bool=True) -> None:
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
	def __init__(self) -> None:
		self.root = None
		self.children = None

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
			

	def insertPoint(self, point:point.point) -> None:
		if type(self.children) is not None: 
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
		else:
			self.children = []
			self.children.append()
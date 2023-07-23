# Trajectory Analysis 2023

### Tasks

1. Visualize (basic function): Visualize the imported trajectories. Here you can be creative. There should be at least a visualization of all trajectories imported as a set. (DONE)
   Possible add-ons could be:
   - ~~Different colors of different trajectories (feature)~~
   - Setting up a complete GUI with possibility to choose a set of trajectories to be displayed or even use the functionalities provided by the methods of the other upcoming tasks (feature) (Partially Implemented)
   - Whatever functionality you can think of... (feature)
2. Preprocessing - Data Reduction:
   - ~~Implement the Douglas-Peucker algorithm to simplify a given trajectory (basic function)~~
   - ~~Implement the Sliding-Window-Algorithm (feature)~~ (Needs to be tested)
   - ~~Visualize one original and one simplified trajectory using the implemented methods (feature)~~
   - ~~Additional Feature: Trajectory Segmentation based on predefined time difference input.~~
3. Indexing
   - Distance Measures: Implement distance measures for trajectories
     - ~~Closest-Pair-Distance (basic function)~~ (needs to be tested)
     - ~~Dynamic-Time-Warping (feature)~~
   - R-tree: Implement a R-tree for a set of trajectories. Here each point is a single spatial object and the nodes should hold a minimal number of two points/MBBs and a maximal number of 5 points/MBBs. (basic function)
4. Querying: Regard a R-query for a set of trajectories.
   - Write a method to solve the R-query using the R-tree. When one point is identified to lie in the radius, mark all other points of the trajectory as visited to be faster and don't have to refine for too many points (for this each point should know its trajectory). (basic function)
   - ~~Write a method to solve the R-query without the R-tree (i.e. by just iterating over all points). There is already an example R-query provided. If you want to test your implementation you can just use the query and the provided result there. (basic function)~~
   - Compare the time difference it takes between the two implemented methods (feature).

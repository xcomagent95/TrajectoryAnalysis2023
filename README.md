# Trajectory Analysis 2023

## 1. Overview

The Trajectory Analysis Project is a comprehensive data visualization project designed to visualize and analyze
trajectory data. Its primary focus is on analysis and study of trajectory data, providing various preprocessing
techniques, implementing distance measures, and enabling trajectory indexing for faster querying. The project aims to
offer a user-friendly interface with intuitive functionalities, which will be useful from basic to advanced users.

## 2. Tasks

1. Visualize (basic function): Visualize the imported trajectories. Here you can be creative. There should be at least a
   visualization of all trajectories imported as a set.
   Possible add-ons could be:
   - Different colors of different trajectories (feature)
   - Setting up a complete GUI with possibility to choose a set of trajectories to be displayed or even use the
     functionalities provided by the methods of the other upcoming tasks (feature)
2. Preprocessing - Data Reduction:
   - Implement the Douglas-Peucker algorithm to simplify a given trajectory (basic function)
   - Implement the Sliding-Window-Algorithm (feature)
   - Visualize one original and one simplified trajectory using the implemented methods (feature)
   - Additional Feature: Trajectory Segmentation based on predefined time difference input.
3. Indexing
   - Distance Measures: Implement distance measures for trajectories
     - Closest-Pair-Distance (basic function) (needs to be tested)
     - Dynamic-Time-Warping (feature)
   - R-tree: Implement a R-tree for a set of trajectories. Here each point is a single spatial object and the nodes
     should hold a minimal number of two points/MBBs and a maximal number of 5 points/MBBs.
4. Querying: Regard a R-query for a set of trajectories.
   - Write a method to solve the R-query using the R-tree. When one point is identified to lie in the radius, mark all
     other points of the trajectory as visited to be faster and don't have to refine for too many points (for this each
     point should know its trajectory). (feature)
   - Write a method to solve the R-query without the R-tree (i.e. by just iterating over all points). There is
     already an example R-query provided. If you want to test your implementation you can just use the query and the
     provided result there. (basic function)
   - Compare the time difference it takes between the two implemented methods (feature).

### 2.1 Visualization

Primarily used is the function visualizeTrajectories which takes a list of trajectories as input and plots them
interactively with plotly.
As a more static backup, there is the function visualizeTrajecotriesPyPlot which takes a list of trajectories as input
and plots them with matplotlib.

### 2.2 Preprocessing

#### 2.2.1 Douglas-Peucker algorithm (basic function)

This function implements the Douglas-Peucker algorithm. It simplifies a trajectory by removing points that are close to
the line segments, thus reducing the complexity
of the trajectory.

The function begins by checking the number of points in the traj. If traj contains less than or equal to 2 points, or if
epsilon is less than 0, it returns traj without any changes.

The function then calls the helper function douglasPeucker_intern which performs the actual simplification.
This function searches for the largest point distance to the line segment. If the distance is greater than epsilon,
the point is added to the simplified trajectory. If the distance is less than epsilon, the point is discarded. The
function then calls itself recursively on the two sub-trajectories to the left and right of the discarded point. The
function returns the simplified trajectory.
The function returns the simplified trajectory.

#### 2.2.2 Sliding-Window-Algorithm (feature)

This function implements the Sliding Window algorithm, another approach to simplify trajectories. It uses a "window" of
three points and removes the middle point if it is perpendicular distance to the line segment connecting the two other
points is less than a certain threshold.

The function starts by checking the length of traj. If traj contains less than or equal to 2 points, or if epsilon is
less than or equal to 0, it returns traj without any changes. If traj contains more than two points, the function calls
the helper function slidingWindow_intern which performs the actual simplification.

The helper function slidingWindow_recursive now actually simplifies the trajectory. It starts by appending the first
point of the window to the result list. Then, it slides the window along traj by increasing the end index.
For each new end point, it calculates the perpendicular distance of the previous point (the middle point in the window)
from the line segment connecting the start point and the new end point. If this distance is greater than epsilon, it
appends the previous point to the result list and calls itself recursively with the new end index as the new start
index.
If the end index reaches the end of traj, it appends the last point to the result list and returns it.
The function returns the simplified trajectory.

#### 2.2.3 Visualize one original and one simplified trajectory using the implemented methods (feature)

The function visualizeTrajectory takes a list of trajectorys as input. This is used to just create an array of the two
simplified and the on original trajectory and input it to the function.

#### 2.2.4 Additional Feature: Trajectory Segmentation based on predefined time difference input

The technique of segmenting a continuous trajectory into smaller pieces based on parameters like time intervals or
spatial properties is known as trajectory segmentation. This segmentation improves the analysis and comprehension of
complicated trajectory patterns and may be applied to a variety of tasks, such as behavior analysis, geographic data
visualization, and transportation planning.

The custom function segmentTrajectory considers a trajectory as input and a time threshold in minutes. It aims to divide
the trajectory into smaller segments based on the time intervals between consecutive points. The idea is to split the
trajectory into segments, each containing points that are within the specified time threshold from each other. To
expalin, the trajectory points in the 15th minute(a span of 60 seconds) will be part of a particular trajectory segment.

### 2.3 Indexing

#### 2.3.1 Distance Measures

Distance measures play a pivotal role in trajectory analysis. The project includes a basic implementation of the Closest-Pair-Distance and an advanced implementation of the Dynamic Time Warping distance measure. The two implemented distance measuring techniques will help the users to understand the extent to which the trajectories are similar or dissimilar. Additionally it provides valuable insights into trajectory relationships.

1. Closest-Pair-Distance (basic function)
   It is a basic implementation to calculate the shortest distance between two
   trajectories from a selected set of trajectories. Apart from trajectory analysis, this method plays an important role
   in the field of pattern recognition and spatial data mining. To calculate the distance between two trajectories,
   first the algorithm compares the position of the points within the trajectories. To achieve this step, the algorithm
   uses Euclidean distance as the distance metric. The closest-pair-distance algorithm is efficient, with a time
   complexity of O(n^2) [where n is the number of trajectories in the set].

2. Dynamic Time Warping (feature) Dynamic Time Warping (DTW) is a powerful algorithm used to compare and measure the
   similarity between time series or temporal sequences with variations in their time axis. It handles sequences of
   different lengths or temporal distortions by optimally aligning and warping them in a nonlinear manner. DTW
   dynamically adjusts temporal shifts between corresponding elements of the sequences to minimize overall distance. In
   this project we are implementing DTW as a feature to calculate the distance measure between two trajectories. In fact
   in the main_template we have also added a user coe to iteratively calculate the distance between any two possible
   pairs from the list of trajectories used. To compute the DTW distance between two sequences, let's say sequence A of length m and sequence B of length n, a 2D dynamic programming table with dimensions (m+1) x (n+1) is used. Each cell in the table stores the cumulative distance between the corresponding elements of sequences A and B up to that point. Starting from the top-left corner of the table, the algorithm iteratively fills the table until the bottom-right corner is reached.

3. R-tree:

### 4.2 Region query

#### Solving region query without R-Tree Region queries are a common type of query to direct at trajectories databases or collections. A region query should return all trajectories which exhibit a relationship with the region used as an input.

The implementation presented here returns all trajectories which contain a point which is contained within a given
region. Points which lie directly on the border are also regarded as contained points. The query gets handled by
iteration over all trajectories in the trajectory database or collection and iterating over all points in the currently
selected trajectory. Each point is checked for containment within the given region. Since regions are defined as
concentric circles in this project, this computation can be facilitated using the euclidean distance between the point
and the region center. If this distance is smaller or equal to the radius of the region, the point is contained within
the region. If a contained point is found in a trajectory it is added to the set of results and the traversal through
the remaining points is omitted.

### Copyright and License Statement

Copyright [2023] [Soumya Ganguly], [Alexander Pilz]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Authors

- Soumya Ganguly <sganguly@uni-muenster.de>
- Alexander Pilz <apilz@uni-muenster.de>
- Emily Sterthaus <m_ster15@uni-muenster.de>

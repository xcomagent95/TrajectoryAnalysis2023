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

## 1. Overview

The Trajectory Analysis Project is a comprehensive data visualization project designed to visualize and analyze trajectory data. Its primary focus is on analysis and study of trajectory data, providing various preprocessing techniques, implementing distance measures, and enabling trajectory indexing for faster querying. The project aims to offer a user-friendly interface with intuitive functionalities, which will be useful from basic to advanced users.

## 2. Tasks

### 2.1 Visualization

### 2.2 Preprocessing

### 2.3 Indexing

#### 2.3.1 Distance Measures: Distance measures play a pivotal role in trajectory analysis. The project includes a basic implementation of the Closest-Pair-Distance and an advanced implementation of the Dynamic Time Warping distance measure. The two implemented distance measuring techniques will help the users to understand the extent to which the trajectories are similar or dissimilar. Additionally it provides valuable insights into trajectory relationships.

1.  Closest-Pair-Distance (basic function) It is a basic implementation to calculate the shortest distance between two trajectories from a selected set of trajectories. Apart from trajectory analysis, this method plays an important role in the field of pattern recognition and spatial data mining. To calculate the distance between two trajectories, first the algorithm compares the position of the points within the trajectories. To achieve this step, the algorithm uses Euclidean distance as the distance metric. The closest-pair-distance algorithm is efficient, with a time complexity of O(n^2) [where n is the number of trajectories in the set].

2.  Dynamic Time Warping (feature) Dynamic Time Warping (DTW) is a powerful algorithm used to compare and measure the similarity between time series or temporal sequences with variations in their time axis. It handles sequences of different lengths or temporal distortions by optimally aligning and warping them in a nonlinear manner. DTW dynamically adjusts temporal shifts between corresponding elements of the sequences to minimize overall distance. In this project we are implementing DTW as a feature to calculate the distance measure between two trajectories. In fact in the main_template we have also added a user coe to iteratively calculate the distance between any two possible pairs from the list of trajectories used.

To compute the DTW distance between two sequences, let's say sequence A of length m and sequence B of length n, a 2D dynamic programming table with dimensions (m+1) x (n+1) is used. Each cell in the table stores the cumulative distance between the corresponding elements of sequences A and B up to that point. Starting from the top-left corner of the table, the algorithm iteratively fills the table until the bottom-right corner is reached.

2.  R-tree:

### Copyright and License Statement

Copyright [2023] [Soumya Ganguly]

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

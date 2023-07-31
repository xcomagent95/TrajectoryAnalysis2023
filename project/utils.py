# imports
from datetime import datetime
import numpy as np
import point
import trajectory
import math
from glob import glob
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.io as pio
import point
import rtree

# ---------------------- GIVEN -----------------------
"""Import a single trajectory from a file with the file format 
xCoordinate yCoordinate day hour ... (other attributes will not be imported).
Each trajectory should hold an unique number (id)."""
def importTrajectory(filename: str, number: int) -> trajectory:
    # Import
    data = np.loadtxt(filename, delimiter=' ', dtype=str)

    # Create trajectory
    currTrajectory = trajectory.trajectory(number)

    # Convert data into points
    for entry in data:
        # Create point
        x = float(entry[0])
        y = float(entry[1])
        day = entry[2]
        hour = entry[3]
        timestamp = day + ':' + hour
        newPoint = point.point(x,y,timestamp,trajectoryID=number)
        currTrajectory.addPoint(newPoint)

    # Return trajectory
    return currTrajectory


"""Import the given set of 62 with indexes between 1 and 96 trajectories"""
def importTrajectories(foldername: str) -> list:
    listOfTrajectories = []
    for i in range(1, 96):
        filename = foldername + '/extractedTrace' + str(i) + '.txt'

        if glob(filename):
            currTrajectory = importTrajectory(filename, i)
            listOfTrajectories.append(currTrajectory)
    return listOfTrajectories


"""Method to calculate the perpendicular distance between one point
and a segment defined by two points"""
# Modified to avoid division by zero error.
# Todo: Verify i work!
def calculateDistance(point, p1, p2):
    if p2.X == p1.X:
        return abs(point.X - p1.X)
    else:
        m = (p2.Y - p1.Y) / (p2.X - p1.X)
        a = m
        b = -1
        c = - (m * p1.X - p1.Y)
        d = abs((a * point.X + b * point.Y + c)) / (math.sqrt(a * a + b * b))
        # print("Perpendicular distance is", d)
        return d


"""Calculate euclidean distance between two given points"""
def pointDistance(p0: point, p1: point) -> float:
    dist = math.sqrt((p0.X-p1.X)**2+(p0.Y-p1.Y)**2)
    return dist
# --------------------------------------------------


perpendicularDistance = calculateDistance
euclideanDistance = pointDistance


# The following Section adds the visualization of trajectories to the project
# Either use the plotly or the pyplot version
# Todo: Talk to Seep which Library are allowed

# ---------------------- 1.1) -----------------------
# This function visualizes the trajectories in a plotly graph
def visualizeTrajectories(listOfTrajectories: list):
    fig = go.Figure()
    for t in listOfTrajectories:
        x = []
        y = []
        for p in t.points:
            x.append(p.X)
            y.append(p.Y)
        fig.add_trace(
            go.Scatter(x=x, y=y, mode='lines', visible='legendonly', name=t.unique_id if t.unique_id else t.number))
    pio.show(fig)

# This function visualizes the trajectories in a pyplot graph
def visualizeTrajecotriesPyPlot(listOfTrajectories: list):
    for t in listOfTrajectories:
        x = []
        y = []
        for p in t.points:
            x.append(p.X)
            y.append(p.Y)
        plt.plot(x, y)
    plt.show()
# ---------------------------------------------------

# ---------------------- 3.2) -----------------------
# Function to build an R Tree out of a list of trajectories:
def buildRTree(listOfTrajectories: list):
    tree = rtree.rTree()
    tree.fillRTree(listOfTrajectories)
# ---------------------------------------------------

"""
Custom function to segment a trajectory input based on a time interval passed as argument.
So if there are points more than the threshold difference mentioned in the variable
time_threshold_in_minutes; we will segment and add the point to the new segment.
The idea is to split the trajectory into segments of a minute or two.
"""
def segmentTrajectory(trajectory_input, time_threshold_in_minutes):
    segments = []
    segment = [trajectory_input[0]]
    for i in range(1, len(trajectory_input)):
        # Extracting minute from time stamp of previous point
        minute_time_for_prev_point = int(
            trajectory_input[i - 1].timestamp.split(":")[2])

        # Extracting minute from time stamp of current point
        minute_time_for_curr_point = int(
            trajectory_input[i].timestamp.split(":")[2])

        # Calculating the minutes difference
        difference_in_minutes = minute_time_for_curr_point - minute_time_for_prev_point

        if difference_in_minutes < time_threshold_in_minutes:
            segment.append(trajectory_input[i])
        else:
            segments.append(segment)
            segment = [trajectory_input[i]]
    segments.append(segment)
    return segments

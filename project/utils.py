# imports
import numpy as np
import point
import trajectory
import math
from glob import glob
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.io as pio
import point


"""Import a single trajectory from a file with the file format 
xCoordinate yCoordinate day hour ... (other attributes will not be imported).
Each trajectory should hold an unique number (id)."""
def importTrajectory(filename:str,number:int) -> trajectory:
    # Import
    data = np.loadtxt(filename, delimiter=' ',dtype=str)

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
        newPoint = point.point(x,y,timestamp)
        currTrajectory.addPoint(newPoint)

    # Return trajectory
    return currTrajectory

"""Import the given set of 62 with indexes between 1 and 96 trajectories"""
def importTrajectories(foldername:str) -> list:
    listOfTrajectories = []
    for i in range(1,96):
        filename = foldername + '/extractedTrace' + str(i) + '.txt'

        if glob(filename):
            currTrajectory = importTrajectory(filename,i)
            listOfTrajectories.append(currTrajectory)
    return listOfTrajectories

"""Method to calculate the perpendicular distance between one point
and a segment defined by two points"""
def calculateDistance(point:point,p1:point,p2:point):
    m = (p2.Y - p1.Y)/(p2.X - p1.X)
    a = m
    b = -1
    c = - (m*p1.X - p1.Y)
    d = abs((a * point.X + b * point.Y + c)) / (math.sqrt(a * a + b * b))
    print("Perpendicular distance is"),d
    return d

"""Calculate euclidean distance between two given points"""
def pointDistance(p0:point,p1:point) -> float:
    dist = math.sqrt((p0.X-p1.X)**2+(p0.Y-p1.Y)**2)
    return dist

#The following Section adds the visualization of trajectories to the project
#Either use the plotly or the pyplot version
#Todo: Talk to Seep which Library are allowed

#This function visualizes the trajectories in a plotly graph
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

#This function visualizes the trajectories in a pyplot graph
def visualizeTrajecotriesPyPlot(listOfTrajectories: list):
    for t in listOfTrajectories:
        x = []
        y = []
        for p in t.points:
            x.append(p.X)
            y.append(p.Y)
        plt.plot(x, y)
    plt.show()

perpendicularDistance = calculateDistance
euclideanDistance = pointDistance

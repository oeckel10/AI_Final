import json
import pandas as pd

class InputData:

    def __init__(self, path):
        # Enter the directory of the tour data
        self.path = path
        self.DataLoad()

    def DataLoad(self):
        var = ['Instances']
        var.append(self.path)

        # Enter the directory of the tour data
        path = '\\'.join(var)

        # Read in the data from the tour data file and save in variable “inputData”
        with open(path) as f:
            inputData = json.load(f)

        # Saving the route matrix
        self.data = inputData['Distances']

        # Import the coordinate list
        self.coordinates = inputData['Coordinates']  # Import the coordinate list

        # Generation of an array with the numbers 0-(number of points in the route plan) for axis labeling in order to be able to trace the matrix more clearly and easily
        axis = [i for i in range(len(self.data[0]))]

        # Create a matrix using Pandas DataFrame, as this structure is relatively easy to work with
        self.matrix = pd.DataFrame()
        for row in self.data:
            self.matrix = pd.DataFrame(self.data, columns=axis, index=axis)  # Insert the data with labeling of the axes x,y
        

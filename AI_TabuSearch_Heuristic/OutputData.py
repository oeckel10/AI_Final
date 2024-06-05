import csv
from EvaluationLogic import *
import os

class outputAlgorithm:
    def __init__(self, order_final, matrix, coordinates, path):  # Add the path parameter to the constructor
        self.order_final = order_final  # Store the final order of points
        self.matrix = matrix  # Store the distance matrix
        self.coordinates = coordinates  # Store the coordinates of the points
        self.path = path  # Store the path of the input file

    def startOutput(self):  # Add the startOutput method
        if not os.path.exists('Solutions'):  # Check if the Solutions directory exists
            os.mkdir('Solutions')  # Create the Solutions directory if it does not exist

        writer_path = 'Solutions\Solution-' + self.path.replace('.json', '') + '.csv'  # Define the path for the output CSV file
        cum_sum = 0  # Initialize the cumulative sum of the path costs

        id = self.path.replace('.json', '').replace('scenario_example_id_', '')  # Extract the scenario ID from the input file name
        
        # Open the CSV file in write mode
        with open(writer_path, 'w', newline='') as file:  # Use 'w' mode to write a new file or overwrite an existing file
            writer = csv.writer(file)  # Create a CSV writer object
            
            writer.writerow([id])  # Write the scenario ID to the CSV file
            
        for i in range(len(self.order_final)):  # Iterate over the final order of points
            if i == len(self.order_final) - 1:  # Check if the current point is the last point in the order
                cum_sum += self.matrix.iloc[self.order_final[i], self.order_final[0]]  # Calculate the path cost from the last point to the first point
                
                # Open the CSV file in append mode
                with open(writer_path, 'a', newline='') as file:  # Use 'a' mode to append to an existing file
                    writer = csv.writer(file)  # Create a CSV writer object
                    
                    writer.writerow([self.coordinates])  # Write the coordinates of the points to the CSV file
                    writer.writerow([self.order_final])  # Write the final order of points to the CSV file
                    writer.writerow([cum_sum])  # Write the cumulative sum of path costs to the CSV file
                break
            else:
                cum_sum += self.matrix.iloc[self.order_final[i], self.order_final[i + 1]]  # Calculate the path cost from the current point to the next point

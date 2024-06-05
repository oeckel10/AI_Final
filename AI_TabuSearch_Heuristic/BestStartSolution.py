from EvaluationLogic import *
from InputData import *
import random
from copy import deepcopy
import math
pd.options.mode.chained_assignment = None  # Disable warnings for chained assignments, common in pandas operations

class BestStartSolution:
    def __init__(self, matrix, seed):
        self.matrix = matrix  # Distance matrix for the TSP
        self.start_solution_pool = []  # Pool to store generated start solutions
        self.cache = []  # General purpose cache, unused in this snippet
        self.seed = seed  # Seed for reproducibility in random number generation

    def generate_best_start_solution(self):
        # Generate a simple First Come First Serve (FCFS) solution
        fcfs = list(range(len(self.matrix)))  # Create a route that visits points in the order they appear
        self.start_solution_pool.append(deepcopy(fcfs))  # Add the FCFS route to the solution pool

        # Generate random solutions, 200 reproducible random numbers with seed
        random.seed(self.seed)  # Set the seed for random number generation
        random_numbers = [random.randint(0, 10000) for _ in range(200)]  # Generate 200 random numbers
        random_cache = []  # Cache to store random solutions

        for i in random_numbers:  # Iterate over each generated random number
            axis = list(range(len(self.matrix[0])))  # List of indices for points
            axis.remove(0)  # Remove the start point index
            axis.remove(len(self.matrix[0]) - 1)  # Remove the end point index
            size = len(self.matrix)

            first_order = random.sample(axis, len(self.matrix[0]) - 2)  # Randomly sample points to visit
            order = [0] + first_order + [size - 1]  # Create a complete tour including start and end

            if not random_cache:
                random_cache.append(order)  # Add the first random solution to the cache
            else:
                # Compare the new random solution to the last one in cache using a custom evaluation function
                if EvaluationLogic().SolutionFinder(order, self.matrix) < EvaluationLogic().SolutionFinder(random_cache[-1], self.matrix):
                    random_cache.append(order)  # Only add better solutions to the cache

        self.start_solution_pool.append(deepcopy(random_cache[-1]))  # Add the best random solution to the pool

        # Generate a solution based on Shortest Processing Time (SPT)
        matrice = deepcopy(self.matrix)  # Copy the matrix to modify
        matrice = matrice.astype(float)  # Ensure the matrix is in float for operations

        for i in range(len(matrice[0]) - 1):
            matrice.iloc[i,i] = math.inf  # Set diagonal to infinity to avoid self-loops
        matrice.replace(-1, math.inf, inplace=True)  # Replace any -1s with infinity to denote impossible paths

        order_list = []  # List to store the order of points visited
        line = 0  # Start from the first point
        i = 0

        matrice.drop(matrice.tail(1).index, inplace=True)  # Drop the last row
        matrice = matrice.iloc[:, :-1]  # Drop the last column
        length = len(matrice[0] - 1)

        while i < (length - 1):  # Iterate until all points are visited
            matrice.iloc[line].idxmin()  # Find the point with the minimum distance from the current point
            line_alt = deepcopy(line)  # Backup the current point index
            order_list.append(matrice.loc[line].idxmin())  # Add the next point to the order list

            line = matrice.loc[line].idxmin()  # Move to the next point
            del matrice[line_alt]  # Remove the visited point from consideration
            i += 1

        order_list.append(len(matrice))  # Add the last point
        order_list.insert(0, 0)  # Insert the start point at the beginning

        self.start_solution_pool.append(deepcopy(order_list))  # Add the SPT solution to the pool

        # Return the best solution from the pool based on the evaluation logic
        if EvaluationLogic().SolutionFinder(self.start_solution_pool[0], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[1], self.matrix) and \
           EvaluationLogic().SolutionFinder(self.start_solution_pool[0], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[2], self.matrix):  # Compare the FCFS solution to the random and SPT solutions
            return self.start_solution_pool[0]  # Return the first solution if it's the best
        elif EvaluationLogic().SolutionFinder(self.start_solution_pool[1], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[0], self.matrix) and \
             EvaluationLogic().SolutionFinder(self.start_solution_pool[1], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[2], self.matrix):  # Compare the random solution to the FCFS and SPT solutions
            return self.start_solution_pool[1]  # Return the second solution if it's the best
        else:
            return self.start_solution_pool[2]  # Otherwise, return the third solution

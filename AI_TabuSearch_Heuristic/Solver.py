from copy import deepcopy
from timeit import default_timer

from InputData import *
from OutputData import *
from EvaluationLogic import *

class Solver:

    def __init__(self, path):  # Constructor
        self.path = path  # Path to the JSON file
        self.solutionPool = []  # Pool to store solutions
        

    def generateNeighboorhood(self, firstSolution, matrix, coordinates, tabuList, type = 'swap', maxIterations=10000):  # Function to generate the neighborhood of a solution
        self.matrix = matrix  # Distance matrix for the TSP
        self.firstSolution = firstSolution  # Initial solution
        self.type = type  # Type of neighborhood generation
        self.coordinates = coordinates  # Coordinates of the points
        self.maxIterations = maxIterations  # Maximum number of iterations
        self.tabuList = tabuList  # Tabu list to store forbidden moves
        localBestSolution = []  # List to store the best solutions in the neighborhood
        it=0  # Iteration counter

        aspiration_criteria = [EvaluationLogic().SolutionFinder(deepcopy(firstSolution), self.matrix), deepcopy(firstSolution)]  # Aspiration criteria to store the best solution found
        

        if type == "swap":  # Swap neighborhood generation
            localBestSolution.clear()  # Clear the list of best solutions

            for i in range(1, len(self.firstSolution)-1):  # Iterate over the solution
                for j in range(1, len(self.firstSolution)-1):  # Iterate over the solution
                    if it == self.maxIterations:  # Check if the maximum number of iterations has been reached
                        break  
                    else:
                        it+=1
                        if i < j:
                            indexA = j
                            indexB = i
                            nextSolution = list(self.firstSolution)  # Create a copy of the solution

                            nextSolution[indexA] = deepcopy(self.firstSolution[indexB])  # Swap the elements
                            nextSolution[indexB] = deepcopy(self.firstSolution[indexA])  # Swap the elements

                            changeCombi = (i, j)  # Store the change combination
                            
                            if (changeCombi not in self.tabuList) or (EvaluationLogic().SolutionFinder(deepcopy(nextSolution), self.matrix) < aspiration_criteria[0])==True: # Check if the move is allowed
                                    localBestSolution.append(nextSolution)  # Add the solution to the list of best solutions
                                    if aspiration_criteria[0] > EvaluationLogic().SolutionFinder(nextSolution, self.matrix):  # Check if the new solution is better
                                        aspiration_criteria[0] = EvaluationLogic().SolutionFinder(nextSolution, self.matrix)
                                        aspiration_criteria[1] = nextSolution
            
            cache = []
            for i in localBestSolution:  # Iterate over the best solutions
                cache.append(EvaluationLogic().SolutionFinder(deepcopy(i), self.matrix))  # Evaluate the solutions

            index_min = min(range(len(cache)), key=cache.__getitem__)  # Find the best solution
            singleLocalBestSolution = deepcopy(localBestSolution[index_min])  # Store the best solution

            return singleLocalBestSolution  # Return the best solution

        elif type == 'insertion':  # Insertion neighborhood generation
            nextPermut = []
            nextPermuts = []
            localBestSolution.clear()  # Clear the list of best solutions
            firstSolutio = deepcopy(self.firstSolution)  # Create a copy of the solution

            for i in range(1, len(firstSolutio)-1):  # Iterate over the solution
                for j in range(1, len(firstSolutio)-1):  # Iterate over the solution
                    if it == self.maxIterations:  # Check if the maximum number of iterations has been reached
                        break
                    if i == j or i == j + 1:  # Check if the indices are the same
                        continue
                    elif i<j:
                        it+=1
                        nextPermuts.clear()
                        nextPermut.clear()
                        indexA = deepcopy(i)  # Store the index
                        indexB = deepcopy(j)  # Store the index

                        for k in range(len(firstSolutio)):  # Iterate over the solution
                            if k == i:
                                continue
                            nextPermut.append(deepcopy(firstSolutio[k]))  # Add the element to the new solution
                        nextPermut.insert(indexB, deepcopy(firstSolutio[i]))  # Insert the element at the new index
                        changeCombi = (i, j)  # Store the change combination
                        nextPermuts = [nextPermut, changeCombi]  # Store the new solution and the change combination

                        if (changeCombi not in self.tabuList) or (EvaluationLogic().SolutionFinder(nextPermuts[0], self.matrix) < aspiration_criteria[0])==True:  # Check if the move is allowed
                            localBestSolution.append(deepcopy(nextPermuts))  # Add the solution to the list of best solutions
                            nextSolu = EvaluationLogic().SolutionFinder(nextPermuts[0], self.matrix)  # Evaluate the solution
                            if aspiration_criteria[0] > nextSolu:  # Check if the new solution is better
                                aspiration_criteria[0] = nextSolu  # Update the aspiration criteria
                                aspiration_criteria[1] = nextPermuts[0]  # Update the aspiration criteria

            cache = []
            localBestSolution2 = [item[0] for item in localBestSolution]  # Extract the solutions
            for i in localBestSolution2:  # Iterate over the best solutions
                cache.append(EvaluationLogic().SolutionFinder(deepcopy(i), self.matrix))  # Evaluate the solutions

            index_min = min(range(len(cache)), key=cache.__getitem__)  # Find the best solution
            singleLocalBestSolution = deepcopy(localBestSolution[index_min])  # Store the best solution

            return singleLocalBestSolution  # Return the best solution

    def tabuSearch(self, firstSolution, matrix, coordinates, path, maxTabuListLength=5, maxIterations = 500):  # Tabu search algorithm
        self.firstSolution = firstSolution  # Initial solution
        self.matrix = matrix  # Distance matrix for the TSP
        self.coordinates = coordinates  # Coordinates of the points
        self.path = path  # Path to the JSON file
        tabuList = []  # Tabu list to store forbidden moves
        Solution = deepcopy(firstSolution)  # Initial solution
        self.solutionPool.append(deepcopy(firstSolution))  # Add the initial solution to the pool
        self.maxTabuListLength = maxTabuListLength  # Maximum length of the tabu list
        self.maxIterations = maxIterations  # Maximum number of iterations
        time_needed=default_timer()  # Start the timer
        timer = 0
        iteration = 1
        changeCombination = []
        changeCombinationCache = []

        if len(self.matrix[0])<50:  # Check the size of the matrix
            maxTabuSearchTime = 10  # Set the maximum time for the tabu search
        else:
            maxTabuSearchTime = 280  # Set the maximum time for the tabu search
        
        while timer < maxTabuSearchTime:  # Iterate until the maximum time is reached
            iteration+=1  
            
            di = self.generateNeighboorhood(deepcopy(Solution), self.matrix, self.coordinates, tabuList, type='swap', maxIterations=self.maxIterations)  # Generate the neighborhood
            ds = self.generateNeighboorhood(deepcopy(Solution), self.matrix, self.coordinates, tabuList, type='insertion', maxIterations=self.maxIterations)  # Generate the neighborhood
            
            if EvaluationLogic().SolutionFinder(di, self.matrix) <= EvaluationLogic().SolutionFinder(ds[0], self.matrix):  # Compare the solutions
                changeCombination = []

                for index, (first, second) in enumerate(zip(Solution, di)):  # Iterate over the solutions
                    if first != second:  # Check if the elements are different
                        changeCombination.append(index)  # Store the change combination

                changeCombinationCache = changeCombination[0], changeCombination[1]  # Store the change combination
                tabuList.append(changeCombinationCache)  # Add the change combination to the tabu list
                Solution=deepcopy(di)  # Update the solution
                self.solutionPool.append(deepcopy(Solution))  # Add the solution to the pool

            else: 
                changeCombination = deepcopy(ds[1])  # Store the change combination
                tabuList.append(changeCombination)  # Add the change combination to the tabu list
                
                Solution=deepcopy(ds[0])  # Update the solution
                self.solutionPool.append(deepcopy(Solution))  # Add the solution to the pool

            timer = default_timer() - time_needed  # Update the timer

            while len(tabuList) > self.maxTabuListLength:  # Check the length of the tabu list
                tabuList.pop(0)  # Remove the first element

        cache = []
        for i in self.solutionPool:  # Iterate over the solutions
            cache.append(EvaluationLogic().SolutionFinder(i, self.matrix))  # Evaluate the solutions

        index_min = min(range(len(cache)), key=cache.__getitem__)  # Find the best solution
        bestFinalSolution = deepcopy(self.solutionPool[index_min])  # Store the best solution

        outputAlgorithm(bestFinalSolution, self.matrix, self.coordinates, self.path).startOutput()  # Output the best solution
        
        return bestFinalSolution  # Return the best solution
import math

class EvaluationLogic:

    def __init__(self):
        self.path_sum = 0

    def SolutionFinder(self, order, matrix):    
    # Introduction of run/count variables
        self.path_sum = 0  # Indicates the sum of the travel costs
        i = 0  # Iterates over each element of the reassembled array order
        counter = 1     # Is required to incorporate a termination criterion, as otherwise an error is thrown if iteration is at the last element, as the path costs in the for loop
                        # from the current element to the next element in the array are added up. However, there is no subsequent element at the last element in the array
                        # this is why a termination criterion 'if counter == len(data[0])' is built in
                        # It is also used to target the next element in the array after i -> see for loop, part “else:...”

        for i in order:  # Iterates over each element in the array order
            if counter == len(matrix[0]):  # Cancellation criterion
                break  # If this occurs, the for loop is aborted and the code is continued outside
            elif matrix.iloc[i, order[counter]] == -1:  # Second termination criterion: if a connection has an evaluation of '-1', this means that this connection is invalid
                self.path_sum = math.inf  # If connection is invalid, the path costs of this permutation are assigned the value infinity and the for loop is aborted, the next permutation is started
                break
            else:  # If no abort criterion is met, the following code is executed
                self.path_sum = self.path_sum + matrix.iloc[i, order[counter]]  # Path costs are accumulated by adding the edge evaluation from point i to the subsequent point in the array to the previous path costs
                                                                                # However, the subsequent point must be addressed with 'order[counter]', as 'i+1' only leads to an incremental increase 
                                                                                # of the value i and not to the next position in the array. The counting variable 'counter' was introduced for this purpose
                counter += 1  # Increment count variable incrementally, for next iteration step
        return self.path_sum
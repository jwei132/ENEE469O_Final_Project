import numpy as np

class linear_prog():
    def __init__(self):
        self.source_supply = None
        self.dest_demand = None
        self.cost_matrix = None
        self.sol_matrix = None

    def set_source(self, array):
        self.source_supply = np.copy(array)

    def set_dest(self, array):
        self.dest_demand = np.copy(array)

    def set_cost(self, array):
        

        if len(array) is not len(self.source_supply) or len(array[0]) is not len(self.dest_demand):
            return False
        
        self.sol_matrix = np.zeros(len(self.source_supply), len(self.dest_demand))
        for i in range(0, self.sol_matrix):
            for j in range(0, self.sol_matrix[0]):
                self.sol_matrix[i, j] = array[i, j]

        return True


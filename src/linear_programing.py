import numpy as np
import scipy
import scipy.optimize

class linear_prog():
    def __init__(self):
        self.__source_supply = None
        self.__dest_demand = None
        self.__cost_matrix = None
        self.__sol_matrix = None
        self.__num_source = None
        self.__num_dest = None

    def set_source(self, array):
        self.__source_supply = np.copy(array)
        self.__num_source = len(array)

    def set_dest(self, array):
        self.__dest_demand = np.copy(array)
        self.__num_dest = len(array)

    def set_cost(self, array):
        if self.__source_supply is None or self.__dest_demand is None:
            return False

        if len(array) is not len(self.__source_supply) or len(array[0]) is not len(self.__dest_demand):
            return False
        
        self.__sol_matrix = np.zeros([len(self.__source_supply), len(self.__dest_demand)])
        self.__cost_matrix = np.zeros([len(self.__source_supply), len(self.__dest_demand)])
        for i in range(0, len(self.__cost_matrix)):
            for j in range(0, len(self.__cost_matrix[0])):
                self.__cost_matrix[i, j] = array[i, j]

        return True
    
    def __get_objective(self):
        mult_array = np.multiply(self.__cost_matrix, self.__sol_matrix)
        return np.sum(mult_array)
    
    def __flatten_problem(self):
        # x is a vector with length n*m

        self.__c = np.array([])
        for row in self.__cost_matrix:
            self.__c = np.append(self.__c, row)
        self.__c = np.matrix.astype(self.__c, int)

        # Equality constraints on demand (i.e. All demands of each destination must be met)
        self.__A_eq_demand = np.zeros([self.__num_dest, self.__num_dest * self.__num_source])
        for row_index in range(0, len(self.__A_eq_demand)):
            self.__A_eq_demand[row_index, row_index:len(self.__A_eq_demand[0]):self.__num_dest] = 1
        self.__b_eq_demand = np.copy(self.__dest_demand)

        self.__A_eq_demand = np.matrix.astype(self.__A_eq_demand, int)
        self.__b_eq_demand = np.matrix.astype(self.__b_eq_demand, int)

        # Inequality constraints on solutions being positive
        self.__A_ub_pos = -1 * np.identity(self.__num_source * self.__num_dest)
        self.__b_ub_pos = np.zeros(self.__num_dest * self.__num_source)

        # Inequality constraints for supply constraints
        self.__A_ub_sup = np.zeros([self.__num_source, self.__num_dest * self.__num_source])
        for row_index in range(0, len(self.__A_ub_sup)):
            self.__A_ub_sup[row_index, self.__num_dest*row_index:self.__num_dest*(row_index+1)] = 1
        self.__b_ub_sup = np.copy(self.__source_supply)

        self.__A_ub = np.concatenate((self.__A_ub_pos, self.__A_ub_sup))
        self.__b_ub = np.concatenate((self.__b_ub_pos, self.__b_ub_sup))

        self.__A_ub = np.matrix.astype(self.__A_ub, int)
        self.__b_ub = np.matrix.astype(self.__b_ub, int)

    def solve(self):
        self.__flatten_problem()
        sol = scipy.optimize.linprog(self.__c, self.__A_ub, self.__b_ub, self.__A_eq_demand, self.__b_eq_demand, method='simplex')
        x = np.zeros([self.__num_source, self.__num_dest])
        for i in range(0, self.__num_source):
            x[i] = sol.x[i*self.__num_dest:(i+1)*self.__num_dest]
        return x, sol


        
        



        

    




import numpy as np
import scipy
import scipy.optimize

class linear_prog():
    def __init__(self):
        self.__supply_capacity = None
        self.__destination_demand = None
        self.__cost_matrix = None
        self.__num_source_nodes = None
        self.__num_dest_nodes = None

    def set_source(self, array):
        self.__supply_capacity = np.copy(array)
        self.__num_source_nodes = len(array)

    def set_dest(self, array):
        self.__destination_demand = np.copy(array)
        self.__num_dest_nodes = len(array)

    def set_cost(self, array):
        # Check if either supply capacity or destination demand arrays are not set
        if self.__supply_capacity is None or self.__destination_demand is None:
            return False
        
        # Checks if the dimentions of the input array matches the number of supply and destination nodes.
        if len(array) is not len(self.__supply_capacity) or len(array[0]) is not len(self.__destination_demand):
            return False
        
        self.__sol_matrix = np.zeros([len(self.__supply_capacity), len(self.__destination_demand)])
        self.__cost_matrix = np.copy(array)

        return True
    
    def __get_objective(self, x): # Returns the p* value
        mult_array = np.multiply(self.__cost_matrix, x)
        return np.sum(mult_array)
    
    def __flatten_problem(self):
        '''
        Converts the input arrays and vectors into a linear program in the form:
        Minimize c^T * x
        st. A_ub * x <= b_ub
            A_eq * x = b_eq
        
        Since the goal of our problem is to find an optimal matrix X which represents the number of products from each supply node to destination node, we can flatten it into a vector x with a length of n*m where n is the number of source nodes and m is the number of destination nodes. 

        In the same way, the cost matrix C may be flattened into a vector of length n*m.

        A_ub will have dimensions p x (n*m) where p is the number of inequality constraint equations.
        b_ub is a vector of length p

        A_eq will have dimensions q x (n*m) where q is the number of equality constraints.
        b_eq is a vector of length q

        This function will take in inputs C (nxm cost matrix), the supply capacity (n length vector), and the destination demands (m length vector) and converts it to the linear form above.
        The inequality constraints for this problem are that the sum of outgoing products for any source node does not exceed the supply node's capacity.
        Another inequality is that any element in the solution vector x must be positive. 
        Finally, the equality constraint for this problem is that the sum of products going to each destination is equal to the demand from that destination node. 
        '''

        # Flattening the cost matrix into a vector of length n*m
        self.__c = np.array([])
        for row in self.__cost_matrix:
            self.__c = np.append(self.__c, row)

        self.__c = np.matrix.astype(self.__c, int)

        # Equality constraints on demand (i.e. All demands of each destination must be met)
        self.__A_eq_demand = np.zeros([self.__num_dest_nodes, self.__num_dest_nodes * self.__num_source_nodes])
        for row_index in range(0, len(self.__A_eq_demand)):
            self.__A_eq_demand[row_index, row_index:len(self.__A_eq_demand[0]):self.__num_dest_nodes] = 1
        self.__b_eq_demand = np.copy(self.__destination_demand)

        self.__A_eq_demand = np.matrix.astype(self.__A_eq_demand, int)
        self.__b_eq_demand = np.matrix.astype(self.__b_eq_demand, int)

        # Inequality constraints on solutions being positive
        self.__A_ub_pos = -1 * np.identity(self.__num_source_nodes * self.__num_dest_nodes)
        self.__b_ub_pos = np.zeros(self.__num_dest_nodes * self.__num_source_nodes)

        # Inequality constraints for supply constraints (the sum of outgoing products from each supplier node does not exceed it's capacity)
        self.__A_ub_sup = np.zeros([self.__num_source_nodes, self.__num_dest_nodes * self.__num_source_nodes])
        for row_index in range(0, len(self.__A_ub_sup)):
            self.__A_ub_sup[row_index, self.__num_dest_nodes*row_index:self.__num_dest_nodes*(row_index+1)] = 1
        self.__b_ub_sup = np.copy(self.__supply_capacity)

        # Concatenate the two inequality sets into one for solving
        self.__A_ub = np.concatenate((self.__A_ub_pos, self.__A_ub_sup))
        self.__b_ub = np.concatenate((self.__b_ub_pos, self.__b_ub_sup))

        self.__A_ub = np.matrix.astype(self.__A_ub, int)
        self.__b_ub = np.matrix.astype(self.__b_ub, int)

    def solve(self):
        self.__flatten_problem()

        # Solve the linear program with the simplex algorithm
        sol = scipy.optimize.linprog(self.__c, self.__A_ub, self.__b_ub, self.__A_eq_demand, self.__b_eq_demand, method='simplex')
        
        # Reconstruct the solution into an array like we expect
        x = np.zeros([self.__num_source_nodes, self.__num_dest_nodes])
        for i in range(0, self.__num_source_nodes):
            x[i] = sol.x[i*self.__num_dest_nodes:(i+1)*self.__num_dest_nodes]
        
        # Returns the solution matrix, the solution object from the scipy function, and the total cost of transportation given the optimal value that was calculated. 
        return x, sol, self.__get_objective(x)


        
        



        

    




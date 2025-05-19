import numpy as np
import random
import os
term_size = os.get_terminal_size()

from linear_program_solver import linear_prog

# The number of products from each supply node
supply_capacity = np.array([5000, 2000, 3000, 4000]) 

# The number of products each destination demands from suppliers
destination_demand = np.array([3123, 1424, 2000, 554, 5344, 543, 1000])

# A cost matrix which represents the cost of moving one product from source to destination.
# An element in row i and column j represents the cost of moving one product from source node i to destination node j
cost_matrix = np.zeros([len(supply_capacity), len(destination_demand)])

# For this simulation, we are generating a random cost matrix. You can modify this to be a specific cost matrix
cost_min = 1
cost_max = 10

# Initiating the random cost matrix
for i in range(0, len(cost_matrix)):
    for j in range(0, len(cost_matrix[0])):
        random.seed()
        cost_matrix[i, j] = random.randint(cost_min, cost_max)

# Creating a linear program solver object
lp = linear_prog()

# Set the source and destination capacity and demand values
lp.set_source(supply_capacity)
lp.set_dest(destination_demand)

# Feeding the cost matrix to the solver. If successful (The dimensions of the cost matrix match the source and destination supply and demand dimensions), returns True. 
if not lp.set_cost(cost_matrix):
    print("Problem adding cost matrix!")

# Solve the linear problem
x, sol, cost = lp.solve()
print("\n\n")
print('=' * term_size.columns)

print("\n\nTo meet the total product demand of " + str(np.sum(destination_demand)) + " items spread across " + str(len(destination_demand)) + " destinations with a supply count of " + str(np.sum(supply_capacity)) + " items spread across " + str(len(supply_capacity)) + " suppliers,")
print("it costs " + str(cost) + " to move products with the optimal transportation solution:\n")
print(x)
print("\n\nGiven a cost matrix:\n")
print(cost_matrix)
print("\n\nWith a supply capacity:")
print(supply_capacity)
print("\n\nAnd destination demand:")
print(str(destination_demand) + "\n\n")

print('=' * term_size.columns)
print("\n\n")
# print(sol)






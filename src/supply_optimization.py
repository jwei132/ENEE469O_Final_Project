import numpy as np
import random

supply_capacity = np.array([5000, 2000, 3000, 4000])

dest_demand = np.array([123, 1424, 34, 554, 5344, 543, 1000])

cost_matrix = np.zeros([len(supply_capacity), len(dest_demand)])

cost_min = 100
cost_max = 200

# Initiating the cost matrix
for i in range(0, len(cost_matrix)):
    for j in range(0, len(cost_matrix[0])):
        random.seed()
        cost_matrix[i, j] = random.randint(cost_min, cost_max)

solution_matrix = np.zeros([len(supply_capacity), len(dest_demand)])



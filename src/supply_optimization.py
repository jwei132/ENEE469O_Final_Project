import numpy as np
import random

from linear_programing import linear_prog

supply_capacity = np.array([5000, 2000, 3000, 4000])

dest_demand = np.array([3123, 1424, 2000, 554, 5344, 543, 1000])

cost_matrix = np.zeros([len(supply_capacity), len(dest_demand)])

cost_min = 1
cost_max = 10

# Initiating the cost matrix
for i in range(0, len(cost_matrix)):
    for j in range(0, len(cost_matrix[0])):
        random.seed()
        cost_matrix[i, j] = random.randint(cost_min, cost_max)

lp = linear_prog()

lp.set_source(supply_capacity)
lp.set_dest(dest_demand)
if not lp.set_cost(cost_matrix):
    print("Problem adding cost matrix!")

x, sol = lp.solve()

print(x)

print(sol)






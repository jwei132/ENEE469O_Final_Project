# Problem Specification

The specific problem we are trying to solve is to determine the optimal number of items to ship from a source to destination under known cost constraints between each source and destination pair while fulfilling each destination's product demand value.

The solution to the optimization problem is an nxm matrix which specifies how much product should be shipped from n sources to m destinations. Each entry in the solution matrix corresponds to how much product is shipped from the ith source to the jth destination.

## Objective Function

The goal of this problem is to generate a transportation matrix X which has dimension nxm representing the number of products moved from each source node to destination node which minimizes the total cost of transportation.

Each entry in X, indexed by (i,j), represents the number of products moved from source node i to destination node j.

We can then take the Frobenius product of the transportation matrix X with the cost matrix C to obtain the total cost of transporting products according to the transportation matrix X.

The goal of the problem is to minimize the Frobenius product of the X and C.

(The Frobenius product of A and B (where A and B have the same dimensions) is defined as a double sum over all the indices of the matrix of a_ij * b_ij)

## Source Capacity Constraints

Given n number of sources, each source has a specific capacity c_i. The sum of outgoing products for a specific source node cannot exceed the total capacity of that node.

## Destination Demand Constraints

To solve this optimization problem, we are assuming that the demand for any given destination node is fulfilled with products from source nodes.

The demand for a specific destination node is denoted d_j.

## Non-negative Constraints

In the solution, the number of products moved from each source to destination node may not be negative.

## Cost Constraints

The cost constraints are represented in an nxm matrix.  Each entry indexed by (i,j) represents the cost of moving one product from source node i to destination node j.

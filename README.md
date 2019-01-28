# VDA Assignment and Course Project
## Assignment 1 - Kernighan Lin Partitioning Algorithm

**Input Format**

A text file containing the adjacency matrix is taken as input when the code is run.
Separate all entries of the matrix in a row with a space and begin each row in a new line. 
Do not have any extra blank row

**Step 1**: Run the code on the command line either on Windows/ Ubuntu

python KL_Partitioning.py

**Step 2**: When prompted to enter the name of the file containing the adjacency matrix, enter the name of the file.

eg: adj_matrix.txt (This file is there in the submission folder)

**Step 3**: Enter number of partitions needed (only a power of 2 is allowed)

When partitions greater than number of nodes is entered, the code exits with a message saying "Partitioning not possible" hence tackling the corner case
In case of the input not being power of 2, it will prompt asking you for input again.

**Output Format**

The required partitions are printed on the command line.

**Modular Approach**

Inorder to make the code modular, the entire code is divided into multiple functions.
Each of the functions is called in a main function and execution of code is carried out.

## Assignment 2 - Simulated Annealing for Partitioning

We all must have heard of Annealing process in case of chemicals and metals. The same concept has been applied to devise an algorithm for graph partitioning.

Simulated Annealing is a heuristic algorithm and there is some sort of randomness in the solution always and convergence to best solution may not be guarenteed.

Objective is to minimize the cost function in every iteration which is given by the sum of cut size and product of imbalance factor and lamdbda (weight of the imbalance factor)

**Input Format**

A text file containing the adjacency matrix is taken as input when the code is run.
Separate all entries of the matrix in a row with a space and begin each row in a new line. 
Do not have any extra blank row

**Step 1**: Run the code on the command line either on Windows/ Ubuntu

python Simulated_Annealing.py

**Step 2**: When prompted to enter the name of the file containing the adjacency matrix, enter the name of the file.

eg: adj_matrix.txt (This file is there in the submission folder)

**Step 3**: Enter number of partitions needed (only a power of 2 is allowed)

When partitions greater than number of nodes is entered, the code exits with a message saying "Partitioning not possible" hence tackling the corner case
In case of the input not being power of 2, it will prompt asking you for input again.

**Output Format**

The required partitions are printed on the command line as result along with the final cut size of the two partitions. An approach similar to the modular approach in KL Partitioning is replicated.





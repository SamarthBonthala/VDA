# VDA Assignment and Course Project
## Assignment 1 - Kernighan Lin Partitioning Algorithm

**Input Format**

A text file containing the adjacency matrix is taken as input when the code is run.
Separate all entries of the matrix in a row with a space and begin each row in a new line. 
Do not have any extra blank row

**Step 1**: Run the code on the command line either on Windows/ Ubuntu

python 15EC143_225_KL_Partitioning.py

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

Simulated Annealing is a heuristic algorithm and there is some sort of randomness in the solution always and convergence to best solution, global mimimum may not be guarenteed and hence the best solution at every accepted iteration is tracked and final partition would be the best solution.

Objective is to minimize the cost function in every iteration which is given by the sum of cut size and product of imbalance factor and lamdbda (weight of the imbalance factor)

**Input Format**

The input files are the testbench files from ISCAS .

**Step 1:** Run the code on the command line either on Windows/ Ubuntu

python 15EC143_225_Simulated_Annealing.py

**Step 2:** When prompted to enter the name of the file containing the netlist, enter the netlist name

eg: s27.bench (This file is there in the submission folder)

**Output Format**

Best partition out of all the accepted solutions is obtained as the output where best solution implies partition with minimum cost. The two partitions as well as associated cost is displayed at the output.

**Novelty in Implementation:**

1. Modular Approach – The problem has been divided into functions and each small task is run in a function and called by the main program when required

2. Choice of lambda value in cost function – Lambda value depends on the size of the netlist (number of gates/nodes). Higher the number of nodes, lower should be the value and vice-versa. A function was coded which takes in number of nodes as input and returns the lambda value based on a quadratic function obtained through rigorous testing for convergence to best possible solution.

3. Initial Temperature Calculation – Simulated annealing requires fixing a temperature value and instead of arbitrarily choosing the temperature value, the annealing algorithm is run 4 times and average of the delta costs between trials is computed and initial temperature is found out using the formula Inital temp = - (Delta_cost_average) / ln(0.9)




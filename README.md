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

## Assignment 3 - Simulated Annealing for Floorplanning

Simulated annealing is a heuristic algorithm employed very often in CAD tools for various processes involved in Physical Design such as partitioning and floorplanning. 

**NOTE**: When executing the code kindly ensure that the following files are present in the same directory-
1. 15EC143_225_SA_Floorplanning.py
2. Netlist files – s27.bench or s298.bench
3. Netlist_to_AdjMatrix.py (Contains function that converts the netlist to adjacency matrix)
4. draw_fp.py (To draw the floorplan obtained using Turtle package)
5. stockmeyer.py (Contains functions for area computation and computation of coordinates of every block)

**Input Format**

The input files are the testbench files from ISCAS .

**Step 1**: Run the code on the command line either on Windows/ Ubuntu

python 15EC143_225_SA_Floorplanning.py

**Step 2**: When prompted to enter the name of the file containing the netlist, enter the netlist name

eg: s27.bench (This file is there in the submission folder)

**Algorithm**

The algorithm is run for multiple temperatures and for multiple times for each temperature. Each time, a cost is computed and the change is accepted if cost decreases from previous stage else accepted with a probability in case of an uphill change (cost increases from previous iteration). Temperature is decreased after a given number of failed attempts to get a downhill move. There might be ups and downs in the cost and the algorithm tracks the best solution obtained until every instant. The algorithm is terminated after a certain amount of time. 

Stockmeyer algorithm is used to compute the area of the given set of blocks. An expression termed Polish expression is constructed which is basically post-order traversal of a binary tree and either operands (nodes) or the operators (‘H’ or ‘V’ - representing slicing orientation ) are entries of the tree. 

Each iteration of the annealing algorithm involves a change to the polish expression in one of the following three ways:
1. **M1 move** – Operand swap: Two adjacent operands in the polish expression are swapped in the expression which gives an altogehter different orientation of the blocks

2. **M2 move** - Chain Invert: Chain is a sequence of operators without an operand in between. This operation basically converts all vertical slicings to horizontal and vice versa ( H -> V and V -> H)

3. **M3 move** - Operand-Operator Swap: An adjacent operator and operand are swapped. Additional care is to be taken when this swap is performed so that the properties for the polish expression are not violated. Ballotting property has to be verified. 

**Output** 

Simulated annealing algorithm puts out globally best/optimal floorplan in the form of a polish expression and we would know the cost = area + c*wirelength and bottom left edge coordinates of every block through the polish expression. The information available is used to illustrate the floorplan graphically using a python package named Turtle. (Python graphics)


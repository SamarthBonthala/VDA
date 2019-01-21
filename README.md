# VDA Assignment and Course Project
## Assignment 1

###Kernighan Lin Partitioning Algorithm

###Input Format

A text file containing the adjacency matrix is taken as input when the code is run.

Step 1: Run the code on the command line 

python KL_Partitioning.py

Step 2: When prompted to enter the name of the file containing the adjacency matrix, enter the name of the file.

ex: adj_matrix.txt (This file is there in the submission folder)

Step 3: Enter number of partitions needed (only a power of 2 is allowed)

When partitions greater than number of nodes is entered, the code exits with a message saying "Partitioning not possible" hence tackling the corner case

###Output Format

Partitions at all levels of the recursion are printed on the command line

###Modular Approach

Inorder to make the code modular, the entire code is divided into multiple functions.
Each of the functions is called in a main function and execution of code is carried out.


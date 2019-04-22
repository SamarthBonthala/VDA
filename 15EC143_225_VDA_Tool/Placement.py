import random
import math
import os
import time
from turtle import *
from Netlist_to_AdjMatrix import netlist_to_adj_mat
from stockmeyer import area_coord
from stockmeyer import vertical
from stockmeyer import horizontal
from SA_Floorplanning import *

# Assuming we get the the area of the circuit from other functions of SA_Floorplanning.py file

def maze_routing(frontier,grid)
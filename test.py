from player import Player
from board import *
#import enter
import tkinter as tk
from math import *

resources = ['d','b','o', 'g','w','g','b', 's','s','w','o','g', 'b','o','s','s', 'w','w','g']
values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
ports = ['g','3','w','3','o','3','b','3','s']

board = Board(resources, values, ports)
board.display_board()

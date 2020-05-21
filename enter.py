from board import Board

def legend():
    print("""+---------------Legend---------------+
|Resources:                          |
|  w - wood                          |
|  g - grain                         |
|  o - ore                           |
|  b - brick                         |
|  s - sheep                         |
|  d - desert                        |
|                                    |
|Values:                             |
|  Enter the #. If its desert enter 0|
|                                    |
|Ports:                              |
|  Resource or '3' for 3:1 ports.    |
|                                    |
|Hexes:                              |
|  Hexes are laid out in battleship  |
|  layout with rows named by letter  |
|  and columns named by number.      |
|  Eg:                               |
|            a1  a2  a3              |
|          b1  b2  b3  b4            |
|        c1  c2  c3  c4  c5          |
|          d1  d2  d3  d4            |
|            e1  e2  e3              |
|                                    |
|Vertices:                           |
|  Vertices should be shown by a     |
|  battleship character, starting    |
|  with the row denoted by a letter, |
|  then by number starting at 1.     |
|  a row is                          |
|                                    |
|Edges: Should be denoted by the     |
|  vertex from which the edge        |
|  started, followed by a "d",       |
|  "l", or "r", with left or right   |
|  going to a1 and a3.               |
+------------------------------------+\n""")

def hexResource(hex):
    while(True):
        val = input("Resource for " + hex + ": ")
        if val in "wgobsd" and val != "":
            break
        print(val + " is not a valid entry, try again.")
    return val
    
def hexValues(hex):
    while(True):
        val = input("Value for " + hex + ": ")
        try:
            val = int(val)
            if type(val) == int and ((val <= 12 and val >= 2 and not val == 7) or val == 0) :
                break
        except:
            pass
        print(str(val) + " is not a valid entry, try again.")
    return val
        
def iterateOverBoard(hexes, entry):
    if entry == "resources":
        print("\nEnter the hex tiles' resource: (one of w,g,s,o,b,d)")
        return [hexResource(str) for str in hexes]
    if entry == "values":
        print("\nEnter the hex tiles' value (between 2 and 12):")
        return [hexValues(str) for str in hexes]

def enterPorts():
    print("\nEnter the values for the ports, starting at the top right of the board and working clockwise.  (one of w,g,s,o,b,3)")
    ports = []
    for i in range(9):
        val = input("Value for port "+str(i)+": ")
        while not val in "wgobs3" or len(val) == 0:
            print(val + " is not a valid entry, try again.")
            val = input("Value for port "+str(i)+": ")
        ports.append(val)
    return ports
  
def convertVertex(string):
    if len(string) < 2 or len(string) > 3:
        return False
    row = ord(string[0])-97
    try:
        col = int(string[1:len(string)])-1
    except:
        return False
    if row > 5 or row < 0 or col > int(12-2*abs(row-2.5))-1:
        return False
    v_index = 0
    for i in range(row):
        v_index += int(12-2*abs(i-2.5))
    v_index += col
    return v_index
  
def enterSettlement(player, board):
    while True:
        print("Settlements may be placed by the following layout:\
        a1:a7, b1:b9, c1:c11, d1:d11, e1:e9, f1:f7")
        vertex = input("\nEnter the vertex the settlement was placed on for player " + str(player+1)+": ")
        v_index = convertVertex(vertex)
        if v_index == False:
            print("Not a valid vertex. Try again.")
            continue
        if board.add_settlement(player, v_index):
            print("Settlement added at " + vertex + " successfully.")
            return
        print("Placement conflicts with another settlement. Try again.")

def convertEdge(edge):
    if len(edge) < 3 or len(edge) > 4:
        return (False, False)
    v1 = convertVertex(edge[0:-1])
    if edge[-1] == 'l':
        v2 = convertVertex(edge[0]+str(int(edge[1:-1])-1))
    elif edge[-1] == 'r':
        v2 = convertVertex(edge[0]+str(int(edge[1:-1])+1))
    elif edge[-1] == 'd':
        if edge[0] < 'c':
            v2 = convertVertex(chr(ord(edge[0])+1)+str(int(edge[1:-1]) + 1))
        elif edge[0] == 'c':
            v2 = convertVertex(chr(ord(edge[0])+1)+edge[1:-1])
        elif edge[0] > 'c':
            v2 = convertVertex(chr(ord(edge[0])+1)+str(int(edge[1:-1]) - 1))
    else:
        v2 = False
    return (v1,v2)

def enterRoad(player, board):
    while True:
        print("Roads may be placed by the node it comes from (one of a1:a7, b1:b9, c1:c11, d1:d11, e1:e9, f1:f7). ")
        edgeStr = input("Enter the vertex the road starts on, followed by either d,l,or r to show the direction the road travels: ")
        edge = convertEdge(edgeStr)
        if not (type(edge[0])==int and type(edge[1])==int):
            print("Not a valid edge. Try again.")
            continue
        if board.add_road(player, edge):
            print("Road added at " + edgeStr + " successfully.\n")
            return
        print("Road placement is not valid, try again.")
        
def enterInitialSettlement(player, board):
    while True:
        print("\nSettlements may be placed by the following layout:\
        a1:a7, b1:b9, c1:c11, d1:d11, e1:e9, f1:f7")
        vertex = input("Enter the vertex the settlement was placed on for player " + str(player+1)+": ")
        v_index = convertVertex(vertex)
        if not type(v_index) == int:
            print("Not a valid vertex. Try again.")
            continue
        if board.add_starting_settlement(player, v_index):
            print("Settlement added at " + vertex + " successfully.")
            return v_index
        print("Placement conflicts with another settlement. Try again.")


def enterInitialRoad(player, board, vertex):
    while True:
        print("\nRoads may be placed by the node it comes from (one of a1:a7, b1:b9, c1:c11, d1:d11, e1:e9, f1:f7). ")
        edgeStr = input("Enter the vertex the road starts on, followed by either d,l,or r to denote the direction from that vertex which the edge travels: ")
        edge = convertEdge(edgeStr)
        if not (type(edge[0]) == int and type(edge[1])==int):
            print("Not a valid edge. Try again.")
            continue
        if board.add_starting_road(player, vertex, edge):
            print("Road added at " + edgeStr + " successfully.")
            return
        print("Road placement is not valid, try again.")

def initialSettlementPlacement(board):
    for i in range(4):
        v = enterInitialSettlement(i,board)
        enterInitialRoad(i,board, v)
    for i in range(3,-1,-1):
        v = enterInitialSettlement(i,board)
        enterInitialRoad(i,board,v)
    
def getWinner():
    while True:
        win = int(input("\nEnter the winner of the game (1:4)"))-1
        if win >= 0 and win < 4:
            return win
        print("Invalid entry, enter a value between 1 and 4.")


hexes = ["a1","a2","a3","b1","b2","b3","b4","c1","c2","c3","c4","c5","d1","d2","d3","d4","e1","e2","e3"]

#Temporary test values:
resources = ['d','b','o', 'g','w','g','b', 's','s','w','o','g', 'b','o','s','s', 'w','w','g']
values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
ports = ['g','3','w','3','o','3','b','3','s']
#Real values:
resources = iterateOverBoard(hexes,"resources")
values = iterateOverBoard(hexes,"values")
ports = enterPorts()

#entries into board also need to change
b = Board(resources, values, ports)
initialSettlementPlacement(b)
b.display_board()
winner = getWinner()


#TODO: Add the print to file functionality
#TODO: Run tests of collecting each turn throughout the game
#TODO: Add development card functionality
#TODO: Add dice functionality

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
|  a row is
|                                    |
|Edges: Should be denoted by a "d",  |
|  "l", or "r", with left or right   |
|  going to a1 and a3, followed by   |
|  the vertex from which the edge    |
|  started.                          |
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
            if type(val) == int and ((val <= 12 and val >= 2) or val == 0) :
                break
        except:
            pass
        print(str(val) + " is not a valid entry, try again.")
    return val
        
def iterateOverBoard(hexes, entry):
    if entry == "resources":
        print("\nEnter the hex tiles' resource: (one of w,g,s,o,b)")
        return [hexResource(str) for str in hexes]
    if entry == "values":
        print("\nEnter the hex tiles' value (between 2 and 12):")
        return [hexValues(str) for str in hexes]

def enterPorts():
    print("\nEnter the values for the ports, starting at the top right of the board and working clockwise.")
    ports = []
    for i in range(9):
        val = input("Value for port "+str(i)+": ")
        while not val in "wgobs3":
            print(val + " is not a valid entry, try again.")
            val = input("Value for port "+str(i)+": ")
        ports.append(val)
    return ports
    
def enterSettlement(board):
    while True:
        vertex = input("\nEnter the vertex the settlement was placed on: ")
        row = ord(vertex[0])-97
        col = int(vertex[1:len(vertex)])-1
        if row > 5 or row < 0 or col > int(12-2*abs(row-2.5))-1:
            print("Not a valid vertex. Try again.")
            pass
        v_index = 0
        for i in range(row):
            v_index += int(12-2*abs(i-2.5))
        v_index += col
        if board.addSettlement(v_index):
            print("Settlement added at " + vertex + " successfully.")
            return
        print("Placement conflicts with another settlement. Try again.")

hexes = ["a1","a2","a3","b1","b2","b3","b4","c1","c2","c3","c4","c5","d1","d2","d3","d4","e1","e2","e3"]
#resources = iterateOverBoard(hexes,"resources")
#values = iterateOverBoard(hexes,"values")
#ports = enterPorts()
empty = ['' for i in hexes]
ports = ['g','3','w','3','o','3','b','3','s']
b = Board(hexes, empty, ports)
enterSettlement(b)
enterSettlement(b)
print(b.toString())

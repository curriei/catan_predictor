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
|  Vertices should be shown by the   |
|  three hexes which surround them,  |
|  starting with top left, moving    |
|  clockwise. In the case that a     |
|  vertex is on the edge of the map, |
|  each water hex next to it should  |
|  be denoted by a w.  In the case of|
|  multiple two water hexes, they    |
|  should be labeled 1 and 2, moving |
|  clockwise.                        |
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
    
def printBoard(resources, values, ports):
    i = 0
    print("     "+ports[0]+"      "+ports[1])
    for row in range(5):
        if row == 1:
            print(" "+ports[8]+" ",end='')
        elif row == 3:
            print(" "+ports[7]+" ",end='')
        else:
            print(" "+" " * 2 * abs(row-2), end='')
        for j in range(5 - abs(row-2)):
            print(" "+str(values[i])+resources[i]+" ", end='')
            i+=1
        if row == 0:
            print("  "+ports[2],end='')
        elif row == 2:
            print(" "+ports[3],end='')
        elif row == 4:
            print("  "+ports[4],end='')
        print()
    print("     " + ports[6]+"      "+ports[5])
    print()
        
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
    


hexes = ["a1","a2","a3","b1","b2","b3","b4","c1","c2","c3","c4","c5","d1","d2","d3","d4","e1","e2","e3"]
resources = iterateOverBoard(hexes,"resources")
values = iterateOverBoard(hexes,"values")
ports = enterPorts()
printBoard(resources,values,ports)

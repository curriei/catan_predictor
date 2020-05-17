import networkx as nx
from player import Player

class Board:

    def __init__(self, resources, values, ports):
        self.resources = resources
        self.values = values
        self.ports = ports
        self.settlements = []
        self.roads = []
        self.players = [Player(), Player(), Player(), Player()]
        self.G = self._create_graph()
        
    def _create_graph(self):
        G = nx.Graph()
        ab_edges = [(0,8),(2,10),(4,12),(6,14)]
        bc_edges = [(7,17),(9,19),(11,21),(13,23),(15,25)]
        cd_edges = [(16,27),(18,29),(20,31),(22,33),(24,35),(26,37)]
        de_edges = [(28,38),(30,40),(32,42),(34,44),(36,46)]
        ef_edges = [(39,47),(41,49),(43,51),(45,53)]
        vertical_edges = ab_edges+bc_edges+cd_edges+de_edges+ef_edges
        G.add_edges_from([(i,i+1) for i in range(53)])
        G.remove_edges_from([(6,7),(15,16),(26,27),(37,38),(46,47)])
        G.add_edges_from(vertical_edges)
        return(G)
    
    def isValidSettlement(self, player, vertex):
        neighbours = set(nx.neighbors(self.G, vertex)).union({vertex})
        if len(neighbours.intersection(set(self.settlements))) > 0 or not self.players[player].can_place_settlement(vertex):
            return False
        return True
      
    def addSettlement(self,player,vertex):
        if self.isValidSettlement(player, vertex):
            index = sum([self.players[i].get_num_settlements() for i in range(player)])
            self.settlements.insert(index, vertex)
            self.players[player].place_settlement(vertex)
            return True
        return False
        
    def isValidRoad(self, player, edge):
        if edge in self.roads or not self.players[player].can_place_road(edge) or not self.G.has_edge(edge[0],edge[1]):
            return False
        return True

    def addRoad(self, player, edge):
        edge = (min(edge),max(edge))
        if self.isValidRoad(player, edge):
            index = sum([self.players[i].get_num_roads() for i in range(player)])
            self.roads.insert(index, edge)
            self.players[player].place_road(edge)
            return True
        return False
        
    def addStartingSettlement(self, player, vertex):
        neighbours = set(nx.neighbors(self.G, vertex)).union({vertex})
        if len(neighbours.intersection(set(self.settlements))) > 0:
            return False
        index = sum([self.players[i].get_num_settlements() for i in range(player)])
        self.settlements.insert(index, vertex)
        self.players[player].place_initial_settlement(vertex)
        return True
    
    def addStartingRoad(self, player, vertex, edge):
        if vertex in edge:
            return self.addRoad(player, edge)
        return False
        
    def toString(self):
        i = 0
        boardString = ""
        boardString += ("     "+self.ports[0]+"      "+self.ports[1]+"\n")
        for row in range(5):
            if row == 1:
                boardString += (" "+self.ports[8]+" ")
            elif row == 3:
                boardString += (" "+self.ports[7]+" ")
            else:
                boardString += (" "+" " * 2 * abs(row-2))
            for j in range(5 - abs(row-2)):
                boardString += (" "+str(self.values[i])+self.resources[i]+" ")
                i+=1
            if row == 0:
                boardString += ("  "+self.ports[2])
            elif row == 2:
                boardString += (" "+self.ports[3])
            elif row == 4:
                boardString += ("  "+self.ports[4])
            boardString += "\n"
        boardString += ("     " + self.ports[6]+"      "+self.ports[5]+ "\n")
        return(boardString)          

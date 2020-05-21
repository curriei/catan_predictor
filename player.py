import networkx as nx

class Player (nx.Graph):
    def __init__(self, colour):
        self.hand = {'cities':4,'settlements':5,'roads':15}
        self.roads = nx.Graph()
        self.settlements = set()
        self.cities = set()
        self.colour = colour
        
    def place_settlement(self,vertex):
        if can_place_settlement(vertex):
            self.settlements.add(vertex)
            self.hand['settlements'] -= 1
            
    def place_initial_settlement(self,vertex):
        self.roads.add_node(vertex)
        self.hand['settlements'] -= 1
        self.settlements.add(vertex)
        
    def place_road(self,edge):
        if self.can_place_road(edge):
            self.roads.add_edge(edge[0],edge[1])
            self.hand['roads'] -= 1
    
    def place_city(self,vertex):
        if self.can_place_city(vertex):
            self.hand['settlements'] += 1
            self.hand['cities'] -=1
            self.settlements.remove(vertex)
            self.cities.add(vertex)
    
    def can_place_settlement(self, vertex):
        if not (vertex in self.settlements or vertex in self.cities) and vertex in nx.nodes(self.roads) and self.hand['settlements'] > 0:
            return True
        return False
        
    def can_place_city(self,vertex):
        if self.hand['cities'] > 0 and vertex in self.settlements:
            return True
        return False
    
    def can_place_road(self,edge):
        if self.hand['roads'] > 0 and (edge[0] in nx.nodes(self.roads) or edge[1] in nx.nodes(self.roads)):
            return True
        return False
        
    def get_num_roads(self):
        return self.roads.number_of_edges()
    
    def get_num_settlements(self):
        return len(self.settlements)
    
    def get_num_cities(self):
        return len(self.cities)
    
    def get_roads(self):
        return [e for e in self.roads.edges]
    
    def get_settlements(self):
        return self.settlements
    
    def get_cities(self):
        return self.cities
        
    def get_colour(self):
        return  self.colour
        
    def get_victory_points(self):
        return self.get_num_cities()*2 + self.get_num_settlements


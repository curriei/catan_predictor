import networkx as nx
import tkinter as tk
from player import Player
from math import *

class Board:

    def __init__(self, resources, values, ports):
        self.resources = resources
        self.values = values
        self.ports = ports
        self.settlements = []
        self.roads = []
        self.players = [Player('red'), Player('blue'), Player('green'), Player('orange')]
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
    
    def is_valid_settlement(self, player, vertex):
        neighbours = set(nx.neighbors(self.G, vertex)).union({vertex})
        if len(neighbours.intersection(set(self.settlements))) > 0 or not self.players[player].can_place_settlement(vertex):
            return False
        return True
      
    def add_settlement(self,player,vertex):
        if self.is_valid_settlement(player, vertex):
            index = sum([self.players[i].get_num_settlements() for i in range(player)])
            self.settlements.insert(index, vertex)
            self.players[player].place_settlement(vertex)
            return True
        return False
        
    def is_valid_road(self, player, edge):
        if edge in self.roads or not self.players[player].can_place_road(edge) or not self.G.has_edge(edge[0],edge[1]):
            return False
        return True

    def add_road(self, player, edge):
        edge = (min(edge),max(edge))
        if self.is_valid_road(player, edge):
            index = sum([self.players[i].get_num_roads() for i in range(player)])
            self.roads.insert(index, edge)
            self.players[player].place_road(edge)
            return True
        return False
        
    def add_starting_settlement(self, player, vertex):
        neighbours = set(nx.neighbors(self.G, vertex)).union({vertex})
        if len(neighbours.intersection(set(self.settlements))) > 0:
            return False
        index = sum([self.players[i].get_num_settlements() for i in range(player)])
        self.settlements.insert(index, vertex)
        self.players[player].place_initial_settlement(vertex)
        return True
    
    def add_starting_road(self, player, vertex, edge):
        if vertex in edge:
            return self.add_road(player, edge)
        return False
    
    def get_player_placements(self, player):
        p = self.players[player]
        return {'roads': p.get_roads(), 'settlements': p.get_settlements(), 'cities': p.get_cities()}
        
    def to_string(self):
        i = 0
        board_string = ""
        board_string += ("     "+self.ports[0]+"      "+self.ports[1]+"\n")
        for row in range(5):
            if row == 1:
                board_string += (" "+self.ports[8]+" ")
            elif row == 3:
                board_string += (" "+self.ports[7]+" ")
            else:
                board_string += (" "+" " * 2 * abs(row-2))
            for j in range(5 - abs(row-2)):
                board_string += (" "+str(self.values[i])+self.resources[i]+" ")
                i+=1
            if row == 0:
                board_string += ("  "+self.ports[2])
            elif row == 2:
                board_string += (" "+self.ports[3])
            elif row == 4:
                board_string += ("  "+self.ports[4])
            board_string += "\n"
        board_string += ("     " + self.ports[6]+"      "+self.ports[5]+ "\n")
        return(board_string)
        
    def display_board(self):
        root = tk.Tk()
        app = Application(self, master=root)
        app.mainloop()
    
    
    
class Application(tk.Frame):
    def __init__(self, board, master=None):
        super().__init__(master)
        self.board = board
        self.master=master
        self.pack()
        self.hex_width = 60
        self.hex_side_length = (self.hex_width*0.5)/cos(pi/6)
        self.width = self.hex_width*7
        self.create_widgets()
    
    def create_widgets(self):
        canvas =  tk.Canvas(self, width=self.width,height=self.width)
        self.draw_hexes(canvas,self.board.resources)
        self.draw_ports(canvas, self.board.ports)
        self.draw_roads(canvas)
        self.draw_settlements(canvas)
        canvas.pack(side='top')
        
        self.enter_values(self.board.values)
        
        self.quit = tk.Button(self, text='Quit', fg='red', command=self.master.destroy)
        self.quit.pack(side='bottom')

    def draw_hexes(self, canvas, resources):
        first_x_center = self.hex_width * 2.5
        y_center = self.hex_width + self.hex_side_length*(0.5 + sin(pi/6))
        i = 0
        for row in range(5):
            x_center = first_x_center
            for col in range(5-abs(row-2)):
                self.draw_hex(canvas, resources[i], x_center, y_center)
                i += 1
                x_center += self.hex_width
                
            if row >= 2:
                first_x_center += self.hex_width*0.5
            else:
                first_x_center -= self.hex_width*0.5
            y_center += self.hex_side_length * (1+sin(pi/6))
        
    def draw_hex(self,canvas,resource, x_center, y_center):
        points = self._get_hex_points(x_center, y_center, self.hex_width, self.hex_side_length)
        colour = self._get_resource_colour(resource)
        canvas.create_polygon(points, fill=colour, outline='grey30', width=2)
        circle_size = 14
        canvas.create_oval(x_center-circle_size,y_center-circle_size,x_center+circle_size,y_center+circle_size,fill='white', outline='white')
        
    def _get_hex_points(self, x_center, y_center, hex_width, hex_side_length):
        point_1_x = x_center - hex_width * 0.5
        point_1_y = y_center + hex_side_length * 0.5
        point_2_x = point_1_x
        point_2_y = point_1_y - hex_side_length
        point_3_x = x_center
        point_3_y = y_center - hex_side_length * (sin(pi/6) + 0.5)
        point_4_x = point_2_x + hex_width
        point_4_y = point_2_y
        point_5_x = point_4_x
        point_5_y = point_1_y
        point_6_x = x_center
        point_6_y = y_center + hex_side_length * ((sin(pi/6)) + 0.5)
        return [point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y, point_4_x, point_4_y, point_5_x, point_5_y, point_6_x, point_6_y]
        
    def _get_resource_colour(self, resource):
        if resource == 'g':
            return 'goldenrod1'
        elif resource == 'b':
            return 'firebrick4'
        elif resource == 'o':
            return 'mediumslateblue'
        elif resource == 'w':
            return 'forestgreen'
        elif resource == 's':
            return 'greenyellow'
        elif resource ==  'd':
            return 'wheat2'
        elif resource == '3':
            return 'grey60'
            
    def draw_ports(self, canvas, ports):
        angles = [-pi/6,pi/6,pi/6,pi/2,5*pi/6,5*pi/6,7*pi/6,3*pi/2,3*pi/2]
        xs = [self.hex_width*1.95,self.hex_width*3.53,self.hex_width*5.05,self.hex_width*6.08,self.hex_width*5.55, self.hex_width*4.03,self.hex_width*2.45,self.hex_width*1.42,self.hex_width*1.42]
        ys = [self.hex_width *1.2, self.hex_width * 0.91 ,self.hex_width*1.8,self.hex_width*3.02,self.hex_width*4.53,self.hex_width*5.41,self.hex_width*5.7,self.hex_width*4.47, self.hex_width*2.73]
        for i in range(len(ports)):
            self.draw_port(canvas, ports[i],xs[i],ys[i],angles[i])
            
    def draw_port(self,canvas, resource, x,y,angle):
        colour = self._get_resource_colour(resource)
        points = self._get_port_points(x,y,angle)
        canvas.create_polygon(points, fill=colour,outline='grey30',width=2)
        
    def _get_port_points(self, x, y, theta):
        length = self.hex_side_length
        x1 = x
        y1 = y
        x2 = x+length*cos(theta)
        y2 = y+length*sin(theta)
        y2 = y+length*sin(theta)
        x3 = x+length*0.9182244753700887*cos(theta-0.36728644275210964)
        y3 = y+length*0.9182244753700887*sin(theta-0.36728644275210964)
        x4 = x+length*0.359400717752101*cos(theta-pi/2.704686111488799)
        y4 = y+length*0.359400717752101*sin(theta-pi/2.704686111488799)
        return(x1,y1,x2,y2,x3,y3,x4,y4)
    
    def draw_settlements(self, canvas):
        for p in range(4):
            d = self.board.get_player_placements(p)
            c = self.board.players[p].get_colour()
            for s in d['settlements']:
                self.draw_settlement(canvas, s, c)
    
    def draw_settlement(self, canvas, vertex, colour):
        center = self._get_vertex_coords(vertex)
        settlement_length = self.hex_side_length/2.4
        settlement_width = self.hex_side_length/3.3
        x1 = center[0] - settlement_length/2
        y1 = center[1] - settlement_width/2
        x2 = center[0] + settlement_length/2
        y2 = center[1] + settlement_width/2
        canvas.create_rectangle(x1, y1, x2, y2, fill=colour)
    
    def draw_roads(self, canvas):
        for p in range(4):
            d = self.board.get_player_placements(p)
            c = self.board.players[p].get_colour()
            for e in d['roads']:
                self.draw_road(canvas, e, c)
        
    def draw_road(self, canvas, road, colour):
        coord1 = self._get_vertex_coords(road[0])
        coord2 = self._get_vertex_coords(road[1])
        canvas.create_line(coord1[0], coord1[1], coord2[0], coord2[1], fill=colour, width=5.0)
    
    def _get_vertex_coords(self, vertex):
        if vertex < 7:
            if vertex % 2 == 0:
                return (self.hex_width*(2+0.5*vertex), self.hex_width*1.3)
            elif vertex % 2 == 1:
                return (self.hex_width*(2+0.5*vertex), self.hex_width*1.05)
        vertex -= 7
        if vertex < 9:
            if vertex % 2 == 0:
                return (self.hex_width*(1.5+0.5*vertex), self.hex_width*2.15)
            elif vertex % 2 == 1:
                return (self.hex_width*(1.5+0.5*vertex), self.hex_width*1.85)
        vertex -= 9
        if vertex < 11:
            if vertex % 2 == 0:
                return (self.hex_width*(1+0.5*vertex), self.hex_width*3.0)
            elif vertex % 2 == 1:
                return (self.hex_width*(1+0.5*vertex), self.hex_width*2.75)
        vertex -= 11
        if vertex < 11:
            if vertex % 2 == 0:
                return (self.hex_width*(1+0.5*vertex), self.hex_width*3.63)
            elif vertex % 2 == 1:
                return (self.hex_width*(1+0.5*vertex), self.hex_width*3.87)
        vertex -= 11
        if vertex < 9:
            if vertex % 2 == 0:
                return (self.hex_width*(1.5+0.5*vertex), self.hex_width*4.5)
            elif vertex % 2 == 1:
                return (self.hex_width*(1.5+0.5*vertex), self.hex_width*4.75)
        vertex -= 9
        if vertex < 7:
            if vertex % 2 == 0:
                return (self.hex_width*(2+0.5*vertex), self.hex_width*5.33)
            elif vertex % 2 == 1:
                return (self.hex_width*(2+0.5*vertex), self.hex_width*5.62)
        
        
    def enter_values(self, values):
        first_x_center = self.hex_width * 2.5
        y_center = self.hex_width + self.hex_side_length*(0.5 + sin(pi/6))
        i = 0
        for row in range(5):
            x_center = first_x_center
            for col in range(5-abs(row-2)):
                l = tk.Label(self, text=str(values[i]))
                l.place(x=x_center,y=y_center, anchor='center')
                i += 1
                x_center += self.hex_width
            if row >= 2:
                first_x_center += self.hex_width*0.5
            else:
                first_x_center -= self.hex_width*0.5
            y_center += self.hex_side_length * (1+sin(pi/6))

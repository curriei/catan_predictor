import networkx as nx
import matplotlib.pyplot as plt

ab = [(0,8),(2,10),(4,12),(6,14)]
bc = [(7,17),(9,19),(11,21),(13,23),(15,25)]
cd = [(16,27),(18,29),(20,31),(22,33),(24,35),(26,37)]
de = [(28,38),(30,40),(32,42),(34,44),(36,46)]
ef = [(39,47),(41,49),(43,51),(45,53)]

vert = ab+bc+cd+de+ef

G = nx.Graph()
G.add_edges_from([(i,i+1) for i in range(53)])
G.remove_edges_from([(6,7),(15,16),(26,27),(37,38),(46,47)])
G.add_edges_from(vert)
nx.draw_networkx(G,with_labels=True)
plt.show()

from Open_Database import GraphReduction
import networkx as nx
import matplotlib.pyplot as plt
path = "C:\\Users\\alexa\\Documents\\TU Delft\\Course material\\Other\\Blockchain\\Blockchain Lab\\Incremental Pagerank\\"
file_name = "multichain_09_02_18"

gr = GraphReduction(path, file_name, 0, 2)
graph = gr.generate_graph(gr.open_data_set())
print len(graph.nodes)
nx.draw_random(graph, node_size=30)
plt.show()

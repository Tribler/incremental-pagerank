from Open_Database2 import GraphReduction2
from Page_Rank2 import IncrementalPersonalizedPageRank2
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np


start_time = time.time()
file_path = "C:\\Users\\alexa\\Documents\\TU Delft\\Course material\\Other\\Blockchain\\Blockchain Lab\\Incremental Pagerank\\"
file_name = "trustchain"

gr = GraphReduction2(file_path, file_name)
gr.open_data_set()
graph = gr.generate_graph()
nx.draw_circular(graph, node_size=30)
plt.show()

node = random.choice(gr.nodes)
pr = IncrementalPersonalizedPageRank2(graph, node, 300, 0.05)
pr.initial_random_walks()
page_ranks = pr.compute_personalized_page_ranks()
page_ranks_2 = nx.pagerank(graph, alpha=0.95, personalization={node: 1},
                           max_iter=500, weight='weight')
print "Monte Carlo Pageranks: ", page_ranks.values()
print "Power Iteration Pageranks: ", page_ranks_2.values()
print np.max(np.array(page_ranks.values()) - np.array(page_ranks_2.values()))

finish_time = time.time()

print finish_time - start_time, " Seconds"

from Open_Database import GraphReduction
from Page_Rank import IncrementalPersonalizedPageRank
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np

start_time = time.time()
path = "C:\\Users\\alexa\\Documents\\TU Delft\\Course material\\Other\\Blockchain\\Blockchain Lab\\Incremental Pagerank\\"
file_name = "multichain_09_02_18"

gr = GraphReduction(path, file_name, 0, 2)
gr.open_data_set()
gr.generate_graph()
#nx.draw_random(gr.graph, node_size=30)
#plt.show()
node = random.choice(gr.blocks)[0]
pr = IncrementalPersonalizedPageRank(gr.graph, node, 1000, 0.05, 500)
pr.initial_random_walks()
page_ranks = pr.compute_personalized_page_ranks()
page_ranks_2 = nx.pagerank(gr.graph,
                           alpha=0.95,
                           personalization={node: 1},
                           max_iter=500,
                           weight='weight')


#print page_ranks.values()
#print page_ranks_2.values()
#print np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values()))/len(page_ranks.values())
#print numpy.abs(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values()))
#print iter(page_ranks.keys()).next()
#print iter(page_ranks_2.keys()).next()
#print numpy.amax(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values()))
#print page_ranks.keys() == page_ranks_2.keys()
#print max(page_ranks.values() - page_ranks_2.values())
finish_time = time.time()

print finish_time - start_time, " Seconds"

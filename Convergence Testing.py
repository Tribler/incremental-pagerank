"""
In this code we run the IncrementalPersonalizedPageRank class on a randomly generated graph to compute the
personalized page rank values. We simultaneously the page rank method given in the networkx library and compare
their values for different parameters.
"""
import networkx as nx
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Page_Rank import IncrementalPersonalizedPageRank
import numpy

random.seed(111)
graph = nx.DiGraph()
number_of_nodes = random.randint(2, 100)
nodes = range(number_of_nodes)
graph.add_nodes_from(nodes)
number_of_random_walks = 10
random_walk_length = 5
difference = list()

for _ in range(2 * number_of_nodes):
    node_1 = random.choice(list(graph.nodes))
    node_2 = random.choice(list(set(graph.nodes) - {node_1}))
    if graph.has_edge(node_1, node_2) or graph.has_edge(node_2, node_1):
        continue
    else:
        weight = random.randint(0, 10)
        graph.add_weighted_edges_from([(node_1, node_2, weight)])
nx.draw_circular(graph, node_size=30, with_labels=True)
plt.show()

while number_of_random_walks <= 600:
    number_of_random_walks += 200
    random_walk_length = 5
    while random_walk_length <= 100:
        random_walk_length += 1
        pr = IncrementalPersonalizedPageRank(graph, 0, number_of_random_walks, 0.05, random_walk_length)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')

        difference.append(numpy.linalg.norm(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values())))
plt.plot(range(6, 101), difference[0:95], 'r', range(6, 101), difference[96:191], 'g',
         range(6, 101), difference[192:287], 'y')
red_patch = mpatches.Patch(color='red', label='210 Random Walks')
green_patch = mpatches.Patch(color='green', label='410 Random Walks')
yellow_patch = mpatches.Patch(color='yellow', label='610 Random Walks')
plt.legend(handles=[red_patch, green_patch, yellow_patch])
plt.title('Accuracy of Page Ranks')
plt.ylabel('Euclidean Norm')
plt.xlabel('Random Walk Length')
plt.show()

difference_2 = []
number_of_random_walks = 10
random_walk_lengths = [25, 50, 100]
for random_walk_length in random_walk_lengths:
    while number_of_random_walks <= 500:
        number_of_random_walks += 50
        pr = IncrementalPersonalizedPageRank(graph, 0, number_of_random_walks, 0.05, random_walk_length)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')

        difference.append(numpy.linalg.norm(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values())))
plt.plot(range(60, 510, 50), difference[0:9], 'r', range(60, 510, 50), difference[6:15], 'g',
         range(60, 510, 50), difference[16:25], 'y')
red_patch = mpatches.Patch(color='red', label='Random Walk Length: 25')
green_patch = mpatches.Patch(color='green', label='Random Walk Length: 50')
yellow_patch = mpatches.Patch(color='yellow', label='Random Walk Length: 100')
plt.legend(handles=[red_patch, green_patch, yellow_patch])
plt.title('Accuracy of Page Ranks')
plt.ylabel('Euclidean Norm')
plt.xlabel('Number of Random Walks')
plt.show()



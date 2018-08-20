import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy

graph = nx.DiGraph()
number_of_nodes = random.randint(2, 100)
nodes = range(number_of_nodes)
graph.add_nodes_from(nodes)
for _ in range(2*number_of_nodes):
    node_1 = random.choice(list(graph.nodes))
    node_2 = random.choice(list(set(graph.nodes) - {node_1}))
    if graph.has_edge(node_1, node_2) or graph.has_edge(node_2, node_1):
        continue
    else:
        weight = random.randint(0, 10)
        graph.add_weighted_edges_from([(node_1, node_2, weight)])
nx.draw_random(graph, node_size=30)
        pr = IncrementalPersonalizedPageRank(self.graph, 0, 200, 0.05, 50)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')
        print "Random Walks: ", pr.random_walks

        print "Initial Page Ranks: ", "\n", page_ranks, "\n", page_ranks_2
        #print numpy.linalg.norm(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values()))
        for node in pr.graph.nodes:
            self.assertAlmostEqual(page_ranks[node], page_ranks_2[node], 1)
        nx.draw_circular(self.graph, with_labels=True)
        #plt.ion()
        plt.show()
        #plt.pause(5)

        print "Initial Nodes :", self.graph.nodes
        print "Initial Edges :", self.graph.edges

        c = random.randint(self.number_of_nodes//4, self.number_of_nodes//2)
        choices = ["Remove Edge / Add Edge", "Change Edge Weight", "Remove Node / Add Node"]
        for _ in range(c):
            choice = random.choice(choices)
            if choice == "Remove Edge / Add Edge":
                node_1 = random.choice(list(pr.graph.nodes))
                node_2 = random.choice(list(set(pr.graph.nodes) - {node_1}))
                if pr.graph.has_edge(node_1, node_2):
                    pr.remove_edge(node_1, node_2)
                elif pr.graph.has_edge(node_2, node_1):
                    pr.remove_edge(node_2, node_1)
                else:
                    weight = random.randint(-10, 10)
                    pr.add_edge(node_1, node_2, weight)
            elif choice == "Change Edge Weight":
                edge = random.choice(list(pr.graph.edges))
                weight = random.randint(-10, 10)
                pr.add_weight_to_edge(edge[0], edge[1], weight)
            elif choice == "Remove Node / Add Node":
                w = random.randint(0, 1)
                if w == 0:
                    pr.add_node(self.number_of_nodes + 1)
                    self.number_of_nodes += 1
                elif w == 1:
                    node = random.choice(list(set(pr.graph.nodes) - {0}))
                    pr.remove_node(node)

        nx.draw_circular(self.graph, with_labels=True)
        #plt.ion()
        plt.show()
        #plt.pause(5)
        print "Updated Nodes :", self.graph.nodes
        print "Updated Edges :", self.graph.edges

        pr.update_random_walks()
        new_page_ranks = pr.compute_personalized_page_ranks()
        new_page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                       max_iter=500, weight='weight')
        print "New Random Walks: ", pr.random_walks
        print "New Page Ranks: ", "\n", new_page_ranks, "\n", new_page_ranks_2
        #print numpy.linalg.norm(numpy.array(new_page_ranks.values()) - numpy.array(new_page_ranks_2.values()))
        #print page_ranks.keys() == page_ranks_2.keys()
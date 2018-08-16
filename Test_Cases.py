import unittest
import networkx as nx
from Page_Rank import IncrementalPersonalizedPageRank


class Tests(unittest.TestCase):

    def test_page_rank_1(self):
        """
        Test a very simple page rank computation without updating the graph
        """
        self.graph = nx.DiGraph()
        self.nodes = ['a', 'b', 'c']
        self.edges = [('a', 'b', 1), ('a', 'c', 2)]

        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(self.edges)

        pr = IncrementalPersonalizedPageRank(self.graph, 'a', 100, 0.05, 10)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        #print "First Test Pageranks: ", page_ranks
        self.assertTrue('a' in page_ranks)
        self.assertTrue('b' in page_ranks)
        self.assertTrue('c' in page_ranks)
        self.assertEqual(len(pr.random_walks), 100)
        for walk in pr.random_walks:
            self.assertEqual(len(walk), 10)
        self.assertFalse(pr.removed_edges)
        self.assertFalse(pr.added_edges)
        self.assertGreaterEqual(page_ranks['a'], page_ranks['b'])
        self.assertGreaterEqual(page_ranks['a'], page_ranks['c'])

    def test_page_rank_2(self):
        """
        Test page rank and update the graph
        """
        self.graph = nx.DiGraph()
        self.nodes = ['a', 'b', 'c']
        self.edges = [('a', 'b', 1), ('a', 'c', 2)]

        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(self.edges)

        pr = IncrementalPersonalizedPageRank(self.graph, 'a', 100, 0.05, 10)
        pr.initial_random_walks()
        page_ranks_1 = pr.compute_personalized_page_ranks()
        #print "First Page Ranks ", page_ranks_1

        pr.add_node('d')
        pr.add_edge('c', 'd', 2)
        pr.remove_edge('a', 'b')
        pr.remove_node('b')
        pr.add_weight_to_edge('a', 'c', -5)

        self.assertTrue('d' in pr.graph.nodes)
        self.assertTrue(('c', 'd', 2) in pr.added_edges)
        self.assertTrue(('c', 'd') in pr.graph.edges)
        self.assertFalse('b' in pr.graph.nodes)
        self.assertFalse(('a', 'b') in pr.graph.edges)
        self.assertTrue(('a', 'b') in pr.removed_edges)
        self.assertTrue(('c', 'a') in pr.graph.edges)
        self.assertFalse(('a', 'c') in pr.graph.edges)
        for edge in pr.graph.edges:
            self.assertTrue(pr.graph[edge[0]][edge[1]]['weight'] > 0)

        pr.update_random_walks()
        page_ranks_2 = pr.compute_personalized_page_ranks()

        #print "New Page Ranks: ", page_ranks_2

        self.assertFalse(pr.removed_edges)
        self.assertFalse(pr.added_edges)
        self.assertFalse('b' in page_ranks_2)
        self.assertEqual(page_ranks_2['a'], 1)
        self.assertEqual(page_ranks_2['c'], 0)
        self.assertEqual(page_ranks_2['d'], 0)
        self.assertEqual(len(pr.random_walks), 100)
        for walk in pr.random_walks:
            self.assertEqual(len(walk), 10)

    def test_page_rank_3(self):
        """
        We test a personalized page rank on an empty graph
        """
        graph = nx.DiGraph()
        pr = IncrementalPersonalizedPageRank(graph, None, 50, 0.05, 10)
        page_ranks = pr.compute_personalized_page_ranks()
        self.assertEqual(page_ranks, {})

    def test_page_rank_4(self):
        graph = nx.DiGraph()
        nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        edges = [('a', 'c', 3), ('c', 'b', 4), ('b', 'e', 2), ('e', 'f', 1), ('c', 'd', 4), ('d', 'a', 2)]
        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from(edges)

        pr = IncrementalPersonalizedPageRank(graph, 'a', 50, 0, 15)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()

        pr.add_weight_to_edge('c', 'a', 3)
        pr.remove_node('f')
        pr.add_edge('d', 'g', 10)
        pr.add_weight_to_edge('a', 'd', 3)
        pr.add_weight_to_edge('e', 'b', 3)
        pr.update_random_walks()
        new_page_ranks = pr.compute_personalized_page_ranks()

        self.assertFalse(pr.graph.has_edge('a', 'c'))
        self.assertFalse(pr.graph.has_edge('c', 'a'))
        self.assertFalse('f' in new_page_ranks.keys())
        for random_walk in pr.random_walks:
            self.assertEqual(set(random_walk), {'a', 'd', 'g'})

        pr.add_edge('a', 'c', 3)
        pr.add_node('f')
        pr.add_edge('f', 'e', -1)
        pr.remove_edge('d', 'g')
        pr.add_weight_to_edge('e', 'b', -3)
        pr.add_weight_to_edge('d', 'a', 3)

        pr.update_random_walks()
        new_old_page_ranks = pr.compute_personalized_page_ranks()
        print "PR_3: ", pr.random_walks

        self.assertEqual(pr.graph.nodes, graph.nodes)
        self.assertEqual(pr.graph.edges, graph.edges)
        self.assertEqual(page_ranks.keys(), new_old_page_ranks.keys())
        for x, y in zip(page_ranks.values(), new_old_page_ranks.values()):
            self.assertAlmostEqual(x, y, 1)
        self.assertFalse(pr.removed_edges)
        self.assertFalse(pr.added_edges)

    """def test_page_rank_5(self):
        graph = nx.DiGraph()
        nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        edges = [('a', 'b', 1), ('a', 'c', 2), ('c', 'd', 1), ('b', 'd', 3), ('d', 'e', 10), ('e', 'f', 1)]
        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from()"""


if __name__ == '__main__':
    unittest.main()











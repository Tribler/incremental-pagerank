"""
The code below opens the multi-chain database and generates a graph of nodes corresponding to peers in the network
and edges representing the flow of data in between peers
"""
import sqlite3
import networkx as nx
import copy


class GraphReduction(object):
    """
    Class to open the multichain data set file consisting of tables, comprising the columns: public_key_requester,
    public_key_responder, up, down, total_up_requester, total_down_requester, sequence_number_requester,
    previous_hash_requester, signature_requester, hash_requester, total_up_responder, total_down_responder,
    sequence_number_responder, previous_hash_responder, signature_responder and hash_responder.

    A directed graph is then generated with nodes corresponding to the public_key of peers in the network and edges
    representing interactions between individual peers. The weight of an edge connecting to peers is determined by
    the net flow of data in between these peers. The direction of an edge is determined by the sign of the net flow,
    i.e. if a has transferred 3GB to b and b has transferred 1GB to a, then the graph will have a directed edge from
    a to b of weight 2GB.
    """

    def __init__(self, path, file_name, opening_row, closing_row):
        """
        Initializes the graph reduction class
        :param path: location of the data set
        :param file_name: name of the file
        :param opening_row: first row of multichain table that is loaded
        :param closing_row: last row of multichain table that is loaded
        """
        self.path = path
        self.file_name = file_name
        self.opening_row = opening_row
        self.closing_row = closing_row
        self.number_of_rows = self.closing_row - self.opening_row
        self.blocks = []
        self.graph = nx.DiGraph()

    def open_data_set(self):
        """
        Opens the multi chain data base file and selects the given rows from the multi_chain table
        """
        conn = sqlite3.connect(self.path + self.file_name + ".db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM multi_chain LIMIT 500 OFFSET;""")  # Number of rows: 1328229
        self.blocks = cursor.fetchall()
        self.blocks = [list(block) for block in self.blocks]
        for i in xrange(len(self.blocks)):
            for j in iter(list(set(range(len(self.blocks[i]))) - {2, 3, 4, 5, 6, 10, 11, 12, 16})):  # list(set(range(len(self.blocks[i])))
                self.blocks[i][j] = str(self.blocks[i][j]).encode('hex')
        self.blocks = [tuple(block) for block in self.blocks]
        conn.close()
        return

    def generate_graph(self):
        """
        Generates a graph from the multichain blocks. Each node corresponds to a public key. The edge weights
        represent the net data flow in between two nodes
        :return:
        """
        requesters = set(self.blocks[i][0] for i in range(len(self.blocks)))
        responders = set(self.blocks[i][1] for i in range(len(self.blocks)))
        nodes = list(requesters.union(responders))

        del responders
        del requesters

        double_edges = [(node_1, node_2) for node_1 in nodes for node_2 in nodes if node_1 != node_2]
        double_edges = dict(zip(double_edges, [0]*len(double_edges)))
        for block in iter(self.blocks):
            double_edges[(block[0], block[1])] += block[2] - block[3]
            double_edges[(block[1], block[0])] += block[3] - block[2]

        directed_edges = copy.copy(double_edges)

        del double_edges

        directed_edges = dict(filter(lambda x: x[1] > 0, directed_edges.items())) # Returns all edges with positive edge weights
        edges = []
        for directed_edge in iter(directed_edges.keys()):
            edges.append(directed_edge + (directed_edges[directed_edge],))

        del directed_edges

        self.graph.add_nodes_from(nodes)
        self.graph.add_weighted_edges_from(edges)

        return

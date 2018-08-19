"""
The code below opens the multi-chain database and generates a graph of nodes corresponding to peers in the network
and edges representing the flow of data in between peers
"""
import sqlite3
import networkx as nx


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

    def open_data_set(self):
        """
        Opens the multi chain data base file and selects the given rows from the multi_chain table
        :return:
        """
        conn = sqlite3.connect(self.path + self.file_name + ".db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM multi_chain LIMIT 1000 OFFSET 1;""")
        #cursor.execute("""SELECT * FROM multi_chain LIMIT str(self.closing_row) OFFSET str(self.opening_row);""")
        transactions = cursor.fetchall()
        transactions = [list(transaction) for transaction in transactions]
        for i in range(len(transactions)):
            for j in list(set(range(len(transactions[i]))) - {2, 3, 4, 5, 6, 10, 11, 12, 16}):
                transactions[i][j] = str(transactions[i][j]).encode('hex')
        transactions = [tuple(transaction) for transaction in transactions]
        conn.close()
        return transactions

    def generate_graph(self, transactions):
        graph = nx.Digraph()
        requesters = set(transactions[i][0] for i in range(len(transactions)))
        responders = set(transactions[i][1] for i in range(len(transactions)))
        nodes = requesters.union(responders)
        edges = [(node_1, node_2) for node_1, node_2 in nodes if node_1 != node_2]
        edges = dict(zip(edges, [0]*len(edges)))
        for transaction in transactions:
            edges[(transaction[0], transaction[1])] += transaction[2] - transaction[3]

        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from(edges)



        graph.add_nodes_from(nodes)






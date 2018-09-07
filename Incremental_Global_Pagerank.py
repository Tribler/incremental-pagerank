# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 15:04:18 2018

@author: Alexander
"""

import networkx as nx
import sqlite3
import random
import copy
import timeit
import matplotlib.pyplot as plt


#Open Multichain Database 
path="C:\\Users\\alexa\\Documents\\TU Delft\\Course material\\Other\\Blockchain\\Blockchain Lab\\Incremental Pagerank\\"
filepath=path+"multichain_09_02_18.db"
conn=sqlite3.connect(filepath)
cursor=conn.cursor()
#%%

def open_lines(x,y): 
    #cursor.execute("SELECT * FROM multi_chain LIMIT 100 OFFSET 0;""")
    cursor.execute("""SELECT * FROM multi_chain;""" )#Number of rows: 1328229
    rows=cursor.fetchall()
    rows=[list(elem) for elem in rows]
    blocks=[rows[i] for i in range(x,y)]
    
    for k in range(len(blocks)):       
        blocks[k][0]=str(blocks[k][0]).encode('hex')
        blocks[k][1]=str(blocks[k][1]).encode('hex')
        blocks[k][7]=str(blocks[k][7]).encode('hex')
        blocks[k][8]=str(blocks[k][8]).encode('hex')
        blocks[k][9]=str(blocks[k][9]).encode('hex')
        blocks[k][13]=str(blocks[k][13]).encode('hex')
        blocks[k][14]=str(blocks[k][14]).encode('hex')
        blocks[k][15]=str(blocks[k][15]).encode('hex')
    blocks=[tuple(elem) for elem in blocks]
    return blocks



#%%
def generate_graph_2(blocks):
    Graph=nx.DiGraph()
    for block in blocks:
        pubkey_requester=block[0]
        pubkey_responder=block[1]
        sequence_number_requester=block[6]
        sequence_number_responder=block[12]
        value_exchange=block[3]-block[4]
        Graph.add_edge((pubkey_requester,sequence_number_requester),(pubkey_requester,sequence_number_requester + 1), contribution=value_exchange)
        Graph.add_edge((pubkey_requester,sequence_number_requester),(pubkey_responder,sequence_number_responder + 1), contribution=value_exchange)
        Graph.add_edge((pubkey_responder,sequence_number_responder),(pubkey_responder,sequence_number_responder + 1), contribution=value_exchange)
        Graph.add_edge((pubkey_responder,sequence_number_responder),(pubkey_requester,sequence_number_requester + 1), contribution=value_exchange)
    return Graph



#%% 
def random_walk_from_node(Graph,node,reset_probability):
    random_walk=[node]
    c=random.uniform(0,1)
    while len(list(Graph.neighbors(random_walk[-1])))>0 and c>reset_probability:
        random_walk.append(random.choice(list(Graph.neighbors(random_walk[-1]))))
        c=random.uniform(0,1)
    return random_walk


    
def random_walk_of_network(Graph,reset_probability):
    random_walk=[]
    for node in Graph.nodes:
        temp_random_walk=random_walk_from_node(Graph,node,reset_probability)
        random_walk.append(temp_random_walk)
    return random_walk



def multiple_random_walks_of_network(number_of_random_walks,Graph,reset_probability):
    random_walks=[]
    nodes_in_random_walks=[]
    for i in range(number_of_random_walks):
        random_walks.append(random_walk_of_network(Graph,reset_probability))
        for j in range(len(Graph.nodes)):
            nodes_in_random_walks.extend(random_walks[i][j])
    return nodes_in_random_walks



def visit_times_of_multiple_random_walks_of_network(nodes_in_random_walks, Graph):
    zeros=[0 for _ in range(len(list(Graph.nodes)))]
    visit_times=dict(zip(list(Graph.nodes),zeros))
    for node in Graph.nodes:
        #visit_times.append(nodes_in_random_walks.count(node))
        visit_times[node]=nodes_in_random_walks.count(node)
    return visit_times



def compute_global_pageranks(Graph,reset_probability,number_of_random_walks):
    zeros=[0 for _ in range(len(list(Graph.nodes)))]
    global_pageranks=dict(zip(list(Graph.nodes),zeros))
    nodes_in_random_walks=multiple_random_walks_of_network(number_of_random_walks,Graph,reset_probability) 
    visit_times=visit_times_of_multiple_random_walks_of_network(nodes_in_random_walks,Graph)
    #for i in range(len(visit_times)):
    for node in Graph.nodes:
        global_pageranks[node]=float(visit_times[node])/sum(visit_times.values())
    return nodes_in_random_walks,visit_times,global_pageranks



def compute_incremental_global_pageranks(old_Graph,new_Graph,reset_probability,number_of_random_walks):
    [old_nodes_in_random_walks,old_visit_times,old_global_pageranks]=compute_global_pageranks(old_Graph,reset_probability,number_of_random_walks)
    new_visit_times=copy.deepcopy(old_visit_times)
    zeros=[0 for _ in range(len(list(new_Graph.nodes)))]
    new_global_pageranks=dict(zip(list(new_Graph.nodes),zeros))
    
    
    
    for node in old_Graph.nodes:
        if node not in new_Graph.nodes:
            del new_visit_times[node]
    for node in new_Graph.nodes:
        if node not in old_Graph.nodes:
            new_visit_times[node]=0
    
    
    
    
    for node1 in list(set(new_Graph.nodes)-set(old_Graph.nodes)):
        for i in range(number_of_random_walks):
            random_walk = random_walk_from_node(new_Graph,node1,reset_probability)
            for node2 in random_walk:
                new_visit_times[node2]+=1
                
    
    
    updated_nodes=[]
    

    for edge in list(set(new_Graph.edges)-set(old_Graph.edges)):
        if edge[0] in old_Graph.nodes:
            M=(1-reset_probability)*new_visit_times[edge[0]]/(len(list(set(new_Graph.neighbors(edge[0])).union(set(old_Graph.neighbors(edge[0]))))))
            if len(list(old_Graph.neighbors(edge[0])))==0:
                N=0
            else:
                N=float(M)/len(list(old_Graph.neighbors(edge[0])))
            updated_nodes.append([edge[1],M,1])
            for node in old_Graph.neighbors(edge[0]):
                    updated_nodes.append([node,N,1])
    
    
    
    for edge in list(set(old_Graph.edges)-set(new_Graph.edges)):
        if edge[0] in new_Graph.nodes:
            M=(1-reset_probability)*new_visit_times[edge[0]]/(len(list(set(new_Graph.neighbors(edge[0])).union(set(old_Graph.neighbors(edge[0]))))))
        else:
            M=(1-reset_probability)*old_visit_times[edge[0]]/(len(list(old_Graph.neighbors(edge[0]))))                
        updated_nodes.append([edge[1],M,-1])
        if edge[0] not in new_Graph.nodes:
            N=0
        elif len(list(new_Graph.neighbors(edge[0])))==0:
            N=0
        else: N=float(M)/len(list(new_Graph.neighbors(edge[0])))
        if edge[0] in new_Graph:
            for node in new_Graph.neighbors(edge[0]):
                updated_nodes.append([node,N,-1])
    
    
    
    for updated_node in updated_nodes:
        if updated_node[2]==1:
            if updated_node[0] in new_Graph:
                for _ in range(int(updated_node[1])):
                    random_walk=random_walk_from_node(new_Graph,updated_node[0],reset_probability)
                    for node in random_walk:
                        new_visit_times[node]+=1
        else:# updated_node[2]==-1:
            if updated_node[0] in new_Graph:
                for _ in range(int(updated_node[1])):
                    random_walk=random_walk_from_node(new_Graph,updated_node[0],reset_probability)
                    for node in random_walk:
                        new_visit_times[node]-=1
                        
    
    for node in new_Graph.nodes:
        new_global_pageranks[node]=float(new_visit_times[node])/sum(new_visit_times.values())
    
    
    
    return old_global_pageranks,new_global_pageranks


        
#%%
def test_incremental_global_pagerank_on_mutlichain_data():
    reset_probability=0.15
    number_of_random_walks=10


    old_blocks=open_lines(0,885486) 
    new_blocks=open_lines(442753,1328229)


    old_Graph=generate_graph_2(old_blocks)
    nx.draw_random(old_Graph, node_size=50)
    plt.show()
    
    
    new_Graph=generate_graph_2(new_blocks)
    nx.draw_random(new_Graph, node_size=50)
    plt.show()

    old_and_new_global_pageranks=compute_incremental_global_pageranks(old_Graph,new_Graph,reset_probability,number_of_random_walks)


    old_global_pageranks=old_and_new_global_pageranks[0]
    new_global_pageranks=old_and_new_global_pageranks[1]

    print "Old global pageranks: ", old_global_pageranks
    print "New global pageranks: ", new_global_pageranks

     
time=timeit.timeit(test_incremental_global_pagerank_on_mutlichain_data,number=1)
print 'time: ', time, 'seconds'

#%%
#Testing the global incremental pagerank algorithm 
def test_incremental_global_pagerank_1():
    old_nodes=['a','b','c','d','e','f','g','h','i']
    new_nodes=['b','c','d','e']
    
    old_edges=[('a','b'),('b','c'),('c','d'),('d','e'),('e','f'),('f','g'),('g','h'),('h','i')]
    new_edges=[('b','c'),('c','d'),('d','e')]
    
    old_Graph=nx.DiGraph()
    old_Graph.add_nodes_from(old_nodes)
    old_Graph.add_edges_from(old_edges)
    
    new_Graph=nx.DiGraph()
    new_Graph.add_nodes_from(new_nodes)
    new_Graph.add_edges_from(new_edges)

    reset_probability=0.15  
    number_of_random_walks=100
    
    
    old_and_new_pageranks=compute_incremental_global_pageranks(old_Graph,new_Graph,reset_probability,number_of_random_walks)
    print 'Old Pageranks: ', old_and_new_pageranks[0]
    print 'New Pageranks: ', old_and_new_pageranks[1]
    



time=timeit.timeit(test_incremental_global_pagerank_1,number=1)  
print 'time: ', time, 'seconds' 
#%%

def test_incremental_global_pagerank_2():
    old_number_nodes=random.randint(1,50)
    old_nodes=[i for i in range(1,old_number_nodes)]
    

    old_max_number_edges=old_number_nodes*(old_number_nodes-1)
    old_min_number_edges=0
    old_number_edges=random.randint(old_min_number_edges,old_max_number_edges)

    old_edges=[]
    for i in range(0,old_number_edges):
        x=random.choice(old_nodes)
        y=random.choice(old_nodes)
        if (x,y) not in old_edges:
            old_edges.append((x,y))
        else: 
            continue

    old_Graph=nx.DiGraph()
    old_Graph.add_nodes_from(old_nodes)
    old_Graph.add_edges_from(old_edges)
    nx.draw_random(old_Graph, node_size=50)
    
    new_number_nodes=random.randint(1,50)
    new_nodes=[i for i in range(1,new_number_nodes)]
    

    new_max_number_edges=new_number_nodes*(new_number_nodes-1)
    new_min_number_edges=0
    new_number_edges=random.randint(new_min_number_edges,new_max_number_edges)

    new_edges=[]
    for i in range(0,new_number_edges):
        x=random.choice(new_nodes)
        y=random.choice(new_nodes)
        if (x,y) not in new_edges:
            new_edges.append((x,y))
        else: 
            continue

    new_Graph=nx.DiGraph()
    new_Graph.add_nodes_from(new_nodes)
    new_Graph.add_edges_from(new_edges)
    nx.draw_random(new_Graph,node_size=50)

    
    reset_probability=0.15  
    number_of_random_walks=100
    
    
    old_and_new_pageranks=compute_incremental_global_pageranks(old_Graph,new_Graph,reset_probability,number_of_random_walks)
    print 'Old Pageranks: ', old_and_new_pageranks[0]
    print 'New Pageranks: ', old_and_new_pageranks[1]




time=timeit.timeit(test_incremental_global_pagerank_2,number=1)
print 'time: ', time, 'seconds'         
#%%
def test_incremental_global_pagerank_3():
    old_nodes=['a','b','c','d','e','f','g','h','i']
    new_nodes=old_nodes
    
    old_edges=[('a','b'),('b','c'),('c','d'),('d','e'),('e','f'),('f','g'),('g','h'),('h','i'),('i','a')]
    new_edges=list(set(old_edges)-{('i','a')})
    
    
    old_Graph=nx.DiGraph()
    old_Graph.add_nodes_from(old_nodes)
    old_Graph.add_edges_from(old_edges)
    
    new_Graph=nx.DiGraph()
    new_Graph.add_nodes_from(new_nodes)
    new_Graph.add_edges_from(new_edges)
    
    reset_probability=0.15
    number_of_random_walks=5000
    
    
    old_and_new_pageranks=compute_incremental_global_pageranks(old_Graph,new_Graph,reset_probability,number_of_random_walks)
    print 'Old PageRanks: ', old_and_new_pageranks[0]
    print 'New PageRanks: ', old_and_new_pageranks[1]
    
time=timeit.timeit(test_incremental_global_pagerank_3,number=1)
print 'Time: ', time, 'seconds'
#%%
def test_incremental_global_pagerank_4():
    old_nodes=['a','b','c','d']
    new_nodes=['a','b','c','d']
    
    old_edges=[('a','b'),('b','c'),('c','a'),('b','d'),('d','c')]
    #new_edges=list(set(old_edges).union({('b','d'),('d','c')}))
    new_edges=old_edges
    old_Graph=nx.DiGraph()
    old_Graph.add_nodes_from(old_nodes)
    old_Graph.add_edges_from(old_edges)
    
    new_Graph=nx.DiGraph()
    new_Graph.add_nodes_from(new_nodes)
    new_Graph.add_edges_from(new_edges)
    
    nx.draw_random(new_Graph,nodesize=50)
    
    reset_probability=0.15
    number_of_random_walks=5000
    
    old_and_new_pageranks=compute_incremental_global_pageranks(old_Graph,new_Graph,reset_probability,number_of_random_walks)
    print 'Old PageRanks: ', old_and_new_pageranks[0]
    print 'New PageRanks: ', old_and_new_pageranks[1]
    
    
    
    
test_incremental_global_pagerank_4()















 







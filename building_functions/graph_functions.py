
# coding: utf-8

# ## Graph related functions
# 
# A graph is represented by an adjacency matrix $A$ such that 
# $$ A[u][v] = m \; \mbox{ if there is an edge of multiblicity $m$ between $u$ and $v$}$$
# 
# We can generate a random graph:
# - with given maximum degree
# - with given number of edges

# In[1]:

from random import random


# In[2]:

def generate_graph_max_deg(num_v, max_deg):
    adj_mat = [[0 for u in range(num_v)] for v in range(num_v)]
    degs = [0 for v in range(num_v)]
    
    while (max(degs)<max_deg):
        # pick a new edge
        u = int(random()*num_v)
        v = int(random()*num_v)
        while(u == v):
            v = int(random()*num_v)
            
        adj_mat[u][v] += 1
        adj_mat[v][u] += 1
        
        degs[u] += 1
        degs[v] += 1
        
    return adj_mat


    
def generate_graph_max_edges(num_v, max_edges):
    adj_mat = [[0 for u in range(num_v)] for v in range(num_v)]
    
    count = 0
    
    while (count<max_edges):
        # pick a new edge
        u = int(random()*num_v)
        v = int(random()*num_v)
        while(u == v):
            v = int(random()*num_v)
            
        adj_mat[u][v] += 1
        adj_mat[v][u] += 1
        
        count += 1

    return adj_mat
    


# - Return degree sequence, given the adjacency matrix

# In[3]:

def get_deg_seq(adjacency_matrix):
    return [sum(s) for s in adjacency_matrix]


# - Get adjacency matrix of the induced subgraph on the given set of vertices

# In[4]:

def induced_subgraph_adjacency_matrix(vertices, adjacency_matrix):
    new_n = len(vertices)
    new_adj_mat = [[0 for __ in range(new_n)] for _ in range(new_n)]
    for i in range(new_n):
        v = vertices[i]
        for j in range(i+1, new_n):
            u = vertices[j]
            new_adj_mat[i][j] = adjacency_matrix[v][u] 
            new_adj_mat[j][i] = adjacency_matrix[u][v]
    return new_adj_mat


# ## MAX-algorithm
# 
# __remove_vertes_of_highest_degree:__ returns the adjacency matrix of the graph obtained by deleting (any) vertex of maximum degree in the given graph
# 
# __MAX_move:__ if there is a vertex of degree at least $k$, then remove a vertex of the highest degree and return the degree sequence of the obtained graph. otherwise, return the degree sequence of the original graph.

# In[5]:

def remove_vertex_of_highest_degree(adjacency_matrix):
    degs = get_deg_seq(adjacency_matrix)
    num_v = len(adjacency_matrix)
    
    ### get vertices of max deg
    max_deg = max(degs)
    max_deg_v = [v for v in range(num_v) if degs[v]==max_deg]
    
    ### pick a random vertex of max deg
    v = max_deg_v[int(random()*len(max_deg_v))]
    ### delete v
    new_mat = [adjacency_matrix[u][0:v]+adjacency_matrix[u][v+1:num_v] for u in range(num_v) if u!= v]
    
    return new_mat

def MAX_move(adjacency_matrix, k):
    degs = get_deg_seq(adjacency_matrix)
    if max(degs)<k:
        return sorted(degs)
    else:
        new_mat = remove_vertex_of_highest_degree(adjacency_matrix)
        return sorted(get_deg_seq(new_mat))
    
def get_b_MAX(adjacency_matrix, k):
    new_mat = [row for row in adjacency_matrix]
    deg_seq = get_deg_seq(new_mat)
    
    while max(deg_seq)>=k:
        new_mat = remove_vertex_of_highest_degree(new_mat)
        deg_seq = get_deg_seq(new_mat)
    return len(deg_seq)    


# ## Criterion for a sequence to be multi-graphical

# In[1]:

def is_multigraphical(D):
    n = len(D)
    return D[-1] <= sum(D[0:n-1])


# In[ ]:





# coding: utf-8

# ## Exploratory analysis

# In[4]:

from jelen_triesch_argument.kIndependence_functions import * 
from building_functions.graph_functions import * 
from building_functions.aux_functions import *


# * __Are $(i,j)$-steps well defined?__ Make a random graph. Let $D$ be a sequence obtained by one applicatin of $\omega$ operator. Let $E$ be a sequence obtained by one application of MAX-algorithm. Verify if $D$ can be obtaine from $E$ by our $(i,j)$-steps. That is, verify if $D \leq E$.

# In[5]:

max_count = 100

print 'counter-examples:'

for v in range(5, 30):
    for num_e in range(2, v*(v-1)):
        for count in range(max_count):
            adj_mat = generate_graph_max_edges(v, num_e)
            degs = sorted(get_deg_seq(adj_mat))
            k = 1+int(random()*degs[-1])

            D = omega(degs, k)
            E = MAX_move(adj_mat, k)
            
            if equalize_sequence_random(D,E,k)==0:
                print 'error'
                print 'k=', k, 'D:', D, 'E:', E, 'orig:', degs
                print ''
print ''
print 'done'


# * __Claim:__ If $D$ and $E$ are multigraphical $D \leq E$ , then $b(D) \leq b(E)$. 

# In[3]:

def get_random_vals(num_e):
    D = random_integer_partition(num_e,1)
    E = random_integer_partition(num_e,1)
    k = 1+int(random()*max(max(D), max(E)))

    n1 = len(D)
    n2 = len(E)
    if n1<n2:
        D = add_zeros(D, n2)
    elif n1>n2:
        E = add_zeros(E, n1)
    return [D,E,k]


# In[4]:

num_good_partitions = 100

print 'counter-examples:'

for num_e in range(10,51,2):
    for count in range(num_good_partitions):  
        D,E,k = get_random_vals(num_e)
        while D[-1]>(num_e/2) or E[-1]>(num_e/2) or equalize_sequence_random(D,E,k)==0:
            D,E,k = get_random_vals(num_e)
                          
        bD = get_b(D,k)
        bE = get_b(E,k)
        if bD>bE:
            print 'k=', k, 'D=', D, 'E=', E  
            print 'b(D)=', bD, 'b(E)=', bE 
print ''
print 'done'        


# - __Claim:__ If $D$ and $E$ are multi-graphical and $D \leq E$ then $\mathcal{E}(D) \leq \mathcal{E}(E)$. 
# 
# It is enought to prove the claim if $E$ is obtaine from $D$ by a single $(i,j)$-step. The following code verifies this claim.

# In[5]:

num_good_partitions = 100
num_tries = 100

print 'counter-examples:'

for num_e in range(10,31,2):
    for count in range(num_good_partitions):
        D = random_integer_partition(num_e,1)
        D = sorted(D)
        n = len(D)
        if sum(D[0:n-1])>=D[-1]: ## is graphical?
            for k in range(1,max(D)+1):
                ED = elimination_sequence(D,k)
                
                for count2 in range(num_tries):
                    i = int(random()*n)
                    j = i
                    while (j==i):
                        j = int(random()*n)
                    E = [d for d in D]
                    E = i_j_step(E,i,j,k)
                    
                    EE = elimination_sequence(E,k)
                    
                    if (sum(ED)!=sum(EE)) or (equalize_sequence_random(sorted(EE),sorted(ED),k)==0):
                        print 'k=', k, 'E:', E, 'D:', D
                        print 'EE:', EE, 'ED:', ED 
                        print ''
print ''
print 'done'


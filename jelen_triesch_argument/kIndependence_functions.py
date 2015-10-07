
# coding: utf-8

# ## Operators related to $k$-Independence
# 
# Let $D = [d_0, d_1, \dots, d_{n}]$ be a sequence of length $n+1$ such that $d_0 \leq d_1 \leq \dots \leq d_{n-1}$.
# 
# __Omega operator__ $\omega(D,k)$ consists of $d_n$ consequtive applications of legal decrements performed starting with sequence $D' = [d_0, d_1, \dots, d_{n-1}]$ of length $n$. 
# 
# __A legal decrement__ of a non-decreasing sequence $D'$ for given $k$: 
# 
# Decrement $d_i := d_i -1$ where $i$ is determined as follows:
# - if $\sum_{j=0}^{n-2} d_j < d_{n-1}$, then $i = n-1$ in order for the sequence to remain graphical; 
# - if $d_{n-1} > k$, then decrement a vertex with the highest degree choosing $i$ such that the sequence remains sorted;
# - if $d_{n-1} \leq k$, then decrement a vertex with the smallest non-zero degree, keep sequence sorted.
#  
# 

# In[1]:

def legal_decrement(D,k):
    n = len(D)
    i = 0
    
    if sum(D[0:n-1])<D[-1]:
        i = n-1
    elif D[-1]>k:
        i=n-1
        while i>0 and D[i-1]==D[-1]:
            i -= 1
    else:
        i = 0
        while i<n and D[i]==0:
            i += 1
    if i<0 or i==n:
        print 'error: legal decrement could not be performed'
        print 'k=', k, 'D=', D
    else:    
        D[i] -= 1   

def omega(D, k):
    n = len(D)
    new_D = [D[v] for v in range(n-1)]
    for v in range(D[-1]):
        legal_decrement(new_D, k)
    return new_D        


# __Value b__: $b(D,k)$ is the length of a sequence obtained after consecutive applications of omega operator starting with sequence $D$ and terminating when all values in the sequence are strictly smaller than $k$.

# In[2]:

def get_b(D_input,k):
    D = [v for v in D_input]
    while max(D)>= k:
        D = omega(D,k)   
    b = len(D)
    return b 


# ## $(i,j)-$step and goind between two sequences
# 
# Let $E = [e_l]$ be a non-decreasing sequence, and let $i$ and $j$ be indices of two elements in the sequence, $i<j$. Then 
# - if $e_j > k$ and $e_j-e_i \geq 2$, then decrement $e_j$ and increment $e_i$
# - if $e_j < k$ and $e_i > 0$, then increment $e_j$ and decrement $e_i$.
# 
# __Definition:__ Let $D=[d_l]$ and $E=[e_l]$ be two non-decreasing sequences. Then $D \leq E$ if the following hold:
# - $ \sum d_l = \sum e_l$
# - starting from $E$, we can obtain $D$ by a finite sequence of $(i,j)$-steps.

# In[3]:

def i_j_step(E,i,j,k):
    ''' adjust E at vertices i and j'''
    if i==j:
        return 
    elif j<i: # make sure that i<j
        temp = i
        i = j
        j = temp

    if (E[j] > k) and (E[j]-E[i] >= 2):
        E[j] -= 1
        E[i] += 1
    elif (E[j] < k) and (E[i] > 0):
        E[i] -= 1
        E[j] += 1
    return sorted(E)


# Assume we are given two sequences $D=[d_l]$ and $E=[e_l]$ such that $$\sum_l d_l = \sum_l e_l. $$ We want to determine if we can use $(i,j)$-steps to reduce sequence $E$ to sequence $D$. We can try to do so:
# 1. deterministically
# 2. randomly
# 
# Output is a binary value.
# $$
# \mbox{return} := \left\{ \begin{array}{ll}
# 1, & \mbox{successfully equalized sequences} \\
# 0, & \mbox{otherwise}. \end{array}\right. 
# $$
# 
# __Deterministically:__ We can choose $i$ to be the smallest index at which sequence $D$ and $E$ differe and $j$ to be the greatest index at which $D$ and $E$ differ. Try to perfom an $(i,j)$-step for such choice of $i$ and $j$ at most $10 \sum_l d_l$ times (somewhat arbitrary choice of the maximum number of iterations).

# In[4]:

def legal_step_deterministic(D,E,k):
    ''' guide E towards D '''
    n = len(D)
    
    j = n-1
    i = -1
    while j>=0 and E[j]==D[j]:
        j -= 1
    if j== -1:
        return E
    i = j-1
    while i>=0 and E[i]==D[i]:
        i -= 1
    if i == -1:
        return E
    return i_j_step(E,i,j,k)

def equalize_sequence_deterministic(D_in,E_in,k):
    max_count = 10*sum(D_in)
    E = [v for v in E_in]
    D = D_in
    count = 0
    
    if max_count == 0: ### D and E are zero sequences
        return 1
   
    while count<max_count and D!=E and E!=[]:
        E = legal_step_deterministic(D,E,k)
        count += 1
    if count == max_count or E==[]:
        return 0
    else:
        return 1  


# __Randomly:__ We can pick random values for $i$ and $j$ at which we perform $(i,j)$-step. The only consideration is that $d_i > e_i$ and $d_j < e_j$, so that we have two indices one of which needs to be decremented and the other needs to be incremented.

# In[5]:

from random import random

def legal_step_random(D,E,k):
    ''' guide E towards D '''
    
    n = len(D)    
    j = -1
    i = -1
    while j<0:
        j = int(random()*n)
        if (E[j] <= D[j]):
            j = -1
    while i<0:
        i = int(random()*n)
        if (E[i] >= D[i]):
            i = -1
    return i_j_step(E,i,j,k)

def equalize_sequence_random(D_in,E_in,k):
    max_count1 = 3*sum(D_in) ## number of times to try to find i and j for legal decrement
    max_count2 = 5 ## number of times to start over and try to equalize from the beginning

    out_count = 0
    while out_count<max_count2:
        E = [v for v in E_in]
        D = D_in
        count = 0
        
        if max_count1 == 0: ### D and E are zero sequences
            return 1
       
        while count<max_count1 and D!=E and E!=[]:
            E = legal_step_random(D,E,k)
            count += 1
        if D==E:
            return 1
        else:
            out_count += 1
    return 0   


# ## Elimination sequence
# 
# Given a non-decreasing sequence $D=[d_l]$, let $\mathcal{E}(D) = [d^i]$ be the $\omega$-elimination sequence of $D$ such that $d^i$ is the number of legal decrements performed in the $i^{th}$ application of $\omega$-operator starting with sequence $D$, and terminating with an empty sequence. 
# 
# **Claim:** $b(D)=b(\mathcal{E}(D))$.
# 
# To evaluate the claim, function **get_b_from_ED** computes $b(\mathcal{E}(D))$.

# In[6]:

def elimination_sequence(D_input,k):
    D = [v for v in D_input]
    n = len(D)
    ED = [D[-1]]
    for _ in range(n-1):
        D = omega(D,k)         
        ED.append(D[-1])
    return ED   

def get_b_from_ED(D,k):
    ## get ED
    ED = elimination_sequence(D,k)
    
    ## go in reverse and count num of degs < k
    b = 0
    n = len(D)
    for m in range(len(ED)):
        if ED[n-1-m] < k:
            b += 1
        else:
            break
    return b


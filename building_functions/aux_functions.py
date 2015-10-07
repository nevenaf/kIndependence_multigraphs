
# coding: utf-8

# ## Auxiliary functions
# 
# - Add zeros to the beginning of a sequence to get a desired length. Useful for equalizeing length of equence. 

# In[1]:

def add_zeros(D_in, new_length):
    n = len(D_in)
    D = [0 for _ in range(new_length-n)] + [v for v in D_in]
    return D


# - Random integer partition of $n$ with smaller part being at least min_i -- Not so good. Gives a sequence with many 1s. 
# 

# In[2]:

from numpy.random import geometric
from math import ceil,exp,sqrt

def random_integer_partition(n, min_i):
    p = []
    
    x = float(exp(-3.14/sqrt(6.0*float(n))))
    
    good = False
    while not good:
        z = [0 for i in range(min_i-1)]
        z = z+[geometric(1-pow(x,i+1))-1 for i in range(min_i-1, n)]
        sum = 0 
        for i in range(min_i-1, n):
            sum = sum + (i+1)*z[i]
        good = sum==n
    
    p = [i+1 for i in range(n) for _ in range(z[i])]
    return p


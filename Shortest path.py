#!/usr/bin/env python
# coding: utf-8

# In[1]:


from io import StringIO
import numpy as np
import pandas as pd
latitude_longitude_csv_str ="""city,latitude,longitude
London,51.5072,-0.1275
Birmingham,52.48,-1.9025
Manchester,53.4794,-2.2453
Leeds,53.7997,-1.5492
Newcastle,55.0077,-1.6578
Birstall,52.6736,-1.12
Glasgow,55.8609,-4.2514
Liverpool,53.4,-2.9833
Portsmouth,50.8058,-1.0872
Southampton,50.9,-1.4
Nottingham,52.95,-1.15
Bristol,51.45,-2.5833
Sheffield,53.3833,-1.4667
Kingston upon Hull,53.7444,-0.3325
Leicester,52.6333,-1.1333
Edinburgh,55.953,-3.189
Caerdydd,51.4833,-3.1833
Stoke-on-Trent,53,-2.1833
Coventry,52.4081,-1.5106
Reading,51.4542,-0.9731\
"""
latitude_longitude_pd = pd.read_csv(StringIO(latitude_longitude_csv_str), index_col='city')
latitude_longitute_deg = latitude_longitude_pd[['latitude', 'longitude']].to_numpy()


# In[2]:


display(latitude_longitude_pd)


# In[3]:


display(latitude_longitute_deg)


# In[7]:


import numpy as np
def ll_to_distance_matrix(latitude_longitute_deg):
  la_lo_rad = np.pi * latitude_longitute_deg / 180.0
  la, lo = la_lo_rad[:, 0], la_lo_rad[:, 1]
  earth_radius = 6370.0
  distance_matrix = earth_radius * np.arccos(np.sin(la[:, np.newaxis]) * np.sin(la[np.newaxis, :]) + np.cos(la[:, np.newaxis]) * np.cos(la[np.newaxis, :]) * np.cos(lo[:, np.newaxis] - lo[np.newaxis, :]))
  return distance_matrix


# In[8]:


from networkx import from_numpy_matrix
from networkx.algorithms.tree.mst import minimum_spanning_tree
from networkx.algorithms.traversal.depth_first_search import dfs_preorder_nodes

def tsp_from_ll(latitude_longitute_deg, city_list):

  m= from_numpy_matrix(ll_to_distance_matrix(latitude_longitute_deg))
  t = minimum_spanning_tree(m)  # minimum spanning tree from matrix 
  lst_dfs = list(dfs_preorder_nodes(t, source= 0)) # DFS_MST start from London 
  lst_dfs_circuit = list(dfs_preorder_nodes(t, source= 0))
  lst_dfs_circuit.append(0)  # DFS_MST includes London as start and end point

  ordered_city_list = [] # empty list for names of the cities in correct order
  total_distance = 0 # length of the circuit

  # using list without London at the end to display city names 
  for c in lst_dfs: # c is number that represents city 
    ordered_city_list.append((list(latitude_longitude_pd.index))[c])
    # adding to the empty list names of the cities for every c city in order list lst_dfs 
    # accessed through given city list 

    # below using list with London as start and end point 
  for x in lst_dfs_circuit[0:-1]: #x is number that represents city 
    total_distance += ll_to_distance_matrix(latitude_longitute_deg)[x][lst_dfs_circuit[lst_dfs_circuit.index(x)+1]]
    # access through matrix to get all distances start and end at London
    # add distance between cities on index x(first city) and city with index (x)+1(second city) 
    # until the end of that list   

  return ordered_city_list, total_distance  # dispaly values 




# In[9]:


ordered_city_list, total_distance = tsp_from_ll(latitude_longitute_deg, list(latitude_longitude_pd.index))
print(', '.join(ordered_city_list))


# In[10]:


print(total_distance)


# In[11]:


ordered_city_list, total_distance = tsp_from_ll(latitude_longitute_deg, list(latitude_longitude_pd.index))
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
plt.plot(latitude_longitude_pd.loc[ordered_city_list + ['London'], 'longitude'], latitude_longitude_pd.loc[ordered_city_list + ['London'], 'latitude'], 'o-')
plt.xlabel('longitude / deg')
plt.ylabel('latitude / deg')
plt.axes().set_aspect('equal')


# In[ ]:





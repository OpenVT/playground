#
# e.g.:
# python ctypes_graph.py 330 331
#
__author__ = "Randy Heiland"

import sys
import pathlib
#import xml.etree.ElementTree as ET
#import math
# import scipy.io
# from pyMCDS import pyMCDS
# from pyMCDS_cells import pyMCDS_cells
import pcdl
#import matplotlib
import numpy as np
import networkx as nx

print("# args=",len(sys.argv))
if (len(sys.argv) < 2):
    print("Usage:")
else:
    kdx = 1
    out_dir = sys.argv[kdx]
    print("out_dir= ", out_dir)


G = nx.Graph()

id_ct0 = [0,1,2,3,4,5,6]
print("id_ct0= ",id_ct0)
max_idx = len(id_ct0)
xv = [0.,0.,3.,3.,0., 1.5, 5 ]
yv = [0.,2.,0.,3.,4.,4., 0 ]
r =  [1.,1.,1.,1.,1.,1,1]

radius = 1.0     # default
dmax = 2*radius + 1.e-6
dmax2 = dmax*dmax

kdx = 0
kmax = len(id_ct0)
for kdx in range(0,kmax):
    ii = id_ct0[kdx]
    for ndx in range(kdx,kmax):
        jj = id_ct0[ndx]

        if ii != jj:
            x1 = xv[ii]
            x2 = xv[jj]
            y1 = yv[ii]
            y2 = yv[jj]
            d2 = (x1-x2)**2 + (y1-y2)**2
            if d2 < dmax2:
                G.add_edge(ii,jj)

print(list(nx.connected_components(G)))
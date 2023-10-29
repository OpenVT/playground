# mpl4vtu.py -  display PhysiCell VTK (.vtu) cells' initial conditions
#
from vtk import *
from vtk.util import numpy_support
import numpy as np
import random
import argparse
import matplotlib.pyplot as plt
from matplotlib import colors

# try:
#     parser = argparse.ArgumentParser(description='vtu to CC3D .piff')
#     parser.add_argument("-i ", "--input", help=".vtu input file", action="store_true")
# except:
#     pass

reader = vtkXMLUnstructuredGridReader()
# reader.SetFileName("pc_cells2.vtu")
reader.SetFileName("pc_cells.vtu")
# reader.SetFileName("ugrid_test.vtu")
# reader.SetFileName("output_calculix.vtu")  # from https://gitlab.kitware.com/francois.mazen/calculix-to-vtk
# reader.ReadAllVectorsOn()
# reader.ReadAllScalarsOn()
reader.Update()

#ugrid = vtkUnstructuredGrid()
#ugrid = reader.GetOutput()

data = reader.GetOutput()
#dim = data.GetDimensions()
# bds = data.GetBounds()
# print("bds=",bds)  # (41.0, 141.0, 42.0, 42.0, 0.0, 0.0): (xmin,xmax, ymin,ymax,...)
# pd = data.GetPointData()

pts_vtk_array= data.GetPoints().GetData()
pts_numpy_array = numpy_support.vtk_to_numpy(pts_vtk_array)
x,y,z = pts_numpy_array[:,0] , pts_numpy_array[:,1] , pts_numpy_array[:,2]
# print("x=",x)  # list of x-coords , e.g., [ 41. 141.]
# print("y=",y)

print("num arrays=",data.GetPointData().GetNumberOfArrays())
# print(data.GetPointData().GetArrayName(0))  # 'volume'
vol_vtk = data.GetPointData().GetArray(0)  # 'volume'
vol = numpy_support.vtk_to_numpy(vol_vtk)
# print("vol=",vol)  # list of volumes, e.g., [2494., 2494.]

cid_vtk = data.GetPointData().GetArray(1)  # 'cell_id'
cid = numpy_support.vtk_to_numpy(cid_vtk)

#  (x-x0) / (x1-x0) = ix/N, where CP lattice is N pixels wide
#  (ix-0) = N*(x-x0) / (x1-x0)

# ix,iy = center of cell in CPM lattice coords
N = 200
x0 = -100.0
x1 = -x0
xdiff = x1-x0
y0 = -100.0
y1 = -y0
ydiff = y1-y0

lattice = np.zeros((N,N))

ioff = 7
for idx in range(len(vol)):
    ix_ctr = int(N * (x[idx]-x0) / xdiff )  # or round
    iy_ctr = int(N * (y[idx]-y0) / ydiff )
    # print("ctr=",ix_ctr,iy_ctr)
    rows = slice(iy_ctr-ioff, iy_ctr+ioff)
    cols = slice(ix_ctr-ioff, ix_ctr+ioff)
    # lattice[rows,cols] = random.randint(1,3)
    lattice[rows,cols] = cid[idx] + 1
    
# lattice[10:30, 10:20] = 1
# lattice[slice(10,30), slice(10,20)] = 1

# create discrete colormap
cmap = colors.ListedColormap(['white','gray','red'])
# bounds = [0,10,20]
bounds = [0,1,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
# ax.imshow(lattice, cmap=cmap, norm=norm, origin='lower')
ax.imshow(lattice, cmap=cmap, origin='lower')

ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])

plt.show()

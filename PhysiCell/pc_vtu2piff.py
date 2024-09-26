# pc_vtu2piff.py - convert PhysiCell VTK (.vtu) cells' initial conditions to CC3D .piff format
#
import sys
from vtk import *
from vtk.util import numpy_support
import numpy as np
# import argparse

# try:
#     parser = argparse.ArgumentParser(description='vtu to CC3D .piff')
#     parser.add_argument("-i ", "--input", help=".vtu input file", action="store_true")
# except:
#     pass

# dirname = sys.argv[1]
fname = sys.argv[1]

reader = vtkXMLUnstructuredGridReader()
# reader.SetFileName("pc_cells2.vtu")
# reader.SetFileName("pc_cells.vtu")
# reader.SetFileName("pc_2cells.vtu")
reader.SetFileName(fname)
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
print("x=",x)  # list of x-coords , e.g., [ 41. 141.]
print("y=",y)

print("num arrays=",data.GetPointData().GetNumberOfArrays())
print("0th array name: ",data.GetPointData().GetArrayName(0))  # 'volume'
print("1st array name: ",data.GetPointData().GetArrayName(1))  # 
vol_vtk = data.GetPointData().GetArray(0)  # 'volume'
vol = numpy_support.vtk_to_numpy(vol_vtk)
print("vol=",vol)  # list of volumes, e.g., [2494., 2494.]

cid_vtk = data.GetPointData().GetArray(1)
cid = numpy_support.vtk_to_numpy(cid_vtk)
print("cid=",cid)  


# (base) M1P~/git/OpenVT/playground/CC3D/rwh_simple1$ head mcs0.piff
# Include Clusters
# 2    2    Condensing    3    3    3    3    0    0
# 8    8    Condensing    5    5    3    3    0    0
# 5    5    Condensing    6    6    3    3    0    0
# 6    6    Condensing    3    3    4    4    0    0
# 7    7    NonCondensing    4    4    4    4    0    0
# 8    8    Condensing    5    5    4    4    0    0
# 8    8    Condensing    6    6    4    4    0    0
# …


#  (x-x0) / (x1-x0) = ix/N, where CP lattice is N pixels wide
#  (ix-0) = N*(x-x0) / (x1-x0)

# ix,iy = center of cell in CPM lattice coords
ix = []
iy = []
xmin = -20.0
xmax = -xmin
xdel = 10

ymin = xmin
ymax = xmax
ydel = xdel

# N = 200
x0 = -100.0
x1 = -x0
xdiff = x1-x0
y0 = -100.0
y1 = -y0
ydiff = y1-y0

# V = 4/3 * pi * R^3
four_thirds_pi =  4.188790204786391
for idx in range(len(vol)):
    cell_radii = np.divide(vol[idx], four_thirds_pi)
    cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)
    # ix.append( N * (x[idx]-xmin) / xdel )
    # iy.append( N * (y[idx]-ymin) / ydel )
    
print("\nix=",ix)
print("\niy=",iy)

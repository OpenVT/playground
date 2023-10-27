# vtu2piff.py - convert PhysiCell VTK (.vtu) cells' initial conditions to CC3D .piff format
#
from vtk import *
import argparse

# try:
#     parser = argparse.ArgumentParser(description='vtu to CC3D .piff')
#     parser.add_argument("-i ", "--input", help=".vtu input file", action="store_true")
# except:
#     pass

# reader = vtkUnstructuredGridReader()   # vtkUnstructuredGrid or just vtkPolyData?
reader = vtkXMLUnstructuredGridReader()   # vtkUnstructuredGrid or just vtkPolyData?
reader.SetFileName("pc_cells2.vtu")
# reader.SetFileName("ugrid_test.vtk")
# reader.SetFileName("output.vtu")  # from https://gitlab.kitware.com/francois.mazen/calculix-to-vtk
# reader.ReadAllVectorsOn()
# reader.ReadAllScalarsOn()
reader.Update()

#ugrid = vtkUnstructuredGrid()
#ugrid = reader.GetOutput()

data = reader.GetOutput()
#dim = data.GetDimensions()
bds = data.GetBounds()
print("bds=",bds)
pd = data.GetPointData()
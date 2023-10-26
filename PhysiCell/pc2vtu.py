# pc2vtk.py - convert PhysiCell cells' initial conditions (.csv) to VTK format
#
# Rf. https://www.kitware.com/easy-data-conversion-to-vtk-with-python/

from vtk import *

vtk_data = vtkUnstructuredGrid()   # vtkUnstructuredGrid or just vtkPolyData?

# VTK point data
points = vtkPoints()
number_of_points = 2

# VTK data array(s): PC cell volume, etc
# volume = vtkDoubleArray()
volume = vtkFloatArray()
#volume.SetNumberOfComponents(number_of_components)
# volume.SetNumberOfComponents(1)
# number_of_tuples = 1
# volume.SetNumberOfTuples(number_of_tuples)
volume.SetName('volume')

x = 41.0
y = 42.0
z = 0.0
for id in range(number_of_points):
    # points.InsertPoint(id, [x, y, z])
    points.InsertNextPoint(x, y, z)
    volume.InsertNextValue(2494.0)
    x += 100

vtk_data.SetPoints(points)
vtk_data.GetPointData().AddArray(volume)

# VTK "cell" data (none for this)

# for id in range(number_of_tuples):
#     values = [2494.0]
#     volume.SetTuple(id, values)
# vtk_data.GetPointData().AddArray(volume)

out_fname = "pc_cells.vtu"
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName(out_fname)   # .vtp for polydata
writer.SetInputData(vtk_data)
writer.SetDataModeToAscii()
writer.Write()
print("--> ",out_fname)
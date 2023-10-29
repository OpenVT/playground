# pc2vtu.py - convert PhysiCell cells' initial conditions (.csv) to VTK format
#
# Rf. https://www.kitware.com/easy-data-conversion-to-vtk-with-python/

from vtk import *

vtk_data = vtkUnstructuredGrid()   # vtkUnstructuredGrid or just vtkPolyData?

points = vtkPoints()

# volume = vtkDoubleArray()
volume = vtkFloatArray()
volume.SetName('volume')

cell_id = vtkIntArray()
cell_id.SetName('cell_id')

cid_d = {'ctypeA':0, 'ctypeB':1}

with open("data.csv", "r") as fstream:
    for line in fstream:
        l = line.split(",")
        if l[0] == 'x':
            print("got PhysiCell ICs v2")
            continue
        else:
            # print("Error: invalid format for PhysiCell ICs v2")
            # break
            x = float(l[0])
            y = float(l[1])
            z = float(l[2])
            print(x,y,z)

            points.InsertNextPoint(x, y, z)
            volume.InsertNextValue(2494.0)
            cid = l[3].strip('\n')
            cell_id.InsertNextValue(cid_d[cid])

vtk_data.SetPoints(points)
vtk_data.GetPointData().AddArray(volume)
vtk_data.GetPointData().AddArray(cell_id)

out_fname = "pc_cells.vtu"
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName(out_fname)   # .vtp for polydata
writer.SetInputData(vtk_data)
writer.SetDataModeToAscii()
writer.Write()
print("--> ",out_fname)
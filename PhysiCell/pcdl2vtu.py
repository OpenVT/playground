# pcdl2vtu.py - convert PhysiCell cells' (e.g., output00000864_cells.mat) to VTK format
#
# Rf. https://www.kitware.com/easy-data-conversion-to-vtk-with-python/
#     https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL.md

import pathlib
# import pcdl
from pcdl import pyMCDS
from vtk import *

# print('pcdl version:', pcdl.__version__)  # it is easy to figure out which pcdl version you run

# s_path = str(pathlib.Path("cellsort6_output"))
# s_file = 'output00000864.xml'
# s_pathfile = f'{s_path}/{s_file}'
# print('mcds xml:', s_pathfile)

# mcds = pyMCDS(xml_file_root, self.output_dir, microenv=False, graph=False, verbose=False)
fname = 'output00000864.xml'
dirname = 'cellsort6_output'
mcds = pyMCDS(fname, dirname)

# load mcds - multi cell data standard - object
# mcds = pcdl.TimeStep(s_pathfile) 

# from Studio: vis_tab.py: plot_cell_scalar()
total_min = mcds.get_time()
xvals = mcds.get_cell_df()['position_x']
yvals = mcds.get_cell_df()['position_y']
zvals = mcds.get_cell_df()['position_z']

            # elif cell_scalar_name == "cell_type":
            #     ct_low  = int(min(cell_scalar))
            #     ct_high = int(max(cell_scalar))
cell_type = mcds.get_cell_df()['cell_type']
print(" --> cell_type[0]= ",cell_type[0])
cell_vol = mcds.get_cell_df()['total_volume']
print(" --> cell_vol[0]= ",cell_vol[0])

#-------
vtk_data = vtkUnstructuredGrid()   # vtkUnstructuredGrid or just vtkPolyData?

points = vtkPoints()

# volume = vtkDoubleArray()
volume = vtkFloatArray()
volume.SetName('volume')

cell_id = vtkIntArray()
cell_id.SetName('cell_id')

cid_d = {'ctypeA':0, 'ctypeB':1}

z = 0.0
for idx in range(len(xvals)):
    x = xvals[idx]
    y = yvals[idx]
    z = zvals[idx]
    print(x,y,z)

    points.InsertNextPoint(x, y, z)
    # volume.InsertNextValue(2494.0)
    volume.InsertNextValue(cell_vol[idx])
    # cell_id.InsertNextValue(int(cell_type[idx]))
    cell_id.InsertNextValue(cid_d[cell_type[idx]])

vtk_data.SetPoints(points)
vtk_data.GetPointData().AddArray(volume)
vtk_data.GetPointData().AddArray(cell_id)

# out_fname = "pcdl_cells.vtu"
out_fname = fname[:-4] + ".vtu"
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName(out_fname)   # .vtp for polydata
writer.SetInputData(vtk_data)
writer.SetDataModeToAscii()
writer.Write()
print("--> ",out_fname)
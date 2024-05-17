# cb_vtu2morpheus.py - convert (2D) center-based cells (e.g., PhysiCell) in a VTK unstructured grid format (.vtu) to Morpheus's .xml format
#
#  python cb_vtu2morph.py <vtu-input-file> <domain-xmin> <domain-xmax> <domain-ymin> <domain-ymax> <nx-lattice> <ny-lattice>
#  python cb_vtu2morph.py cellsort_small_checker_pcell.vtu -100 100 -100 100 100 100
#
import sys
from vtk import *
from vtk.util import numpy_support
import numpy as np
import argparse
from pathlib import Path

vtu_file = None
try:
    parser = argparse.ArgumentParser(description='Center-based cells .vtu to Morpheus .xml format')

    # parser.add_argument("-b ", "--bare", "--basic", help="no plotting, etc ", action="store_true")
    # parser.add_argument("-f ", "--vtu ", type=str, help=".vtu file")

    # parser = argparse.ArgumentParser()
    parser.add_argument("vtu")
    parser.add_argument("xmin")
    parser.add_argument("xmax")
    parser.add_argument("ymin")
    parser.add_argument("ymax")
    parser.add_argument("nx")
    parser.add_argument("ny")

    args = parser.parse_args()
    print(args.vtu)

    if args.vtu:
        # logging.debug(f'file is {args.file}')
        # sys.exit()
        vtu_file = args.vtu
        print(f'vtu_file is : {vtu_file}')
        if (len(vtu_file) > 0) and Path(vtu_file).is_file():
            print(f'{vtu_file} exists')
            # logging.debug(f'studio.py: open_as_cb():  filePath is valid')
            # logging.debug(f'len(vtu_file) = {len(vtu_file)}')
            # logging.debug(f'done with args.file')
        else:
            print(f'vtu_file is NOT found (or not valid): {args.vtu}')
            # logging.error(f'vtu_file is NOT valid: {args.file}')
            sys.exit()

    try:
        xmin = float(args.xmin)
    except:
        print(f'xmin is not a number: {args.xmin}')
        sys.exit()
    try:
        xmax = float(args.xmax)
    except:
        print(f'xmax is not a number: {args.xmax}')
        sys.exit()
    if xmin >= xmax:
        print(f'Error: xmin {xmin} >= xmax {xmax}')
        sys.exit()

    try:
        ymin = float(args.ymin)
    except:
        print(f'ymin is not a number: {args.ymin}')
        sys.exit()
    try:
        ymax = float(args.ymax)
    except:
        print(f'ymax is not a number: {args.ymax}')
        sys.exit()
    if ymin >= ymax:
        print(f'Error: ymin {xmin} >= ymax {xmax}')
        sys.exit()

    try:
        nx = int(args.nx)
    except:
        print(f'nx is not a number: {args.nx}')
        sys.exit()
    try:
        ny = int(args.ny)
    except:
        print(f'ny is not a number: {args.ny}')
        sys.exit()
except:
    print("Error parsing command line args.")
    sys.exit(-1)

x_range = xmax - xmin
y_range = ymax - ymin

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(vtu_file)
reader.Update()
data = reader.GetOutput()
#dim = data.GetDimensions()
# bds = data.GetBounds()
# print("bds=",bds)  # (41.0, 141.0, 42.0, 42.0, 0.0, 0.0): (xmin,xmax, ymin,ymax,...)
# pd = data.GetPointData()

pts_vtk_array= data.GetPoints().GetData()
pts_numpy_array = numpy_support.vtk_to_numpy(pts_vtk_array)
xvals,yvals,zvals = pts_numpy_array[:,0] , pts_numpy_array[:,1] , pts_numpy_array[:,2]
print("xvals=",xvals)  # list of x-coords , e.g., [ 41. 141.]
print("yvals=",yvals)

num_arrays=data.GetPointData().GetNumberOfArrays()
print("num arrays=",num_arrays)
for idx in range(num_arrays):
    print(f'  array {idx} = {data.GetPointData().GetArrayName(idx)}')  # 'volume'

# cell IDs
# ids_vtk = data.GetPointData().GetArray(0)  # 'cell_id'
ids_vtk = data.GetPointData().GetArray(1)  # 'cell_id'
cell_ids = numpy_support.vtk_to_numpy(ids_vtk)
print("cell_ids=",cell_ids)

# cell volumes
# vol_vtk = data.GetPointData().GetArray(1)  # 'volume'
vol_vtk = data.GetPointData().GetArray(0)  # 'volume'
cell_vol = numpy_support.vtk_to_numpy(vol_vtk)
print("cell_vol=",cell_vol)  # list of volumes, e.g., [2494., 2494.]

dx_lattice = float(xmax-xmin)/nx
dy_lattice = float(ymax-ymin)/ny
print("xmin, xmax = ",xmin,xmax)
print("ymin, ymax = ",ymin,ymax)
print("dx,dy (lattice) = ",dx_lattice,dy_lattice)  # presumably cc3d allows a non-square lattice?

idx = vtu_file.rfind('.')
fname_out = vtu_file[:idx] + "_morph_ics.xml"
print("------ Morpheus filename output= ",fname_out)
fout = open(fname_out, 'w')

four_thirds_pi =  4.188790204786391
cell_radii = np.divide(cell_vol, four_thirds_pi)
cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

# R2 = 8.*8.

debug_flag = False
if debug_flag:
    print(" --------   for Morpheus .xml :")

# Include Clusters
# 2    2    Condensing    3    3    3    3    0    0
# 8    8    Condensing    5    5    3    3    0    0
# ...
# 7    7    NonCondensing    4    4    4    4    0    0

cell_type_name = {0: 'Condensing', 1:"NonCondensing"}

    # <CellPopulations>
    #     <Population type="celltype_1" size="3">
    #         <InitCellObjects mode="distance">
    #             <Arrangement repetitions="1, 1, 1" displacements="1, 1, 1">
    #                 <Sphere center="22.34, 19.55, 0" radius="9.8724"/>
    #             </Arrangement>
    #             <Arrangement repetitions="1, 1, 1" displacements="1, 1, 1">
    #                 <Sphere center="50.452, 80.345, 0" radius="12.345"/>
    #             </Arrangement>
    # ...
    #             </InitCellObjects>
    #     </Population>
    #     <Population type="celltype_2" size="3">

header = """
<?xml version='1.0' encoding='UTF-8'?>
<MorpheusModel version="4">
    <Description>
        <Details>A list of 
            Arrangement repetitions=1, 1, 1 displacements=1, 1, 1
            Sphere center=x_i, y_i, z_i radius=r_i
within the InitCellObjects constructor will place spheres with radii r_i (or discs in 2D, then z_i is ignored) at position (x_i, y_i, z_i).
The mode=distance attribute of InitCellObjects yields a (generalized, with curved interfaces) Voronoi tesselation wherever spheres (possibly of different radii) overlap. 
However, the Voronoi tesselation is currently applied per cell Population element and lattice nodes already occupied by earlier placed Populations are not available for later placed Populations.
One may therefore place all cells within one Population which seeds the cells in the same order with ascending CellIDs as listed and then at time==0 a ChangeCellType is executed to assign the desired CellIDs to a different CellType.</Details>
        <Title>Test Cell Initialization</Title>
    </Description>
    <Space>
        <Lattice class="square">
            <Neighborhood>
                <Order>optimal</Order>
            </Neighborhood>
            <Size symbol="size" value="100, 100, 0"/>
        </Lattice>
        <SpaceSymbol symbol="space"/>
    </Space>
    <Time>
        <StartTime value="0"/>
        <StopTime value="100"/>
        <TimeSymbol symbol="time"/>
    </Time>
    <Analysis>
        <ModelGraph include-tags="#untagged" format="dot" reduced="false"/>
        <Gnuplotter time-step="-1">
            <Plot>
                <Cells value="cell.type"/>
            </Plot>
            <Terminal name="png"/>
        </Gnuplotter>
    </Analysis>
    <CellPopulations>
"""
fout.write(header)

icell = 0
    #     <Population type="celltype_1" size="3">
    #         <InitCellObjects mode="distance">
for celltype_id in cell_type_name.keys():
  print("--------- process celltype_id=",celltype_id)
#   <Population type="celltype_1" size="3">
  s = f'    <Population type="{cell_type_name[celltype_id]}" size="3">\n'
  fout.write(s)
  for icell in range(len(xvals)):
    # print("----- icell= ",icell)
    cell_type_id = int(cell_ids[icell])
    if cell_type_id != celltype_id:
        pass

    x = xvals[icell]
    y = yvals[icell]
    r = cell_radii[icell]
    print(icell,x,y,r)
    # z = zvals[icell]
    s =f'        <Arrangement repetitions="1, 1, 1" displacements="1, 1, 1">\n'
    fout.write(s)
    #                 <Sphere center="50.452, 80.345, 0" radius="12.345"/>
    xnew = (x - xmin)/x_range * nx
    ynew = (y - ymin)/y_range * ny
    # s =f'            Sphere center="{x}, {y}, 0" radius="{r}"/>\n'
    s =f'            <Sphere center="{xnew}, {ynew}, 0" radius="{r}"/>\n'
    if debug_flag:
        print(s)
    fout.write(s)
    s =f'        </Arrangement>\n'
    fout.write(s)

  s = f'    </Population>\n'
  fout.write(s)

trailer = """
    </CellPopulations>
    <CellTypes>
        <CellType name="celltype_1" class="biological"/>
        <CellType name="celltype_2" class="biological"/>
    </CellTypes>
</MorpheusModel>
"""
# cell_type_name = {0: 'Condensing', 1:"NonCondensing"}
s = f'    </CellPopulations>\n    <CellTypes>\n'
fout.write(s)

for ctype in cell_type_name.keys():
    s = f'        <CellType name="{cell_type_name[ctype]}" class="biological"/>\n'
    fout.write(s)

s = f'    </CellTypes>\n</MorpheusModel>\n'
fout.write(s)

# fout.write(trailer)
fout.close()    
print("--> ",fname_out)
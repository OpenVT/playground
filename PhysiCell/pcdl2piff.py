# pcdl2piff.py - convert PhysiCell cells' (e.g., output00000864_cells.mat) to a CC3D .piff format
#
# Note: this is just a temporary script, to be replaced by one that operates on a .vtu and outputs a .piff
#
# Rf. https://www.kitware.com/easy-data-conversion-to-vtk-with-python/
#     https://github.com/elmbeech/physicelldataloader/blob/master/man/TUTORIAL.md

import os,sys,string
import pathlib
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
import numpy as np
# import pcdl
from pcdl import pyMCDS
from vtk import *

# p1=string.atof(sys.argv[1])
try:
    dirname = sys.argv[1]
    fname = sys.argv[2]
    # lattice resolution
    nx = int(sys.argv[3])
    ny = int(sys.argv[4])
except:
    print(f"Usage: {sys.argv[0]} dirname xml_filename nx_lattice ny_lattice")
    exit(-1)

# try:
#     config_file = sys.argv[3]
# except:
#     config_file = "PhysiCell_settings.xml"

# tree = ET.parse(self.config_file)
# tree = ET.parse(os.path.join(dirname,config_file))
tree = ET.parse(os.path.join(dirname,fname))
# print(f"studio: (default) self.tree = {self.tree}")
xml_root = tree.getroot()

# print('pcdl version:', pcdl.__version__)  # it is easy to figure out which pcdl version you run

# s_path = str(pathlib.Path("cellsort6_output"))
# s_file = 'output00000864.xml'
# s_pathfile = f'{s_path}/{s_file}'
# print('mcds xml:', s_pathfile)

# mcds = pyMCDS(xml_file_root, self.output_dir, microenv=False, graph=False, verbose=False)
# fname = 'output00000864.xml'
# dirname = 'cellsort6_output'
mcds = pyMCDS(fname, dirname, microenv=False, graph=False)

bbox = xml_root.find(".//microenvironment//domain//mesh//bounding_box").text
print("bbox = ",bbox)
bbox_l = bbox.split()  # ['-30.000000', '-30.000000', '-10.000000', '30.000000', '30.000000', '10.000000']
# bbox = xml_root.find(".//microenvironment//domain//mesh//bounding_box")
xmin = float(bbox_l[0])
xmax = float(bbox_l[3])
ymin = float(bbox_l[1])
ymax = float(bbox_l[4])
print("bds=",xmin,xmax,ymin,ymax)

dx_lattice = float(xmax-xmin)/nx
dy_lattice = float(ymax-ymin)/ny
print("dx,dy (lattice) = ",dx_lattice,dy_lattice)  # presumably cc3d allows a non-square lattice?


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
cell_vol = mcds.get_cell_df()['total_volume']
# print("type(cell_type)=",type(cell_type))   # <class 'pandas.core.series.Series'>
print("len(cell_type)=",len(cell_type))
for idx in range(len(cell_type)):
    if idx > 4: break
    print(f' {idx}) {cell_type[idx]}: vol= {cell_vol[idx]}')

#-------
# hardwired test
cid_d = {'ctypeA':0, 'ctypeB':1}
ctype_d = {0:'ctypeA', 1:'ctypeB'}

# initial.xml:
#   <bounding_box type="axis-aligned" units="micron">-30.000000 -30.000000 -10.000000 30.000000 30.000000 10.000000</bounding_box>

# get xmin,xmax,xdel, ymin,ymax,ydel from .xml

z = 0.0
four_thirds_pi =  4.188790204786391
cell_radii = np.divide(cell_vol, four_thirds_pi)
cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

# for each cell in PhysiCell
debug_flag = False

fname_out = fname[:-4] + ".piff"
fout = open(fname_out, 'w')
for icell in range(len(xvals)):
    x = xvals[icell]
    y = yvals[icell]
    z = zvals[icell]

    if debug_flag:
        print(f'{icell}) cell at x,y,z= {x},{y},{z}  has radius= {cell_radii[icell]}')
        print(f'{icell}) cell at x,y,z= {x},{y},{z}  has radius= {cell_radii[icell]}')
    R2 = cell_radii[icell] * cell_radii[icell]

    # optimize this loop eventually
    # ix = (x-xmin)/dx_lattice
    # iy = (y-ymin)/dy_lattice
    # print(    "pixel= ",ix,iy)

# 0 Medium 0 5 0 4 0 0
# 1 ct1 1 3 1 1 0 0
# 2 ct1 1 3 3 3 0 0
# 2 ct1 1 1 2 2 0 0

    if debug_flag:
        print(" --------   for piff:")
    for iy in range(ny):
        iyv = (iy * dy_lattice) + ymin
        yd = iyv - y
        if debug_flag:
            print(f"    iyv={iyv}, yd={yd}")
        for ix in range(nx):
            ixv = (ix * dx_lattice) + xmin
            xd = ixv - x
            if (xd*xd + yd*yd) < R2:
                # print(f'{cell_type[icell]} {ctype_d[cell_type[icell]]} {ixv} {ixv} {iyv} {iyv} 0 0')
                # print(f'{cell_type[icell]} foo {ixv} {ixv} {iyv} {iyv} 0 0')
                s =f'{icell} {cell_type[icell]} {ix} {ix} {iy} {iy} 0 0\n'
                # print(f'{icell} {cell_type[icell]} {ix} {ix} {iy} {iy} 0 0')
                fout.write(s)

fout.close()
print(" -----> ",fname_out)

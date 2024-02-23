# playground
Playground for devs to test and share simple models and ideas.

Present the VTK Unstructured Grid (.vtu) format as a possible standard for storing and converting ICs.

A script to generate a .vtu file from a PhysiCell (cells) output file (.mat):
```
(base) M1P~/git/OpenVT/playground/PhysiCell$ python pcdl2vtu.py output_test2cells output00000000.xml
reading: output_test2cells/PhysiCell_settings.xml
Warning @ pyMCDS._read_xml : cell_definition custom_data without variable type setting detected. ['sample']
reading: output_test2cells/output00000000.xml
working on metadata ...
working on mesh data ...
reading: output_test2cells/initial_mesh0.mat
working on discrete cell data ...
reading: output_test2cells/output00000000_cells.mat
done!
bbox =  -30.000000 -30.000000 -10.000000 30.000000 30.000000 10.000000
bds= -30.0 30.0 -30.0 30.0
len(cell_type)= 2
 0) ctypeA: vol= 2494.0
 1) ctypeB: vol= 2494.0
0 ) x,y,z=  -9.649676331393135 -0.8192351629222685 0.0
1 ) x,y,z=  13.980851874014036 -9.174781047707121 0.0
-->  output00000000_pcell.vtu
```

A temporary script to generate a .piff file from a PhysiCell (cells) output file (.mat):
```
(base) M1P~/git/OpenVT/playground/PhysiCell$ python pcdl2piff.py output_test2cells output00000000.xml 20 20
reading: output_test2cells/PhysiCell_settings.xml
Warning @ pyMCDS._read_xml : cell_definition custom_data without variable type setting detected. ['sample']
reading: output_test2cells/output00000000.xml
working on metadata ...
working on mesh data ...
reading: output_test2cells/initial_mesh0.mat
working on discrete cell data ...
reading: output_test2cells/output00000000_cells.mat
done!
bbox =  -30.000000 -30.000000 -10.000000 30.000000 30.000000 10.000000
bds= -30.0 30.0 -30.0 30.0
dx,dy (lattice) =  3.0 3.0
len(cell_type)= 2
 0) ctypeA: vol= 2494.0
 1) ctypeB: vol= 2494.0
 ----->  output00000000.piff
```

Then look at the generated .piff file:
```
(base) M1P~/git/OpenVT/playground/PhysiCell$ ty output00000000.piff 
0 ctypeA 7 7 7 7 0 0
0 ctypeA 5 5 8 8 0 0
0 ctypeA 6 6 8 8 0 0
0 ctypeA 7 7 8 8 0 0
0 ctypeA 8 8 8 8 0 0
0 ctypeA 5 5 9 9 0 0
0 ctypeA 6 6 9 9 0 0
0 ctypeA 7 7 9 9 0 0
0 ctypeA 8 8 9 9 0 0
0 ctypeA 9 9 9 9 0 0
0 ctypeA 4 4 10 10 0 0
0 ctypeA 5 5 10 10 0 0
0 ctypeA 6 6 10 10 0 0
0 ctypeA 7 7 10 10 0 0
0 ctypeA 8 8 10 10 0 0
0 ctypeA 9 9 10 10 0 0
0 ctypeA 5 5 11 11 0 0
0 ctypeA 6 6 11 11 0 0
0 ctypeA 7 7 11 11 0 0
0 ctypeA 8 8 11 11 0 0
0 ctypeA 9 9 11 11 0 0
0 ctypeA 6 6 12 12 0 0
0 ctypeA 7 7 12 12 0 0
0 ctypeA 8 8 12 12 0 0
1 ctypeB 13 13 5 5 0 0
1 ctypeB 14 14 5 5 0 0
1 ctypeB 15 15 5 5 0 0
1 ctypeB 16 16 5 5 0 0
1 ctypeB 13 13 6 6 0 0
1 ctypeB 14 14 6 6 0 0
1 ctypeB 15 15 6 6 0 0
1 ctypeB 16 16 6 6 0 0
1 ctypeB 17 17 6 6 0 0
1 ctypeB 12 12 7 7 0 0
1 ctypeB 13 13 7 7 0 0
1 ctypeB 14 14 7 7 0 0
1 ctypeB 15 15 7 7 0 0
1 ctypeB 16 16 7 7 0 0
1 ctypeB 17 17 7 7 0 0
1 ctypeB 13 13 8 8 0 0
1 ctypeB 14 14 8 8 0 0
1 ctypeB 15 15 8 8 0 0
1 ctypeB 16 16 8 8 0 0
1 ctypeB 17 17 8 8 0 0
1 ctypeB 13 13 9 9 0 0
1 ctypeB 14 14 9 9 0 0
1 ctypeB 15 15 9 9 0 0
1 ctypeB 16 16 9 9 0 0
```

Need a script to plot the .piff file.

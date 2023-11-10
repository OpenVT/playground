
* https://compucell3d.org/Tutorials

```
(base) M1P~/CC3DWorkspace/cellsort_2D_cc3d_10_17_2023_07_25_46$ ls
Simulation/		cellsort_2D.cc3d
(base) M1P~/CC3DWorkspace/cellsort_2D_cc3d_10_17_2023_07_25_46$ ls Simulation/
cellsort_2D.py			cellsort_2D.xml			cellsort_2D_steppables.py
(base) M1P~/CC3DWorkspace/cellsort_2D_cc3d_10_17_2023_07_25_46$ ty cellsort_2D.cc3d  
<Simulation version="3.5.1">
    <XMLScript>Simulation/cellsort_2D.xml</XMLScript>    
    <PythonScript>Simulation/cellsort_2D.py</PythonScript>        
    <Resource Type="Python">Simulation/cellsort_2D_steppables.py</Resource>
</Simulation>

---------------
(base) M1P~/CC3DWorkspace/bacterium_macrophage_cc3d_10_19_2023_13_42_24/LatticeData$ ls
StepLDF.dml	Step_00002.vtk	Step_00005.vtk	Step_00008.vtk	Step_00011.vtk
Step_00000.vtk	Step_00003.vtk	Step_00006.vtk	Step_00009.vtk
Step_00001.vtk	Step_00004.vtk	Step_00007.vtk	Step_00010.vtk

(base) M1P~/CC3DWorkspace/bacterium_macrophage_cc3d_10_19_2023_13_42_24/LatticeData$ ty StepLDF.dml 
<CompuCell3DLatticeData Version="1.0">
   <Dimensions x="100" y="100" z="1"/>
   <Lattice Type="Square"/>
   <Output CoreFileName="Step" Directory="/Users/heiland/CC3DWorkspace/bacterium_macrophage_cc3d_10_19_2023_13_42_24/LatticeData" Frequency="1" NumberOfSteps="10000"/>
   <CellType TypeId="0" TypeName="Medium"/>
   <CellType TypeId="1" TypeName="Bacterium"/>
   <CellType TypeId="2" TypeName="Macrophage"/>
   <CellType TypeId="3" TypeName="Wall"/>
   <Fields>
      <Field Name="Cell_Field" Type="CellField"/>
      <Field Name="ATTR" Type="ConField"/>
   </Fields>
</CompuCell3DLatticeData>
```

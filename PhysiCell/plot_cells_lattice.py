#
# plot_cells_lattice.py:  render/animate PhysiCell .svg files, lattice, pixels (anim via arrows) 
#
# Usage:
#  python plot_cells_lattice.py <lattice_size>   # assume same in each dim
#  python plot_cells_lattice.py <show_nucleus start_index axes_min axes_max>
#    i.e., the arguments <...> are optional and have defaults.
# 
# Keyboard arrows: right/left arrows will single step forward/backward; up/down will increment/decrement step size
#
# Dependencies include matplotlib and numpy. We recommend installing the Anaconda Python3 distribution.
#
# Examples (run from directory containing the .svg files):
#  python plot_cells_lattice.py 
#  python plot_cells_lattice.py 20
#  python plot_cells_lattice.py 0 5 700 1300 
#
# Author: Randy Heiland (except for the circles() function)
#
#
__author__ = "Randy Heiland"

import sys
import glob
import os
import xml.etree.ElementTree as ET
import math
import cmaps
from pathlib import Path
from pyMCDS import pyMCDS
# from pcdl import pyMCDS
join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"
try:
  import matplotlib
  from matplotlib.collections import LineCollection
  from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
  import matplotlib.colors as mplc
  from matplotlib.patches import Circle, Ellipse, Rectangle
  from matplotlib.collections import PatchCollection
except:
  print("\n---Error: cannot import matplotlib")
  print("---Try: python -m pip install matplotlib")
  print(join_our_list)
#  print("---Consider installing Anaconda's Python 3 distribution.\n")
  raise
try:
  import numpy as np  # if mpl was installed, numpy should have been too.
except:
  print("\n---Error: cannot import numpy")
  print("---Try: python -m pip install numpy\n")
  print(join_our_list)
  raise
from collections import deque
try:
  # apparently we need mpl's Qt backend to do keypresses 
#  matplotlib.use("Qt5Agg")
  matplotlib.use("TkAgg")
  import matplotlib.pyplot as plt
except:
  print("\n---Error: cannot use matplotlib's TkAgg backend")
  print(join_our_list)
#  print("Consider installing Anaconda's Python 3 distribution.")
  raise


current_idx = 0
nargs = len(sys.argv)-1
print("# args=",nargs)
output_dir = "."
try:
    output_dir = argv[1]
except:
    pass
print("output_dir=",output_dir)

#for idx in range(len(sys.argv)):
use_defaults = True
show_nucleus = 0
current_idx = 0
axes_min = 0.0
axes_max = 1000  # but overridden by "width" attribute in .svg
lattice_size = 0
if nargs == 1:
  lattice_size = int(sys.argv[1])
elif nargs == 4:
  use_defaults = False
  kdx = 1
  show_nucleus = int(sys.argv[kdx])
  kdx += 1
  current_idx = int(sys.argv[kdx])
  kdx += 1
  axes_min = float(sys.argv[kdx])
  kdx += 1
  axes_max = float(sys.argv[kdx])
elif (len(sys.argv) != 1):
  print("Please provide either no args or 4 args:")
  usage_str = "show_nucleus start_index axes_min axes_max"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 0 0 0 2000" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)

cax2 = None
cell_plot = None
fontsize = 7
label_fontsize = 6
title_fontsize = 10

#"""
print("lattice_size =",lattice_size )
print("show_nucleus=",show_nucleus)
print("current_idx=",current_idx)
print("axes_min=",axes_min)
print("axes_max=",axes_max)
#"""

"""
if (len(sys.argv) > 1):
   current_idx = int(sys.argv[1])
if (len(sys.argv) > 2):
   axes_min = float(sys.argv[2])
   axes_max = float(sys.argv[3])

if (len(sys.argv) > 4):
  usage_str = "[<start_index> [<axes_min axes_max>]]"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 1 10 700 1300" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)
"""

print("current_idx=",current_idx)

#d={}   # dictionary to hold all (x,y) positions of cells

""" 
--- for example ---
In [141]: d['cell1599'][0:3]
Out[141]: 
array([[ 4900.  ,  4900.  ],
       [ 4934.17,  4487.91],
       [ 4960.75,  4148.02]])
"""

figure = plt.figure(figsize=(7,7))
ax0 = figure.gca()
#ax.set_aspect("equal")


#plt.ion()

time_delay = 0.1

count = -1
#while True:

#-----------------------------------------------------
def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    global ax0
    """
    See https://gist.github.com/syrte/592a062c562cd2a98a83 

    Make a scatter plot of circles. 
    Similar to plt.scatter, but the size of circles are in data scale.
    Parameters
    ----------
    x, y : scalar or array_like, shape (n, )
        Input data
    s : scalar or array_like, shape (n, ) 
        Radius of circles.
    c : color or sequence of color, optional, default : 'b'
        `c` can be a single color format string, or a sequence of color
        specifications of length `N`, or a sequence of `N` numbers to be
        mapped to colors using the `cmap` and `norm` specified via kwargs.
        Note that `c` should not be a single numeric RGB or RGBA sequence 
        because that is indistinguishable from an array of values
        to be colormapped. (If you insist, use `color` instead.)  
        `c` can be a 2-D array in which the rows are RGB or RGBA, however. 
    vmin, vmax : scalar, optional, default: None
        `vmin` and `vmax` are used in conjunction with `norm` to normalize
        luminance data.  If either are `None`, the min and max of the
        color array is used.
    kwargs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
        norm, cmap, transform, etc.
    Returns
    -------
    paths : `~matplotlib.collections.PathCollection`
    Examples
    --------
    a = np.arange(11)
    circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
    plt.colorbar()
    License
    --------
    This code is under [The BSD 3-Clause License]
    (http://opensource.org/licenses/BSD-3-Clause)
    """

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    # print("\n\n ----- circles():  x=",x)
    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    # ax0 = plt.gca()
    ax0.add_collection(collection)
    ax0.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        # print("------- doing plt.sci")
        plt.sci(collection)
    # else:
    #     print("------- NOT doing plt.sci")
    return collection

#-----------------------------------------------------
def plot_cell_scalar():
        global current_idx, axes_max, cax2, cell_plot, ax0, lattice_size
        # xml_file_root = "output%08d.xml" % frame

        xml_file_root = "output%08d.xml" % current_idx
        # output_dir = "."
        xml_file = os.path.join(output_dir, xml_file_root)
        # xml_file = os.path.join("tmpdir", xml_file_root)  # temporary hack
        # cell_scalar_name = cell_scalar_combobox.currentText()
        cell_scalar_name = "cell_type"
        # cbar_name = cell_scalar_cbar_combobox.currentText()
        cbar_name = "viridis"
        # print(f"\n\n   >>>>--------- plot_cell_scalar(): xml_file={xml_file}, scalar={cell_scalar_name}, cbar={cbar_name}")
        if not Path(xml_file).is_file():
            print("ERROR: file not found",xml_file)
            return

        mcds = pyMCDS(xml_file, output_dir, microenv=False, graph=False, verbose=False)
        total_min = mcds.get_time()  # warning: can return float that's epsilon from integer value
        # print("total_min=",total_min)
    
        try:
            cell_scalar = mcds.get_cell_df()[cell_scalar_name]
            # print("cell_scalar = ",cell_scalar )
        except:
            # print("plot_cell_scalar(): error performing mcds.get_cell_df()[cell_scalar_name]")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            # msg = "plot_cell_scalar(): error from mcds.get_cell_df()[" + cell_scalar_name + "]. You are probably trying to use out-of-date scalars. Resetting to .svg plots, so you will need to refresh the cell scalar dropdown combobox in the Plot tab."
            msg = "plot_cell_scalar(): error from mcds.get_cell_df()[" + cell_scalar_name + "]. You may be trying to use out-of-date scalars. Please reset the 'full list' or 'partial'."
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            # kill any animation ("Play" button) happening
            animating_flag = False
            play_button.setText("Play")
            timer.stop()

            # cells_svg_rb.setChecked(True)
            # plot_cells_svg = True
            # disable_cell_scalar_widgets()
            return
    
                
        fix_cells_cmap_flag = False
        if fix_cells_cmap_flag:
            vmin = cells_cmin_value
            vmax = cells_cmax_value
        else:
            vmin = cell_scalar.min()
            vmax = cell_scalar.max()
            
        num_cells = len(cell_scalar)
        # print("  len(cell_scalar) = ",len(cell_scalar))
        # fix_cmap = 0
        # print(f'   cell_scalar.min(), max() = {vmin}, {vmax}')
        cell_vol = mcds.get_cell_df()['total_volume']
        # print("mcds.get_cell_df().keys() = ",mcds.get_cell_df().keys())
        # print(f'   cell_vol.min(), max() = {cell_vol.min()}, {cell_vol.max()}')

        four_thirds_pi =  4.188790204786391
        cell_radii = np.divide(cell_vol, four_thirds_pi)
        cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

        xvals = mcds.get_cell_df()['position_x']
        yvals = mcds.get_cell_df()['position_y']
        # print("   type(xvals)= ",type(xvals))  # <class 'pandas.core.series.Series'>
        # print("   dir(xvals)= ",dir(xvals))
        # print(f'   xvals= {xvals}')
        # if total_min > 0.0:
        #     xvals[1] = 0.0
        # print("----(after resetting xvals)----")
        # print(f'   xvals= {xvals}')
        # print(f'   yvals= {yvals}')

        # title_str += "   cells: " + svals[2] + "d, " + svals[4] + "h, " + svals[7][:-3] + "m"
        # title_str = "(" + str(frame) + ") Current time: " + str(total_min) + "m"
        
        # print(cell_scalar_name, " - discrete: ", (cell_scalar % 1  == 0).all()) # Possible test if the variable is discrete or continuum variable (issue: in some time the continuum variable can be classified as discrete (example time=0))
        
        # if( cell_scalar_name == 'cell_type' or cell_scalar_name == 'current_phase'): discrete_variable = list(set(cell_scalar)) # It's a set of possible value of the variable
        discrete_cell_scalars = ['cell_type']
        if cell_scalar_name in discrete_cell_scalars: 
            if cell_scalar_name == "current_phase":   # and if "Fixed" range is checked
                cycle_phases = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18, 100,101,102,103,104]
                # if discrete_variable is None:
                discrete_variable = cycle_phases
            elif cell_scalar_name == "cell_type":
                # ct_low  = int(min(cell_scalar))
                # ct_high = int(max(cell_scalar))
                ct_low  = int(min(cell_scalar.keys()))
                ct_high = int(max(cell_scalar.keys()))
                # print("doing cell_type:  ct_low,ct_high=",ct_low,ct_high)
                discrete_variable = list(range(ct_low,ct_high+1))
            else:
                discrete_variable = list(set(cell_scalar)) # It's a set of possible value of the variable
        # if( discrete_variable ): # Generic way: if variable is discrete
            # cell_scalar_cbar_combobox.setEnabled(False)
            from_list = matplotlib.colors.LinearSegmentedColormap.from_list
            discrete_variable.sort()
            if (len(discrete_variable) == 1): 
                cbar_name = from_list(None, cmaps.gray_gray[0:2], len(discrete_variable))  # annoying hack
            else: 
                try:
                    # print("try: cbar_name = from_list(...)")
                    # print("len(discrete_variable)= ",len(discrete_variable))
                    # print("cmaps.paint_clist[0:len(discrete_variable)]= ",cmaps.paint_clist[0:len(discrete_variable)])
                    cbar_name = from_list(None, cmaps.paint_clist[0:len(discrete_variable)], len(discrete_variable))
                except:
                    print("except: return !!")
                    # return

            # usual categorical colormap on matplotlib has at max 20 colors (using colorcet the colormap glasbey_bw has n colors )
            # cbar_name = from_list(None, cc.glasbey_bw, len(discrete_variable))
            vmin = None
            vmax = None
            # Change the values between 0 and number of possible values
            for i, value in enumerate(discrete_variable):
                cell_scalar = cell_scalar.replace(value,i)
                # print("cell_scalar=",cell_scalar)
        else: 
            cell_scalar_cbar_combobox.setEnabled(True)

        mins = round(total_min)  # hack, assume we want integer mins
        hrs = int(mins/60)
        days = int(hrs/24)
        # print(f"mins={mins}, hrs={hrs}, days={days}")
        title_str = '%d days, %d hrs, %d mins' % (days, hrs-days*24, mins-hrs*60)
        title_str += " (" + str(num_cells) + " agents)"

        axes_min = mcds.get_mesh()[0][0][0][0]
        axes_max = mcds.get_mesh()[0][0][-1][0]

        cell_fill = True
        cell_edge = True
        cell_line_width = 0.5
        # plt.cla()
        ax0.cla()
        if (cell_fill):
            if (cell_edge):
                try:
                    # print("plot circles with vmin,vmax=",vmin,vmax)  # None,None
                    # print("\n----- plot circles with cbar_name=",cbar_name)  # <matplotlib.colors.LinearSegmentedColormap object at 0x1690d5330>
                    cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=cell_line_width, cmap=cbar_name, vmin=vmin, vmax=vmax)
                    # cell_plot = circles(xvals,yvals, s=cell_radii, edgecolor=cell_scalar, linewidth=0.5, cmap=cbar_name, vmin=vmin, vmax=vmax)
                except (ValueError):
                    # print("\n------ ERROR: Exception from circles with edges\n")  # always get this??
                    pass
            else:
                # cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name)
                cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax)

        else:  # semi-trransparent cell, but with (thicker) edge  (TODO: how to make totally transparent?)
            if (cell_edge):
                cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=cell_line_width2, cmap=cbar_name, vmin=vmin, vmax=vmax, alpha=cell_alpha)
            else:
                cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax, alpha=cell_alpha)


        # print("------- plot_cell_scalar() -------------")
        # num_axes =  len(figure.axes)
        num_axes =  len(figure.axes)
        # print("# axes = ",num_axes)  # = 2
        # if num_axes > 1: 
        # if axis_id_cellscalar:
        if cax2:
            # print("# axes(after cell_scalar remove) = ",len(figure.axes))
            # print(" figure.axes= ",figure.axes)
            #ppp
            if( discrete_variable ): # Generic way: if variable is discrete
                try:
                    cax2.remove()
                except:
                    print("except 1: cax2 - discrete_variable !!")
                    pass
                ax2_divider = make_axes_locatable(ax0)
                cax2 = ax2_divider.append_axes("bottom", size="4%", pad="8%")
                if cell_plot:
                    cbar2 = figure.colorbar(cell_plot, ticks=range(0,len(discrete_variable)), cax=cax2, orientation="horizontal")
                    # cbar2.ax.tick_params(length=0) # remove tick line
                    cell_plot.set_clim(vmin=-0.5,vmax=len(discrete_variable)-0.5) # scaling bar to the center of the ticks
                cbar2.set_ticklabels(discrete_variable) # It's possible to give strings
                cbar2.ax.tick_params(labelsize=fontsize)
                cbar2.ax.set_xlabel(cell_scalar_name)
                discrete_variable = None
            else:
                try:
                    cax2.remove()
                except:
                    print("except 2: cax2 - NOT discrete_variable !!")
                    pass
                ax2_divider = make_axes_locatable(ax0)
                cax2 = ax2_divider.append_axes("bottom", size="4%", pad="8%")
                cbar2 = figure.colorbar(cell_plot, ticks=None,cax=cax2, orientation="horizontal")
                cbar2.ax.tick_params(labelsize=fontsize)
                cbar2.ax.set_xlabel(cell_scalar_name)

            # print("\n# axes(redraw cell_scalar) = ",len(figure.axes))
            # print(" figure.axes= ",figure.axes)
            # axis_id_cellscalar = len(figure.axes) - 1
        else:
            ax2_divider = make_axes_locatable(ax0)
            cax2 = ax2_divider.append_axes("bottom", size="4%", pad="8%")
            cbar2 = figure.colorbar(cell_plot, cax=cax2, orientation="horizontal")
            cbar2.ax.tick_params(labelsize=fontsize)
            # print(" figure.axes= ",figure.axes)
            cbar2.ax.set_xlabel(cell_scalar_name)
        
          #------ lattice grid ---------
        if lattice_size > 0:
            # xs = np.arange(self.xmin,self.xmax+1,self.xdel)  # DON'T try to use np.linspace!
            # xs = np.arange(-30,30+1,3)  # DON'T try to use np.linspace!
            ldel = 60.0/lattice_size
            # xs = np.arange(0,60+1, ldel)  # if plotting SVG coords
            xs = np.arange(-30,30+1, ldel)  # if plotting domain/float coords
            # print("xmin,max,del=",self.xmin,self.xmax,self.xdel)
            # print("xs= ",xs)
            # ys = np.arange(-30,30+1,3)
            # ys = np.arange(0,60+1, ldel)
            ys = np.arange(-30,30+1, ldel)  # if plotting domain/float coords
            # print("ys= ",ys)
            hlines = np.column_stack(np.broadcast_arrays(xs[0], ys, xs[-1], ys))
            vlines = np.column_stack(np.broadcast_arrays(xs, ys[0], xs, ys[-1]))
            grid_lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
            line_collection = LineCollection(grid_lines, color="darkgray", linewidths=0.5)
            #  self.ax0.add_collection(line_collection)

            #   ax0 = plt.figure().add_subplot(111, adjustable='box')
            #   ax0.add_collection(line_collection)
            # ax = plt.gca()
            # ax.autoscale_view()
            ax0.add_collection(line_collection)
            # ax.add_collection(line_collection)

   
        plot_xmin = -30
        plot_xmax = 30
        plot_ymin = -30
        plot_ymax = 30
        ax0.set_title(title_str, fontsize=title_fontsize)
        ax0.set_xlim(plot_xmin, plot_xmax)
        ax0.set_ylim(plot_ymin, plot_ymax)

        view_aspect_square = True
        if view_aspect_square:
            ax0.set_aspect('equal')
        else:
            ax0.set_aspect('auto')

        plt.pause(time_delay)  # NEED this

#-----------------------------------------------------
# def plot_svg():
#   global current_idx, axes_max

step_value = 1
def press(event):
  global current_idx, step_value
#    print('press', event.key)
  sys.stdout.flush()
  if event.key == 'escape':
    sys.exit(1)
  elif event.key == 'h':  # help
    print('esc: quit')
    print('right arrow: increment by step_value')
    print('left arrow:  decrement by step_value')
    print('up arrow:   increment step_value by 1')
    print('down arrow: decrement step_value by 1')
    print('0: reset to 0th frame')
    print('h: help')
  elif event.key == 'left':  # left arrow key
#    print('go backwards')
#    fig.canvas.draw()
    current_idx -= step_value
    if (current_idx < 0):
      current_idx = 0
    plot_cell_scalar()
  elif event.key == 'right':  # right arrow key
#        print('go forwards')
#        fig.canvas.draw()
    current_idx += step_value
    plot_cell_scalar()
  elif event.key == 'up':  # up arrow key
    step_value += 1
    print('step_value=',step_value)
  elif event.key == 'down':  # down arrow key
    step_value -= 1
    if (step_value <= 0):
      step_value = 1
    print('step_value=',step_value)
  elif event.key == '0':  # reset to 0th frame/file
    current_idx = 0
    plot_cell_scalar()
  else:
    print('press', event.key)


#for current_idx in range(40):
#  fname = "snapshot%08d.svg" % current_idx
#  plot_cell_scalar(fname)
plot_cell_scalar()
print("\nNOTE: click in plot window to give it focus before using keys.")

figure.canvas.mpl_connect('key_press_event', press)

# keep last plot displayed
#plt.ioff()
plt.show()

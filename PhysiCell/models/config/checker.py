# create checkerboard pattern of 2 cell types
# 18 cells/row in the 378 batch (-> 21 rows)
"""
(base) M1P~/git/OpenVT/playground/PhysiCell/models/config$ head *top_bo*
x,y,z,type,volume,cycle entry,custom:GFP,custom:sample
-141.58728945204578,-150.0,0.0,ctypeA
"""

import csv
import os

def strip_comments(csvfile):
    for row in csvfile:
        # raw = row.split('#')[0].strip()
        # if raw: yield raw
        # print(row)
        raw = row.split('/')[0].strip()
        # print(raw)
        if raw: yield raw

cells_ics = "cellsort_378_top_bot.csv"
# csvreader = csv.reader(file)
if os.path.isfile(cells_ics):
    try:
        header = True
        k = 0
        odd_cell = False
        odd_row = False
        with open(cells_ics) as csvfile:
            csv_reader = csv.reader(strip_comments(csvfile))
            for l in csv_reader:
                if header:
                    print("x,y,z,type,volume,cycle entry,custom:GFP,custom:sample")
                    header = False
                    continue
                idx = k % 18
                # print("k,idx=",k,idx)
                k += 1
                if idx == 0:
                    odd_row = not odd_row
                if odd_row:
                    print(f"{l[0]},{l[1]},{l[2]},ctypeA")
                else:
                    if idx%2 == 0:
                        print(f"{l[0]},{l[1]},{l[2]},ctypeB")
                    else:
                        print(f"{l[0]},{l[1]},{l[2]},ctypeA")

                # odd_cell = not odd_cell
                # if k > 999: 
                #     break
                # # print(f"l {k}= {elm}")
                # # if k > 0:
                # if odd_row:
                #     if k < 19:
                #     else:
                #         print(f"{l[0]},{l[1]},{l[2]},ctypeA")
                #         odd_row = not odd_row
                #         k = 0
                # else:
                #     if odd_cell:
                #         print(f"{l[0]},{l[1]},{l[2]},ctypeA")
                #     else:
                #         print(f"{l[0]},{l[1]},{l[2]},ctypeB")
                #     # if k > 18:
                #     if k > 17:
                #         odd_row = not odd_row
                #         k = 0
    except:
        print("Exception")

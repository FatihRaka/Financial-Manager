from tkinter import *
from tkinter.tix import *

def gridding(widget,row,column,rowspan=1,columnspan=1,sticky=W):
    widget.grid(row=row, column=column, rowspan=rowspan,columnspan=columnspan, sticky=sticky)

def getTOtalRatio(gui_data) :
    RATIOtotal=0
    for RATIOcategory in gui_data:
        RATIOtotal+=RATIOcategory[0].get()
    return RATIOtotal


# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 20:17:06 2022

@author: wb305167
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import *

def display_table(window, data=None, header=None, year=None, row=None, footer=None, all=None, dataframe=None):
    
    def check_span(row_list):
        #print(row_list)
        span_list = [1 for x in row_list]
        i=0
        while i<len(row_list):
            j=i+1
            while j<len(row_list):
                #print("checking ",i," and ",j)
                if (row_list[i]==row_list[j]):
                    #print("updating ",i)
                    span_list[i]=span_list[i]+1
                    span_list[j]=0
                    #print("zeroing ",j)
                    j=j+1
                else:
                    #print("breaking")
                    break
            i=j

        #print(len(row_list))
        #print(span_list)
        return span_list
    # Display the results in a popup window
    # popup window for the Results but only one time after first 
    # set of results start coming in
    fontStyle_sub_title = tkfont.Font(root=window, family="Calibri", size="14", weight="bold")         
   
    #l={}
    if header:
        row_num=0
        row_index = data[row_num][0]
        row_list = data[row_num][1:]
        check_span(row_list)
        if (row_index=="title"):
            tk.Label0 = tk.Label(window, text="", font=fontStyle_sub_title)
            tk.Label0.grid(row=0, column=0, sticky=tk.NSEW, padx=20)
            tk.Label1 = tk.Label(window, text=row_list[0], font=fontStyle_sub_title)
            tk.Label1.grid(row=0, column=2, columnspan=5)
        row_num=1
        row_index = data[row_num][0]
        row_list = data[row_num][1:]
        while (row_index=="header") :
            span_list = check_span(row_list)
            l = tk.Label(window, text="", padx=20)
            l.grid(row=row_num, column=0)
            for j in range(len(row_list)):
                if (span_list[j]!=0):
                    l = tk.Label(window, text=row_list[j], relief=RIDGE, font=fontStyle_sub_title)
                    l.grid(row=row_num, column=j+1, columnspan=span_list[j], sticky=tk.NSEW)
            row_num = row_num+1
            if (row_num<len(data)):
                row_index = data[row_num][0]
                row_list = data[row_num][1:]
            else:
                break
    
    if dataframe is not None:
        data = dataframe.values.tolist()
        all=True
    
    if all:
        row_num = row 
        for i in range(len(data)):       
            l = tk.Label(window, text="", padx=20)
            l.grid(row=row_num, column=0)
            row_list = data[i]
            #print(row_list)
            for j in range(len(row_list)):
                l = tk.Label(window, text=row_list[j], relief=RIDGE, font=fontStyle_sub_title)
                l.grid(row=row_num, column=j+1, sticky=tk.NSEW)
            row_num = row_num+1
        row=None
        
    if row is not None:
        row_num = row 
        l = tk.Label(window, text="", padx=20)
        l.grid(row=row_num, column=0)
        for j in range(len(data)):
            l = tk.Label(window, text=data[j], relief=RIDGE, font=fontStyle_sub_title)
            l.grid(row=row_num, column=j+1, sticky=tk.NSEW)
        row_num = row_num+1
        
    if footer is not None:
        row_num=footer
        row_index = data[0]
        row_list = data[1:]
        l9 = tk.Label(window, text=row_list[0])
        l9.grid(row=footer+4, column=1, pady = 10, columnspan = 5, sticky=tk.W)
    
    return row_num
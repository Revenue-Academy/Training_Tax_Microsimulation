# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 20:56:40 2022

@author: wb305167
"""
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo
from tkinter import filedialog

from threading import Thread

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#from taxcalc import *

from PIL import Image,ImageTk
        
def display_tax_expenditure(self, widget, varname):
    self.active_tax = self.find_active_taxes()
    if (tax_type not in self.active_tax):
        self.msg_window = tk.Toplevel()
        self.msg_window.geometry("250x100+300+300")
        self.msg_window_l1=Label(self.msg_window, text="Tax Type Not Selected", font = self.fontStyle_sub_title)
        self.msg_window_l1.place(relx = 0.10, rely = 0.10, anchor = "w")   
        tax_expenditure_msg_button = tk.Button(self.msg_window, text="Continue", command=lambda: self.clear_chk(widget, self.msg_window))
        tax_expenditure_msg_button.place(relx = 0.35, rely = 0.50, anchor = "w")
        self.msg_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(widget, self.msg_window))        
    else:
        self.vars[tax_type+'_tax_expenditure'] = int(widget.get())
        if (self.vars[tax_type+'_tax_expenditure']):        
            self.entry_benchmark_filename = Entry(self.TAB4, width=30, font = self.fontStyle)
            self.entry_benchmark_filename.place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_y,
                                      anchor = "e")
            self.entry_benchmark_filename.insert(END, self.vars['benchmark_filename'])
            self.button_benchmark_filename = ttk.Button(self.TAB4, text = "Change Benchmark File", style='my.TButton', command=self.input_benchmark_filename)
            self.button_benchmark_filename.place(relx = self.block_1_entry_x,
                                       rely = self.block_1_entry_y, anchor = "w")        
            self.button_generate_tax_expenditures = ttk.Button(self.TAB4, text = "Generate Tax Expenditures", style='my.TButton', command=self.clicked_generate_tax_expenditures)
            self.button_generate_tax_expenditures.place(relx = self.button_1_pos_x, 
                                                     rely = self.button_1_pos_y, anchor = "w")     
  
def tab4(self):

        self.l3A=Label(self.TAB4,text="Tax Expenditures",
                 font = self.fontStyle_sub_title)
        self.l3A.place(relx = 0.1, rely = 0.1, anchor = "w")
        
        
        '''
        self.tax_expenditure_chk = tk.IntVar()
        self.tax_expenditure_chk_box = tk.Checkbutton(self.TAB4, text='Estimate Tax Expenditures', font = self.fontStyle, variable=self.tax_expenditure_chk, command=lambda: self.display_tax_expenditure(self.tax_expenditure_chk, 'tax_expenditure'))
        self.tax_expenditure_chk_box.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
        '''
        self.button_generate_tax_exp = ttk.Button(self.TAB4, text = "Generate Tax Expenditure", style='my.TButton', command=self.clicked_generate_tax_expenditures)
        self.button_generate_tax_exp.place(relx = 0.1,rely = 0.2, anchor = "w")
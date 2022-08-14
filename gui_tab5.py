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

def display_distribution_table(self, widget, tax_type, block_1_title_pos_x):
    #print("I am inside display distribution table")
    self.vars[tax_type+'_display_distribution_table_by_attribute'] = int(widget.get())
    #print("self.vars[tax_type+'_display_distribution_table'] ",self.vars[tax_type+'_display_distribution_table'])
    #print("tax_type+'_distribution_json_filename' ", self.vars[tax_type+'_distribution_json_filename'])    

def display_distribution(self, widget, tax_type, block_1_title_pos_x):
    self.active_tax = self.find_active_taxes()
    #print(self.active_tax)
    if (tax_type not in self.active_tax):
        self.msg_window = tk.Toplevel()
        self.msg_window.geometry("250x100+300+300")
        self.msg_window_l1=tk.Label(self.msg_window, text="Tax Type Not Selected", font = self.fontStyle_sub_title)
        self.msg_window_l1.place(relx = 0.10, rely = 0.10, anchor = "w")    
        elasticity_msg_button = tk.Button(self.msg_window, text="Continue", command=lambda: self.clear_chk(widget, self.msg_window))
        elasticity_msg_button.place(relx = 0.35, rely = 0.50, anchor = "w")
        self.msg_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(widget, self.msg_window))
    else:
        self.vars[tax_type+'_distribution_table'] = int(widget.get())
        #print("self.vars[tax_type+'_distribution_table'] ", self.vars[tax_type+'_distribution_table'])
        if self.vars[tax_type+'_distribution_table']:
            self.grid_placement(block_1_title_pos_x)
            self.l1_distribution[tax_type]=Label(self.TAB5,text="Data Inputs for Distribution Table "+ tax_type.upper(),
                     font = self.fontStyle_sub_title)
            self.l1_distribution[tax_type].place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
            
            self.entry_distribution_json_filename[tax_type] = Entry(self.TAB5, width=30, font = self.fontStyle)
            self.entry_distribution_json_filename[tax_type].place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_1_y,
                                      anchor = "e")
            self.entry_distribution_json_filename[tax_type].insert(END, self.vars[tax_type+'_distribution_json_filename'])
            self.button_distribution_json_filename[tax_type] = ttk.Button(self.TAB5, text = "Change Distribution Inputs File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_distribution_json_filename[tax_type], tax_type+'_distribution_json_filename'))
            self.button_distribution_json_filename[tax_type].place(relx = self.block_1_entry_x,
                                       rely = self.block_1_entry_1_y, anchor = "w")

            self.display_distribution_table_attr_chk[tax_type] = tk.IntVar()
            self.display_distribution_table_attr_chk_box[tax_type] = tk.Checkbutton(self.TAB5, text='Generate Distribution Table by Attribute', 
                                                           font = self.fontStyle,
                                                           state = tk.DISABLED,
                                                           variable=self.display_distribution_table_attr_chk[tax_type], command=lambda: self.display_distribution_table(self.display_distribution_table_chk[tax_type], tax_type, self.block_distribution_pos_x[tax_type]))
            self.display_distribution_table_attr_chk_box[tax_type].place(relx = self.block_distribution_pos_x[tax_type], 
                                                rely = self.block_1_entry_1_y+2*self.entry_entry_gap_y, anchor = "w")

            
            self.button_generate_distribution = ttk.Button(self.TAB5, text = "Generate Distribution Tables by income Deciles", style='my.TButton')
            self.button_generate_distribution.place(relx = self.block_distribution_pos_x[tax_type],
                                                    rely = self.block_1_entry_1_y+4*self.entry_entry_gap_y, anchor = "w")       
            self.button_generate_distribution.config(command=lambda: self.clicked_generate_distribution('dist_by_decile'))
            
            self.button_generate_distribution = ttk.Button(self.TAB5, text = "Generate Total Tax Contribution by income levels", style='my.TButton')
            self.button_generate_distribution.place(relx = self.block_distribution_pos_x[tax_type],
                                                    rely = self.block_1_entry_1_y+6*self.entry_entry_gap_y, anchor = "w")       
            self.button_generate_distribution.config(command=lambda: self.clicked_generate_distribution('dist_by_income'))
            
        else:
            self.vars[tax_type+'_display_revenue_table'] = 1
            self.save_inputs()
            self.l1_distribution[tax_type].destroy()
            self.entry_distribution_json_filename[tax_type].destroy()
            self.button_distribution_json_filename[tax_type].destroy()
            self.display_distribution_table_attr_chk_box[tax_type].destroy()
            self.button_generate_distribution.destroy()
             
def tab5(self):
    self.l1_distribution = {}
    self.entry_distribution_json_filename = {}
    self.button_distribution_json_filename = {}
    self.display_distribution_table_attr_chk = {}
    self.display_distribution_table_attr_chk_box = {} 
    # for positions of the different tax type on the screen
    self.block_distribution_pos_x = {}
    pos_x = [0.10, 0.40, 0.70]

    for tax_type in self.tax_list:
        self.vars[tax_type+'_distribution_table'] = 0 
        self.vars[tax_type+'_display_distribution_table'] = 0
        self.vars[tax_type+'_display_distribution_table_by_attribute'] = 0
        self.vars[tax_type+'_display_revenue_table'] = 1
    self.save_inputs()
    self.block_distribution_pos_x = self.allocate_pos_x(pos_x, self.status,
                                                    self.block_distribution_pos_x)
         
    self.TAB5_root_title=Label(self.TAB5,text="Tax Microsimulation Model",
             font = self.fontStyle_title)
    self.TAB5_root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")

    self.TAB5_root_title=Label(self.TAB5,text="Distribution Tables",
             font = self.fontStyle_sub_title)
    self.TAB5_root_title.place(relx = self.title_pos_x, rely = self.sub_title_pos_y, anchor = "n")
    
    
    self.pit_distribution_chk = tk.IntVar()
    self.pit_distribution_chk_box = tk.Checkbutton(self.TAB5, text='Personal Income Tax', 
                                                   font = self.fontStyle,
                                                   state = self.status['pit'],                                                   
                                                   variable=self.pit_distribution_chk, command=lambda: self.display_distribution(self.pit_distribution_chk, 'pit', self.block_distribution_pos_x['pit']))
    self.pit_distribution_chk_box.place(relx = self.block_distribution_pos_x['pit'], 
                                        rely = self.block_1_title_box_y, anchor = "w")

    self.cit_distribution_chk = tk.IntVar()
    self.cit_distribution_chk_box = tk.Checkbutton(self.TAB5, text='Corporate Income Tax', 
                                                   font = self.fontStyle,
                                                   state = self.status['cit'],                                                    
                                                   variable=self.cit_distribution_chk, command=lambda: self.display_distribution(self.cit_distribution_chk, 'cit', self.block_distribution_pos_x['cit']))
    self.cit_distribution_chk_box.place(relx = self.block_distribution_pos_x['cit'], 
                                        rely = self.block_1_title_box_y, anchor = "w")

    self.vat_distribution_chk = tk.IntVar()
    self.vat_distribution_chk_box = tk.Checkbutton(self.TAB5, text='Value Added Tax', 
                                                   font = self.fontStyle,
                                                   state = self.status['vat'],                                                    
                                                   variable=self.vat_distribution_chk, command=lambda: self.display_distribution(self.vat_distribution_chk, 'vat', self.block_distribution_pos_x['vat']))
    self.vat_distribution_chk_box.place(relx = self.block_distribution_pos_x['vat'], 
                                        rely = self.block_1_title_box_y, anchor = "w") 
    
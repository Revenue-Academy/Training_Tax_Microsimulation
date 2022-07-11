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
from super_combo import super_combo
#from taxcalc import *

from PIL import Image,ImageTk

def get_gf_dict(self, event):
    self.attribute_value = self.selected_attribute_widget.get()
    #print('selected_attribute ', self.attribute_value)
    self.growfactors_widget_dict[1][1].config(values=self.tab_growfactors.policy_options(self.growfactors[self.attribute_value]))    
    
def tab7(self):
    #self.attribute_columns is assigned in get_growfactors_dict function
    if len(self.attribute_columns)>0:
        #print('self.attribute_columns ',self.attribute_columns)
        #print('self.attribute_types ', self.attribute_types)
        #attribute_name=self.attribute_columns[0]
        attribute_value=self.attribute_types[0]
        self.selected_attribute_widget = tk.StringVar()
        self.sector_combo = ttk.Combobox(self.TAB7, textvariable=self.selected_attribute_widget, value=self.attribute_types, font=self.text_font)
        self.sector_combo.current(0)
        self.sector_combo.place(relx = 0.1, 
                                rely = 0.05, anchor = "w", width=200)
        self.sector_combo.bind("<<ComboboxSelected>>", lambda event: self.get_gf_dict(event))
        #print('self.growfactors[self.attribute_types[0]] ',self.growfactors[self.attribute_types[0]])
        #self.year_value_pairs_growfactors_dict = len(self.growfactors[self.attribute_types[0]][list(self.growfactors[self.attribute_types[0]].keys())[0]]['Year'])

    else:
        #attribute_name=None
        attribute_value=None
        self.selected_attribute_widget=None
        self.year_value_pairs_growfactors_dict=0
        #print('ATTRIBUTE_READ_VARS ', self.ATTRIBUTE_READ_VARS)
        #print('self.growfactors ', self.growfactors)
        #self.year_value_pairs_growfactors_dict = len(self.growfactors[list(self.growfactors.keys())[0]]['Year'])
    
    growfactors_combo_width = int(self.vars['end_year'])-int(self.vars['start_year']) + 1
    self.tab_growfactors = super_combo(self.TAB7, self.growfactors, 'Year', 
                                       'Value', 0.01, 0.15, attribute_value, 
                                       self.selected_attribute_widget, 
                                       editable_field_year=0, 
                                       num_combos=growfactors_combo_width)
    (self.button_growfactors, self.growfactors_widget_dict) = self.tab_growfactors.display_widgets(self.TAB7)
    # this is the number of year value pairs in the growfactors
    self.year_value_pairs_growfactors_dict = len(self.growfactors_widget_dict[1][2])
    self.button_growfactors.configure(command=self.clicked_generate_policy_revenues)
        
    return

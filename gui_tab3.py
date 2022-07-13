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
from super_combo import super_combo
rcParams.update({'figure.autolayout': True})

def display_elasticity(self, widget, tax_type, block_1_title_pos_x):
    #self.active_tax = self.find_active_taxes()
    #print(self.active_tax)
    #print(tax_type)
    if (tax_type not in self.active_tax_list):
        self.msg_window = tk.Toplevel()
        self.msg_window.geometry("250x100+200+200")
        self.msg_window_l1=tk.Label(self.msg_window, text="Tax Type Not Selected", font = self.fontStyle_sub_title)
        self.msg_window_l1.place(relx = 0.10, rely = 0.10, anchor = "w")    
        elasticity_msg_button = tk.Button(self.msg_window, text="Continue", command=lambda: self.clear_chk(widget, self.msg_window))
        elasticity_msg_button.place(relx = 0.35, rely = 0.50, anchor = "w")
        self.msg_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(widget, self.msg_window))
    else:
        self.vars[tax_type+'_adjust_behavior'] = int(widget.get())
        self.save_inputs()
        self.elasticity_json = self.get_elasticity_dict(self.tax_type)
        num_combos = len(self.elasticity_json[list(self.elasticity_json.keys())[0]]['threshold'])        
        if (self.vars[tax_type+'_adjust_behavior']):
            self.year_value_pairs_elasticity_dict = 3       
            self.tab_elasticity = super_combo(self.TAB3, self.elasticity_json, 'threshold', 'value', 0.01, 0.20, editable_field_year=1, elasticity=1, num_combos=num_combos)
            (self.button_save_elasticity, self.elasticity_widget_dict) = self.tab_elasticity.display_widgets(self.TAB3)
            self.elasticity_widget_dict[1][1].config(values=self.tab_elasticity.policy_options(self.elasticity_json))
            self.button_save_elasticity.configure(command=self.clicked_generate_policy_revenues)
            #self.button_save_elasticity.configure(command=self.clicked_generate_policy_revenues('rev_behavior'))
        else:
            self.save_inputs()
            self.tab_elasticity.destroy_all_widgets()
            
def tab3(self, tax_type):
    
    self.block_elasticity_pos_x = {}
    pos_x = [0.1, 0.4, 0.67]
    for tax_type in self.tax_list:
        self.vars[tax_type+'_adjust_behavior'] = 0
    
    self.block_elasticity_pos_x = self.allocate_pos_x(pos_x, self.status,
                                                    self.block_elasticity_pos_x)

    #print('self.block_elasticity_pos_x ', self.block_elasticity_pos_x)
    self.pit_elasticity_chk = tk.IntVar()
    self.pit_elasticity_chk_box = tk.Checkbutton(self.TAB3, text='Personal Income Tax', 
                                                 font = self.fontStyle,
                                                 state = self.status['pit'],
                                                 variable=self.pit_elasticity_chk, command=lambda: self.display_elasticity(self.pit_elasticity_chk, 'pit', self.block_elasticity_pos_x['pit']))
    self.pit_elasticity_chk_box.place(relx = self.block_elasticity_pos_x['pit'], 
                                      rely = self.block_1_title_box_y, anchor = "w")
    #print('self.block_elasticity_pos_x ', self.block_elasticity_pos_x)
    self.cit_elasticity_chk = tk.IntVar()
    self.cit_elasticity_chk_box = tk.Checkbutton(self.TAB3, text='Corporate Income Tax', 
                                                 font = self.fontStyle,
                                                 state = self.status['cit'],
                                                 variable=self.cit_elasticity_chk, command=lambda: self.display_elasticity(self.cit_elasticity_chk, 'cit', self.block_elasticity_pos_x['cit']))
    self.cit_elasticity_chk_box.place(relx = self.block_elasticity_pos_x['cit'], 
                                      rely = self.block_1_title_box_y, anchor = "w")
    
    #print('self.block_elasticity_pos_x ', self.block_elasticity_pos_x)
    self.vat_elasticity_chk = tk.IntVar()
    self.vat_elasticity_chk_box = tk.Checkbutton(self.TAB3, text='Value Added Tax', 
                                                 font = self.fontStyle,
                                                 state = self.status['vat'],
                                                 variable=self.vat_elasticity_chk, command=lambda: self.display_elasticity(self.vat_elasticity_chk, 'vat', self.block_elasticity_pos_x['vat']))
    self.vat_elasticity_chk_box.place(relx = self.block_elasticity_pos_x['vat'], 
                                      rely = self.block_1_title_box_y, anchor = "w")
    return

    

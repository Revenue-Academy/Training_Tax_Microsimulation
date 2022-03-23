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

def grid_placement_tab3(self, block_1_title_pos_x, block_1_title_pos_y=None):
       
    self.button_2_TAB3_pos_x = block_1_title_pos_x
    self.block_block_gap = 0.1
    if block_1_title_pos_y is None:
        self.block_1_title_pos_y = 0.20
    else:
        self.block_1_title_pos_y = block_1_title_pos_y      
    self.button_1_TAB3_pos_y = self.block_1_title_pos_y+self.block_title_entry_gap_y

    self.block_2_TAB3_entry_1_1_x = block_1_title_pos_x
    self.block_2_TAB3_title_pos_y = self.button_1_TAB3_pos_y + self.block_block_gap
    self.text_entry_gap = 0.03
    self.block_2_TAB3_entry_1_1_y = (self.block_2_TAB3_title_pos_y+
                                self.block_title_entry_gap_y+
                                self.text_entry_gap)
    self.block_2_TAB3_combo_entry_gap_x = 0.14
    self.block_2_TAB3_entry_entry_gap_x = 0.05
    self.block_2_TAB3_entry_entry_gap_y = 0.06
    
    self.block_2_TAB3_entry_1_2_x = self.block_2_TAB3_entry_1_1_x + self.block_2_TAB3_combo_entry_gap_x
    self.block_2_TAB3_entry_1_3_x = self.block_2_TAB3_entry_1_2_x + self.block_2_TAB3_entry_entry_gap_x      
    self.block_2_TAB3_entry_1_4_x = self.block_2_TAB3_entry_1_3_x + self.block_2_TAB3_entry_entry_gap_x      

    self.block_2_TAB3_entry_2_1_y = (self.block_2_TAB3_entry_1_1_y +
                                     self.block_2_TAB3_entry_entry_gap_y)
  
    self.button_add_reform_x = self.block_2_TAB3_entry_1_4_x + self.block_2_TAB3_entry_entry_gap_x + 0.02
 
       
def display_elasticity(self, widget, tax_type, block_1_title_pos_x):
    self.active_tax = self.find_active_taxes()
    #print(self.active_tax)
    #print(tax_type)
    if (tax_type not in self.active_tax):
        self.msg_window = tk.Toplevel()
        self.msg_window.geometry("250x100+200+200")
        self.msg_window_l1=tk.Label(self.msg_window, text="Tax Type Not Selected", font = self.fontStyle_sub_title)
        self.msg_window_l1.place(relx = 0.10, rely = 0.10, anchor = "w")    
        elasticity_msg_button = tk.Button(self.msg_window, text="Continue", command=lambda: self.clear_chk(widget, self.msg_window))
        elasticity_msg_button.place(relx = 0.35, rely = 0.50, anchor = "w")
        self.msg_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(widget, self.msg_window))
    else:
        self.vars[tax_type+'_adjust_behavior'] = int(widget.get())
        if (self.vars[tax_type+'_adjust_behavior']):
            
            self.grid_placement_tab3(block_1_title_pos_x)
            """
            self.l1_elasticity[tax_type]=Label(self.TAB3,text="Elasticity Data Inputs "+ tax_type.upper(),
                     font = self.fontStyle_sub_title)
            self.l1_elasticity[tax_type].place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
            
            self.entry_elasticity_filename[tax_type] = Entry(self.TAB3, width=30, font = self.fontStyle)
            self.entry_elasticity_filename[tax_type].place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_1_y,
                                      anchor = "e")
            self.entry_elasticity_filename[tax_type].insert(END, self.vars[tax_type+'_elasticity_filename'])
            self.button_elasticity_filename[tax_type] = ttk.Button(self.TAB3, text = "Elasticity JSON File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_elasticity_filename[tax_type], tax_type+'_elasticity_filename'))
            self.button_elasticity_filename[tax_type].place(relx = self.block_1_entry_x,
                                       rely = self.block_1_entry_1_y, anchor = "w")
            
            """
            self.l2_TAB3[tax_type]=Label(self.TAB3, text="Elasticity", font = self.fontStyle_sub_title)
            self.l2_TAB3[tax_type].place(relx = self.sub_title_pos_x, rely = self.sub_title_pos_y, anchor = "w")
            
            self.l3_TAB3[tax_type]=Label(self.TAB3, text="Select Elasticity Parameter: ", font = self.fontStyle)
            self.l3_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_1_x, 
                     rely = self.block_2_TAB3_entry_1_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_dict[tax_type], self.elasticity_items_list[tax_type] = self.elasticity_options(tax_type)
            print(self.elasticity_dict[tax_type])
            #print(self.elasticity_items_list[tax_type])
            #self.policy_options_list.remove('gst_rate')
            self.elasticity_widget_dict[tax_type] = {}
            self.elasticity_selected_dict[tax_type] = {}
            self.num_elasticity_changes[tax_type] = 1
            # self.elasticity_widget_dict[tax_type][1] is the first rows of the
            # dropdownlist and entry boxes
            # calling create_elasticity_widgets creates the second and 
            # subsequent rows
            self.elasticity_widget_dict[tax_type][1] = {}
            self.elasticity_selected_dict[tax_type][1] = {}
            self.elasticity_widget_dict[tax_type][1][1] = ttk.Combobox(self.TAB3, value=self.elasticity_items_list[tax_type], font=self.text_font, name=tax_type+'_'+str(self.num_elasticity_changes[tax_type]))
            self.elasticity_widget_dict[tax_type][1][1].current(0)
            self.elasticity_widget_dict[tax_type][1][1].place(relx = self.block_2_TAB3_entry_1_1_x, 
                            rely = self.block_2_TAB3_entry_1_1_y, anchor = "w", width=200)
            
            self.elasticity_widget_dict[tax_type][1][1].bind("<<ComboboxSelected>>", lambda event: self.show_elasticity_selection(event, self.elasticity_dict[tax_type], self.elasticity_selected_dict[tax_type], self.elasticity_widget_dict[tax_type], tax_type))
            
            self.l3_TAB3[tax_type]=Label(self.TAB3,text="Threshold1: ", font = self.fontStyle)
            self.l3_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_2_x, 
                     rely = self.block_2_TAB3_entry_1_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_widget_dict[tax_type][1][2] = Entry(self.TAB3, width=10, font = self.fontStyle)
            self.elasticity_widget_dict[tax_type][1][2].place(relx = self.block_2_TAB3_entry_1_2_x, rely = self.block_2_TAB3_entry_1_1_y, anchor = "w")
            
            self.l4_TAB3[tax_type]=Label(self.TAB3,text="Threshold2: ", font = self.fontStyle)
            self.l4_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_3_x, 
                     rely = self.block_2_TAB3_entry_1_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_widget_dict[tax_type][1][3] = Entry(self.TAB3, width=10, font = self.fontStyle)
            self.elasticity_widget_dict[tax_type][1][3].place(relx = self.block_2_TAB3_entry_1_3_x, rely = self.block_2_TAB3_entry_1_1_y, anchor = "w")
        
            self.l5_TAB3[tax_type]=Label(self.TAB3,text="Threshold3: ", font = self.fontStyle)
            self.l5_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_4_x, 
                     rely = self.block_2_TAB3_entry_1_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_widget_dict[tax_type][1][4] = Entry(self.TAB3, width=10, font = self.fontStyle)
            self.elasticity_widget_dict[tax_type][1][4].place(relx = self.block_2_TAB3_entry_1_4_x, rely = self.block_2_TAB3_entry_1_1_y, anchor = "w")
        
            self.l6_TAB3[tax_type]=Label(self.TAB3,text="Value1: ", font = self.fontStyle)
            self.l6_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_2_x, 
                     rely = self.block_2_TAB3_entry_2_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_widget_dict[tax_type][1][5] = Entry(self.TAB3, width=10, font = self.fontStyle)
            self.elasticity_widget_dict[tax_type][1][5].place(relx = self.block_2_TAB3_entry_1_2_x, rely = self.block_2_TAB3_entry_2_1_y, anchor = "w")
            
            self.l7_TAB3[tax_type]=Label(self.TAB3,text="Value2: ", font = self.fontStyle)
            self.l7_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_3_x, 
                     rely = self.block_2_TAB3_entry_2_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_widget_dict[tax_type][1][6] = Entry(self.TAB3, width=10, font = self.fontStyle)
            self.elasticity_widget_dict[tax_type][1][6].place(relx = self.block_2_TAB3_entry_1_3_x, rely = self.block_2_TAB3_entry_2_1_y, anchor = "w")
        
            self.l8_TAB3[tax_type]=Label(self.TAB3,text="Value3: ", font = self.fontStyle)
            self.l8_TAB3[tax_type].place(relx = self.block_2_TAB3_entry_1_4_x, 
                     rely = self.block_2_TAB3_entry_2_1_y-self.text_entry_gap, anchor = "w")
            self.elasticity_widget_dict[tax_type][1][7] = Entry(self.TAB3, width=10, font = self.fontStyle)
            self.elasticity_widget_dict[tax_type][1][7].place(relx = self.block_2_TAB3_entry_1_4_x, rely = self.block_2_TAB3_entry_2_1_y, anchor = "w")
        
            
            self.num_elasticity_changes[tax_type] += 1
            print("num in gui: ", self.num_elasticity_changes[tax_type])
            self.button_add_reform[tax_type] = ttk.Button(self.TAB3, text="+", style='my.TButton', command= lambda: self.create_elasticity_widgets(self.TAB3, self.elasticity_selected_dict[tax_type], self.elasticity_widget_dict[tax_type], self.num_elasticity_changes[tax_type], tax_type), width=2)
            self.button_add_reform[tax_type].place(relx = self.button_add_reform_x, rely = self.block_2_TAB3_entry_1_1_y, anchor = "w")        
            #print("gui tab3: ", self.elasticity_widget_dict[tax_type][self.num_elasticity_changes[tax_type]][7].get())            
            self.button_generate_elasticity_dict[tax_type] = ttk.Button(self.TAB3, text = "Update Elasticities", style='my.TButton', command=lambda: self.clicked_generate_elasticity_dict(self.elasticity_selected_dict[tax_type], self.elasticity_widget_dict[tax_type], tax_type))
            #self.button_2_TAB3_pos_x = self.button_1_pos_x
            self.button_2_TAB3_pos_y = (self.block_2_TAB3_entry_2_1_y+(self.num_elasticity_changes[tax_type]-1)*(self.block_2_TAB3_entry_entry_gap_y)) +self.entry_button_gap
            self.button_generate_elasticity_dict[tax_type].place(relx = self.button_2_TAB3_pos_x,
                                                        rely = self.button_2_TAB3_pos_y, anchor = "w")       
            
def tab3(self):
   
    self.l1_TAB3 = {}
    self.l2_TAB3 = {}
    self.l3_TAB3 = {}
    self.l4_TAB3 = {}
    self.l5_TAB3 = {}
    self.l6_TAB3 = {}
    self.l7_TAB3 = {}
    self.l8_TAB3 = {}
    self.l1_elasticity = {}
    self.entry_elasticity_filename = {}
    self.button_elasticity_filename = {}
    self.elasticity_widget_dict = {}
    self.elasticity_selected_dict = {}
    self.num_elasticity_changes = {}
    self.button_add_reform = {}
    self.button_generate_elasticity_dict = {}    
    self.elasticity_dict = {}
    self.elasticity_items_list = {}
    self.block_elasticity_pos_x = {}

    pos_x = [0.01, 0.34, 0.67]

    for tax_type in self.tax_list:
        self.vars[tax_type+'_adjust_behavior'] = 0
    
    self.block_elasticity_pos_x = self.allocate_pos_x(pos_x, self.status,
                                                    self.block_elasticity_pos_x)
    
    self.TAB3_root_title=Label(self.TAB3,text="Tax Microsimulation Model",
             font = self.fontStyle_title)
    self.TAB3_root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")

    self.TAB3_root_title=Label(self.TAB5,text="Adjust for Behavioral Response",
             font = self.fontStyle_sub_title)
    self.TAB3_root_title.place(relx = self.title_pos_x, rely = self.sub_title_pos_y, anchor = "n") 
    
    self.pit_elasticity_chk = tk.IntVar()
    self.pit_elasticity_chk_box = tk.Checkbutton(self.TAB3, text='Personal Income Tax', 
                                                 font = self.fontStyle,
                                                 state = self.status['pit'],
                                                 variable=self.pit_elasticity_chk, command=lambda: self.display_elasticity(self.pit_elasticity_chk, 'pit', self.block_elasticity_pos_x['pit']))
    self.pit_elasticity_chk_box.place(relx = self.block_settings_pos_x['pit'], 
                                      rely = self.block_1_title_box_y, anchor = "w")

    self.cit_elasticity_chk = tk.IntVar()
    self.cit_elasticity_chk_box = tk.Checkbutton(self.TAB3, text='Corporate Income Tax', 
                                                 font = self.fontStyle,
                                                 state = self.status['cit'],
                                                 variable=self.cit_elasticity_chk, command=lambda: self.display_elasticity(self.cit_elasticity_chk, 'cit', self.block_elasticity_pos_x['cit']))
    self.cit_elasticity_chk_box.place(relx = self.block_settings_pos_x['cit'], 
                                      rely = self.block_1_title_box_y, anchor = "w")

    self.vat_elasticity_chk = tk.IntVar()
    self.vat_elasticity_chk_box = tk.Checkbutton(self.TAB3, text='Value Added Tax', 
                                                 font = self.fontStyle,
                                                 state = self.status['vat'],
                                                 variable=self.vat_elasticity_chk, command=lambda: self.display_elasticity(self.vat_elasticity_chk, 'vat', self.block_elasticity_pos_x['vat']))
    self.vat_elasticity_chk_box.place(relx = self.block_settings_pos_x['vat'], 
                                      rely = self.block_1_title_box_y, anchor = "w") 


    self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
    #image = tk.PhotoImage(file="blank.png")
    self.pic = tk.Label(self.TAB3,image=self.image)
    self.pic.place(relx = 0.5, rely = 0.2, anchor = "nw")
    self.pic.image = self.image
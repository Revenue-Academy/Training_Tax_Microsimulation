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
    print("I am inside display distribution table")
    self.vars[tax_type+'_display_distribution_table'] = int(widget.get())
    print("self.vars[tax_type+'_display_distribution_table'] ",self.vars[tax_type+'_display_distribution_table'])
    print("tax_type+'_distribution_json_filename' ", self.vars[tax_type+'_distribution_json_filename'])    

def display_distribution(self, widget, tax_type, block_1_title_pos_x):
    self.active_tax = self.find_active_taxes()
    print(self.active_tax)
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
        print("self.vars[tax_type+'_distribution_table'] ", self.vars[tax_type+'_distribution_table'])
        if self.vars[tax_type+'_distribution_table']:
            self.grid_placement(block_1_title_pos_x)
            self.l1_distribution[tax_type]=Label(self.TAB5,text="Data Inputs "+ tax_type.upper(),
                     font = self.fontStyle_sub_title)
            self.l1_distribution[tax_type].place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
            
            self.entry_distribution_json_filename[tax_type] = Entry(self.TAB5, width=30, font = self.fontStyle)
            self.entry_distribution_json_filename[tax_type].place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_1_y,
                                      anchor = "e")
            self.entry_distribution_json_filename[tax_type].insert(END, self.vars[tax_type+'_distribution_json_filename'])
            self.button_distribution_json_filename[tax_type] = ttk.Button(self.TAB5, text = "Change Data File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_distribution_json_filename[tax_type], tax_type+'_distribution_json_filename'))
            self.button_distribution_json_filename[tax_type].place(relx = self.block_1_entry_x,
                                       rely = self.block_1_entry_1_y, anchor = "w")

            self.display_distribution_table_chk[tax_type] = tk.IntVar()
            self.display_distribution_table_chk_box[tax_type] = tk.Checkbutton(self.TAB5, text='Display Distribution Table', 
                                                           font = self.fontStyle,                                              
                                                           variable=self.display_distribution_table_chk[tax_type], command=lambda: self.display_distribution_table(self.display_distribution_table_chk[tax_type], tax_type, self.block_distribution_pos_x[tax_type]))
            self.display_distribution_table_chk_box[tax_type].place(relx = self.block_distribution_pos_x[tax_type], 
                                                rely = self.block_1_entry_1_y+2*self.entry_entry_gap_y, anchor = "w")
        
def tab5(self):
    self.l1_distribution = {}
    self.entry_distribution_json_filename = {}
    self.button_distribution_json_filename = {}
    self.display_distribution_table_chk = {}
    self.display_distribution_table_chk_box = {}    
    # for positions of the different tax type on the screen
    self.block_distribution_pos_x = {}
    pos_x = [0.10, 0.40, 0.70]    
    for tax_type in self.tax_list:
        self.vars[tax_type+'_distribution_table'] = 0 
        self.vars[tax_type+'_display_distribution_table'] = 0
   
    self.block_distribution_pos_x = self.allocate_pos_x(pos_x, self.status,
                                                    self.block_distribution_pos_x)
    
    self.vars['pit_distribution_json_filename'] = 'pit_distribution_macedonia.json'
    self.vars['cit_distribution_json_filename'] = 'cit_distribution_egypt.json'
    self.vars['vat_distribution_json_filename'] = 'vat_distribution.json'
         
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
    


    
    
    """    
    self.TAB5_l2=Label(self.TAB5, text="Elasticity", font = self.fontStyle_sub_title)
    self.TAB5_l2.place(relx = self.block_1_title_pos_x, rely = self.block_2_TAB5_title_pos_y, anchor = "w")
    
    self.TAB5_l3=Label(self.TAB5, text="Select Elasticity Parameter: ", font = self.fontStyle)
    self.TAB5_l3.place(relx = self.block_2_TAB5_entry_1_1_x, 
             rely = self.block_2_TAB5_entry_1_1_y-self.text_entry_gap, anchor = "w")

    self.elasticity_dict, self.elasticity_items_list = self.elasticity_options()
    #self.policy_options_list.remove('gst_rate')
    self.elasticity_widget_dict = {}
    self.elasticity_selected_dict = {}
    self.num_elasticity_changes = 1
    
   
    self.elasticity_widget_dict[1] = {}
    self.elasticity_selected_dict[1] = {}
    self.elasticity_widget_dict[1][1] = ttk.Combobox(self.TAB5, value=self.elasticity_items_list, font=self.text_font, name=str(self.num_elasticity_changes))
    self.elasticity_widget_dict[1][1].current(1)
    self.elasticity_widget_dict[1][1].place(relx = self.block_2_TAB5_entry_1_1_x, 
                    rely = self.block_2_TAB5_entry_1_1_y, anchor = "w", width=300)
    
    self.elasticity_widget_dict[1][1].bind("<<ComboboxSelected>>", self.show_elasticity_selection1)
    
    self.TAB5_l4=Label(self.TAB5,text="Threshold1: ", font = self.fontStyle)
    self.TAB5_l4.place(relx = self.block_2_TAB5_entry_1_2_x, 
             rely = self.block_2_TAB5_entry_1_1_y-self.text_entry_gap, anchor = "w")
    self.elasticity_widget_dict[1][2] = Entry(self.TAB5, width=10, font = self.fontStyle)
    self.elasticity_widget_dict[1][2].place(relx = self.block_2_TAB5_entry_1_2_x, rely = self.block_2_TAB5_entry_1_1_y, anchor = "w")
    
    self.TAB5_l5=Label(self.TAB5,text="Threshold2: ", font = self.fontStyle)
    self.TAB5_l5.place(relx = self.block_2_TAB5_entry_1_3_x, 
             rely = self.block_2_TAB5_entry_1_1_y-self.text_entry_gap, anchor = "w")
    self.elasticity_widget_dict[1][3] = Entry(self.TAB5, width=10, font = self.fontStyle)
    self.elasticity_widget_dict[1][3].place(relx = self.block_2_TAB5_entry_1_3_x, rely = self.block_2_TAB5_entry_1_1_y, anchor = "w")

    self.TAB5_l6=Label(self.TAB5,text="Threshold3: ", font = self.fontStyle)
    self.TAB5_l6.place(relx = self.block_2_TAB5_entry_1_4_x, 
             rely = self.block_2_TAB5_entry_1_1_y-self.text_entry_gap, anchor = "w")
    self.elasticity_widget_dict[1][4] = Entry(self.TAB5, width=10, font = self.fontStyle)
    self.elasticity_widget_dict[1][4].place(relx = self.block_2_TAB5_entry_1_4_x, rely = self.block_2_TAB5_entry_1_1_y, anchor = "w")

    self.TAB5_l7=Label(self.TAB5,text="Value1: ", font = self.fontStyle)
    self.TAB5_l7.place(relx = self.block_2_TAB5_entry_1_2_x, 
             rely = self.block_2_TAB5_entry_2_1_y-self.text_entry_gap, anchor = "w")
    self.elasticity_widget_dict[1][5] = Entry(self.TAB5, width=10, font = self.fontStyle)
    self.elasticity_widget_dict[1][5].place(relx = self.block_2_TAB5_entry_1_2_x, rely = self.block_2_TAB5_entry_2_1_y, anchor = "w")
    
    self.TAB5_l8=Label(self.TAB5,text="Value2: ", font = self.fontStyle)
    self.TAB5_l8.place(relx = self.block_2_TAB5_entry_1_3_x, 
             rely = self.block_2_TAB5_entry_2_1_y-self.text_entry_gap, anchor = "w")
    self.elasticity_widget_dict[1][6] = Entry(self.TAB5, width=10, font = self.fontStyle)
    self.elasticity_widget_dict[1][6].place(relx = self.block_2_TAB5_entry_1_3_x, rely = self.block_2_TAB5_entry_2_1_y, anchor = "w")

    self.TAB5_l9=Label(self.TAB5,text="Value3: ", font = self.fontStyle)
    self.TAB5_l9.place(relx = self.block_2_TAB5_entry_1_4_x, 
             rely = self.block_2_TAB5_entry_2_1_y-self.text_entry_gap, anchor = "w")
    self.elasticity_widget_dict[1][7] = Entry(self.TAB5, width=10, font = self.fontStyle)
    self.elasticity_widget_dict[1][7].place(relx = self.block_2_TAB5_entry_1_4_x, rely = self.block_2_TAB5_entry_2_1_y, anchor = "w")

    
    self.num_elasticity_changes += 1
    self.button_add_reform = ttk.Button(self.TAB5, text="+", style='my.TButton', command= lambda: self.create_elasticity_widgets(self.TAB5), width=2)
    self.button_add_reform.place(relx = self.button_add_reform_x, rely = self.block_2_TAB5_entry_1_1_y, anchor = "w")        
    
    self.button_generate_elasticity_dict = ttk.Button(self.TAB5, text = "Update Elasticities", style='my.TButton', command=self.clicked_generate_elasticity_dict)
    self.button_2_TAB5_pos_x = self.button_1_pos_x
    self.button_2_TAB5_pos_y = (self.block_2_TAB5_entry_2_1_y+(self.num_elasticity_changes-1)*(self.block_2_TAB5_entry_entry_gap_y)) +self.entry_button_gap
    self.button_generate_elasticity_dict.place(relx = self.button_2_TAB5_pos_x,
                                                rely = self.button_2_TAB5_pos_y, anchor = "w")       
    
    self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
    #image = tk.PhotoImage(file="blank.png")
    self.pic = tk.Label(self.TAB5,image=self.image)
    self.pic.place(relx = 0.5, rely = 0.2, anchor = "nw")
    self.pic.image = self.image
    """
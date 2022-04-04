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

def tab2(self):
    self.block_1_TAB2_title_pos_y = self.block_1_title_pos_y + 0.05
    self.block_1_TAB2_title_pos_x = self.block_1_title_pos_x - 0.05     
    self.button_1_TAB2_pos_x = self.block_1_title_pos_x - 0.10
    self.block_block_gap = 0.1         
    self.button_1_TAB2_pos_y = self.block_1_TAB2_title_pos_y+self.block_title_entry_gap_y
    self.button_1_pos_x = self.button_1_TAB2_pos_x

    self.block_2_TAB2_entry_1_1_x = 0.03
    self.block_2_TAB2_title_pos_y = self.button_1_TAB2_pos_y + self.block_block_gap
    self.text_entry_gap = 0.03
    self.block_2_TAB2_entry_1_1_y = (self.block_2_TAB2_title_pos_y+
                                self.block_title_entry_gap_y+
                                self.text_entry_gap)
    self.block_2_TAB2_combo_entry_gap_x = 0.21
    self.block_2_TAB2_entry_entry_gap_x = 0.04
    self.block_2_TAB2_entry_1_2_x = self.block_2_TAB2_entry_1_1_x + self.block_2_TAB2_combo_entry_gap_x
    self.block_2_TAB2_entry_1_3_x = self.block_2_TAB2_entry_1_2_x + self.block_2_TAB2_entry_entry_gap_x      
         
    self.button_add_reform_x = self.block_2_TAB2_entry_1_3_x + self.block_2_TAB2_entry_entry_gap_x + 0.03
    self.button_del_reform_x = self.block_2_TAB2_entry_1_3_x + self.block_2_TAB2_entry_entry_gap_x + 0.05
    self.button_clear_reform_x = self.block_2_TAB2_entry_1_3_x + self.block_2_TAB2_entry_entry_gap_x + 0.07
     
    self.root_title=Label(self.TAB2,text="Tax Microsimulation Model",
             font = self.fontStyle_title)
    self.root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")
    

    #self.growfactors_filename = "taxcalc/"+self.growfactors_filename
    #print(self.growfactors_filename)
    
    self.l1A=Label(self.TAB2, text="Current Law",
             font = self.fontStyle_sub_title)
    self.l1A.place(relx = self.block_1_TAB2_title_pos_x, rely = self.block_1_TAB2_title_pos_y, anchor = "w")
    #(...)
    #action_with_arg = partial(action, arg)
    #button = Tk.Button(master=frame, text='press', command=action_with_arg)
    self.button_generate_revenue_curr_law = ttk.Button(self.TAB2, text = "Generate Current Law Total Revenues", style='my.TButton', command=self.clicked_generate_revenues)
    self.button_generate_revenue_curr_law.place(relx = self.button_1_TAB2_pos_x, 
                                             rely = self.button_1_TAB2_pos_y, anchor = "w")
    
    self.l2A=Label(self.TAB2, text="Reform", font = self.fontStyle_sub_title)
    self.l2A.place(relx = self.block_1_title_pos_x, rely = self.block_2_TAB2_title_pos_y, anchor = "w")
    
    self.l3A=Label(self.TAB2, text="Select Policy Parameter: ", font = self.fontStyle)
    self.l3A.place(relx = self.block_2_TAB2_entry_1_1_x, 
             rely = self.block_2_TAB2_entry_1_1_y-self.text_entry_gap, anchor = "w")
    
    self.policy_options_list = self.policy_options()
    #self.policy_options_list.remove('gst_rate')
    self.block_widget_dict = {}
    #self.block_selected_dict = {}
    self.num_reforms = 0
    self.num_widgets = 1
   
    self.block_widget_dict[1] = {}
    #self.block_selected_dict[1] = {}
    self.block_widget_dict[1][1] = ttk.Combobox(self.TAB2, value=self.policy_options_list, 
                                                font=self.text_font, name=str(self.num_widgets))
    #self.block_widget_dict[1][1].current(0)
    self.block_widget_dict[1][1].place(relx = self.block_2_TAB2_entry_1_1_x, 
                    rely = self.block_2_TAB2_entry_1_1_y, anchor = "w", width=250)
    
    self.block_widget_dict[1][1].bind("<<ComboboxSelected>>", self.show_policy_selection)
    
    self.l4=Label(self.TAB2,text="Year: ", font = self.fontStyle)
    self.l4.place(relx = self.block_2_TAB2_entry_1_2_x, 
             rely = self.block_2_TAB2_entry_1_1_y-self.text_entry_gap, anchor = "w")
    self.block_widget_dict[1][2] = Entry(self.TAB2, width=6, font = self.fontStyle)
    self.block_widget_dict[1][2].place(relx = self.block_2_TAB2_entry_1_2_x, rely = self.block_2_TAB2_entry_1_1_y, anchor = "w")
    
    self.l5=Label(self.TAB2,text="Value: ", font = self.fontStyle)
    self.l5.place(relx = self.block_2_TAB2_entry_1_3_x, 
             rely = self.block_2_TAB2_entry_1_1_y-self.text_entry_gap, anchor = "w")
    self.block_widget_dict[1][3] = Entry(self.TAB2, width=10, font = self.fontStyle)
    self.block_widget_dict[1][3].place(relx = self.block_2_TAB2_entry_1_3_x, rely = self.block_2_TAB2_entry_1_1_y, anchor = "w")

    '''Create a Button for creating a new reform line item '''
    
    #self.num_reforms += 1
    self.button_add_reform = ttk.Button(self.TAB2, text="+", style='my.TButton', command= lambda: self.create_policy_widgets(self.TAB2), width=2)
    self.button_add_reform.place(relx = self.button_add_reform_x, rely = self.block_2_TAB2_entry_1_1_y, anchor = "w")        

    '''Create a Button for deleting a reform line item '''

    self.button_delete_reform = ttk.Button(self.TAB2, text="-", style='my.TButton', command=self.delete_policy_widgets, width=2)
    self.button_delete_reform.place(relx = self.button_del_reform_x, rely = self.block_2_TAB2_entry_1_1_y, anchor = "w") 

    '''Create a Button to Reset policy reform selection'''

    self.button_clear_reform = ttk.Button(self.TAB2, text="Reset", style='my.TButton', command=self.reset_policy_widgets, width=6)
    self.button_clear_reform.place(relx = self.button_clear_reform_x, rely = self.block_2_TAB2_entry_1_1_y, anchor = "w")
        
    self.button_generate_revenue_policy = ttk.Button(self.TAB2, text = "Generate Revenue under Reform",
                                                     style='my.TButton', command=self.clicked_generate_policy_revenues)
    self.button_2_TAB2_pos_x = self.button_1_pos_x
    self.button_2_TAB2_pos_y = (self.block_2_TAB2_entry_1_1_y+(self.num_widgets+1)*(self.entry_entry_gap_y)) +self.entry_button_gap
    self.button_generate_revenue_policy.place(relx = self.button_2_TAB2_pos_x,
                                                rely = self.button_2_TAB2_pos_y, anchor = "w")       
    
 
    #self.image1 = Image.open("egypt_flag.jpg")
    self.image1 = Image.open("Macedonia_Flag.jpg")
    self.image2 = self.image1.resize((700, 400), Image.ANTIALIAS)
    self.image = ImageTk.PhotoImage(self.image2)
    # "world_bank.png"
    #self.image1 = ImageTk.PhotoImage(Image.open("egypt_flag.jpg"))

    #image = tk.PhotoImage(file="blank.png")
    self.pic = tk.Label(self.TAB2,image=self.image)
    self.pic.place(relx = 0.50, rely = 0.10, anchor = "nw")
    self.pic.image = self.image
     
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

from gui_tab1 import grid_placement
from guifuncs import save_inputs, get_inputs
#from taxcalc import *

from PIL import Image,ImageTk

class super_combo(tk.Frame):
    def __init__(self, tab, input_json, field_year, field_value, position_x, 
                 position_y, attribute_value=None, 
                 selected_attribute_widget=None,
                 editable_field_year=None, elasticity=None, num_combos=None):

        if elasticity is not None:
            self.elasticity=1
        else:
            self.elasticity=0
        #self.block_1_title_pos_x = 0.15
        self.input_json_main = input_json
        self.editable_field_year = editable_field_year
        #self.attribute_name = attribute_name
        # The self.attribute_value input parameter is only used for growfactors
        # where we would like to filter the entries
        self.attribute_value = attribute_value
        if self.attribute_value is not None:
            self.input_json=self.input_json_main[self.attribute_value]
            self.selected_attribute_widget = selected_attribute_widget
        else:
            self.input_json = self.input_json_main
        #print('self.input_json ', self.input_json)
        self.field_year=field_year
        self.field_value=field_value
        self.width_json = 0
        if num_combos is not None:
            self.width_json = num_combos
        else:
            if len(self.input_json)>0:
                self.width_json = len(self.input_json[list(self.input_json.keys())[0]][field_year])                       
        grid_placement(self, 0.15)       
        self.pos_x = position_x
        self.pos_y = position_y
        shift_x = 0
        shift_y = 0
        self.widget_placement(shift_x, shift_y, self.width_json)
        self.fontStyle = tkfont.Font(family="Calibri", size="12")
        self.fontStyle_sub_title = tkfont.Font(family="Calibri", size="14", weight="bold")         
        self.fontStyle_title = tkfont.Font(family="Calibri", size="18", weight="bold")
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        self.text_font = ('Calibri', '12')
        self.block_widget_dict = {}
        return
    
    def widget_placement(self, shift_x, shift_y, width):
        self.combo_label_x = self.pos_x + shift_x
        self.combo_label_y = self.pos_y + shift_y
        self.label_combo_gap_y = 0.03
        self.combo_x = self.pos_x
        self.combo_y = self.combo_label_y + self.label_combo_gap_y
        self.combo_width_x = 0.15
        self.combo_entry_gap_x = 0.02
        self.combo_label_gap_x = 0.02
        self.entry_entry_gap_x = 0.02
        self.entry_1_width_x = 0.03
        self.entry_2_width_x = 0.04
        self.entry_entry_gap_y = 0.03
        self.combo_combo_gap_y = 0.03
        self.combo_button_gap_y = 0.06
        self.label_width_x = 0.02
        if self.attribute_value is not None:
            self.combo_label_gap_x = 0.12

        if width == 1:
            self.entry_1_label_x = self.combo_x + self.combo_width_x + self.combo_entry_gap_x
            self.entry_1_label_y = self.combo_label_y
            self.entry_1_x = self.entry_1_label_x
            self.entry_1_y = self.combo_y            
            self.entry_2_label_x = self.entry_1_label_x + self.entry_1_width_x + self.entry_entry_gap_x            
            self.entry_2_label_y = self.entry_1_label_y
            self.entry_2_x = self.entry_2_label_x
            self.entry_2_y = self.entry_1_y        
            self.plus_button_x = self.entry_2_x + self.entry_2_width_x + self.entry_entry_gap_x
            self.plus_button_y = self.entry_1_y
            self.minus_button_x = self.plus_button_x + self.entry_entry_gap_x
            self.minus_button_y = self.entry_1_y
            self.reset_button_x = self.minus_button_x + self.entry_entry_gap_x
            self.reset_button_y = self.entry_1_y
            self.generate_revenue_policy_button_x = self.combo_x
            self.generate_revenue_policy_button_y = self.combo_y + self.combo_button_gap_y            
        else:
            self.entry_1_label_x = self.combo_x + self.combo_width_x + self.combo_label_gap_x
            self.entry_1_label_y = self.combo_y
            self.entry_1_x = self.entry_1_label_x + self.label_width_x
            self.entry_1_y = self.combo_y          
            self.entry_2_label_x = self.entry_1_label_x
            self.entry_2_label_y = self.entry_1_label_y + self.combo_combo_gap_y
            self.entry_2_x = self.entry_1_x
            self.entry_2_y = self.entry_1_y + self.combo_combo_gap_y          
            self.plus_button_x = self.entry_1_x + width*(max(self.entry_1_width_x,self.entry_2_width_x) + self.entry_entry_gap_x)
            self.plus_button_y = self.entry_1_y
            self.minus_button_x = self.plus_button_x + self.entry_entry_gap_x
            self.minus_button_y = self.entry_1_y
            self.reset_button_x = self.minus_button_x + self.entry_entry_gap_x
            self.reset_button_y = self.entry_1_y            
            self.generate_revenue_policy_button_x = self.combo_x
            self.generate_revenue_policy_button_y = self.combo_y + self.combo_button_gap_y             
            self.attribute_entry_x = self.combo_x + self.combo_width_x+ self.combo_entry_gap_x
        return
    
    def create_block():
        self.block_1_title_x = self.pos_x
        self.block_1_title_y = self.pos_y
        
        self.block_2_title_x = self.pos_x
        self.block_2_title_y = self.pos_y

        self.l1A=tk.Label(tab, text="Current Law",
                 font = self.fontStyle_sub_title)
        self.l1A.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
        #print('Current Law relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y ', self.block_1_title_pos_x, self.block_1_title_pos_y)

        #(...)
        #action_with_arg = partial(action, arg)
        #button = Tk.Button(master=frame, text='press', command=action_with_arg)
        #self.button_generate_revenue_curr_law = ttk.Button(tab, text = "Generate Current Law Total Revenues", style='my.TButton', command=self.clicked_generate_revenues)
        #self.button_generate_revenue_curr_law.place(relx = self.button_1_TAB_pos_x, 
        #                                         rely = self.button_1_pos_y, anchor = "w")
        
        self.l2A=tk.Label(tab, text="Reform", font = self.fontStyle_sub_title)
        self.l2A.place(relx = self.block_1_title_pos_x, rely = self.block_2_title_pos_y, anchor = "w")
        #print('Reform relx = self.block_1_title_pos_x, rely = self.block_2_title_pos_y ', self.block_1_title_pos_x, self.block_2_title_pos_y)
 
        
    def create_new_row_policy_widgets(self, tab):
        #num is the counter for the widgets
        self.policy_options_list = self.policy_options(self.input_json)
        if (self.num_widgets==self.num_reforms):
            self.num_widgets += 1
            num = self.num_widgets
            self.block_widget_dict[num] = {}
            self.block_widget_dict[num][1] = ttk.Combobox(tab, value=self.policy_options_list, font=self.text_font, name=str(num))
            if (self.num_widgets==1):
                self.combo_new_y = self.combo_y + self.combo_combo_gap_y*(self.num_widgets-1)
            else:
                self.combo_new_y = self.combo_y + 2*self.combo_combo_gap_y*(self.num_widgets-1)
            self.block_widget_dict[num][1].place(relx = self.combo_x, 
                            rely = self.combo_new_y, anchor = "w", width=250)
            self.block_widget_dict[num][1].bind("<<ComboboxSelected>>", lambda event: self.show_policy_selection(event, self.block_widget_dict))

            self.block_widget_dict[num][2] = {}

            if (self.width_json==1):
                self.entry_1_new_x = self.entry_1_x
                self.entry_1_new_y = self.combo_new_y                
                self.block_widget_dict[num][2][0] = tk.Entry(tab, width=8, font = self.fontStyle)
                self.block_widget_dict[num][2][0].place(relx = self.entry_1_new_x, 
                                                          rely = self.entry_1_new_y, anchor = "w")                
            else:
                self.entry_1_new_y = self.combo_new_y
                self.l4[num]=tk.Label(tab,text=self.field_year.capitalize(), font = self.fontStyle)
                self.l4[num].place(relx = self.entry_1_label_x, 
                         rely = self.entry_1_new_y, anchor = "w")                
                for i in range(self.width_json):
                    self.block_widget_dict[num][2][i] = tk.Entry(tab, width=8, font = self.fontStyle)
                    self.entry_1_new_x = self.entry_1_x + i*max(self.entry_1_width_x,self.entry_2_width_x)+(i+1)*self.entry_entry_gap_x 
                    self.block_widget_dict[num][2][i].place(relx = self.entry_1_new_x, 
                                                          rely = self.entry_1_new_y, anchor = "w")

            self.block_widget_dict[num][3] = {}
            if (self.width_json==1):
               self.entry_2_new_x = self.entry_2_x
               self.entry_2_new_y = self.combo_new_y               
               self.block_widget_dict[num][3][0] = tk.Entry(tab, width=10, font = self.fontStyle)
               self.block_widget_dict[num][3][0].place(relx = self.entry_2_new_x, 
                                                            rely = self.entry_2_new_y, anchor = "w")
            else:
                self.entry_2_new_y = self.entry_2_y + 2*self.combo_combo_gap_y*(self.num_widgets-1)
                self.l5[num]=tk.Label(tab,text=self.field_value, font = self.fontStyle)
                self.l5[num].place(relx = self.entry_2_label_x, 
                         rely = self.entry_2_new_y, anchor = "w")
                for i in range(self.width_json):                  
                    self.block_widget_dict[num][3][i] = tk.Entry(tab, width=10, font = self.fontStyle)
                    self.entry_2_new_x = self.entry_2_x + i*max(self.entry_1_width_x,self.entry_2_width_x)+(i+1)*self.entry_entry_gap_x
                    self.block_widget_dict[num][3][i].place(relx = self.entry_2_new_x, 
                                                            rely = self.entry_2_new_y, anchor = "w")

            if self.attribute_value is not None:
                self.block_widget_dict[num][4] = {}
                self.block_widget_dict[num][4] = tk.Entry(tab, width=15, font = self.fontStyle)        
                self.block_widget_dict[num][4].place(relx = self.attribute_entry_x, rely = self.combo_new_y, anchor = "w")               
 
            #self.num_reforms += 1
            if (self.width_json==1):
                self.generate_revenue_policy_button_new_y = self.combo_y + 2*self.combo_combo_gap_y*(self.num_widgets-1) + self.combo_button_gap_y
                #print('button pos new ',  self.generate_revenue_policy_button_new_y)
            else:
                self.generate_revenue_policy_button_new_y = self.combo_y + 2*self.combo_combo_gap_y*(self.num_widgets-1) + self.combo_button_gap_y
            self.button_generate_revenue_policy.place(relx = self.generate_revenue_policy_button_x,
                                                    rely = self.generate_revenue_policy_button_new_y, anchor = "w")

    def reset_policy_widgets(self):
        self.num_widgets = len(self.block_widget_dict)
        num = self.num_widgets
        #print('self.num_widgets in reset widgets', self.num_widgets)
        for num in range(2, self.num_widgets+1):
            self.block_widget_dict[num][1].destroy()
            if self.attribute_value is not None:
                self.block_widget_dict[num][4].destroy()
            if (self.width_json>1):
                self.l4[num].destroy()
                self.l5[num].destroy()
            for i in range(self.width_json):
                self.block_widget_dict[num][2][i].destroy()
                self.block_widget_dict[num][3][i].destroy()
            self.block_widget_dict.pop(num, None)
        self.num_reforms = 0
        self.num_widgets = 1
        self.block_widget_dict[1][1].delete(0, tk.END)
        if self.attribute_value is not None:
            self.block_widget_dict[1][4].delete(0, tk.END)
        for i in range(self.width_json):
            self.block_widget_dict[1][2][i].config(state=tk.NORMAL)
            self.block_widget_dict[1][2][i].delete(0, tk.END)
            self.block_widget_dict[1][3][i].delete(0, tk.END)
        #print('button at reset ',self.generate_revenue_policy_button_y)            
        self.button_generate_revenue_policy.place(relx = self.generate_revenue_policy_button_x, 
                                                  rely = self.generate_revenue_policy_button_y, anchor = "w")

    def destroy_all_widgets(self):
        self.num_widgets = len(self.block_widget_dict)
        num = self.num_widgets
        #print('self.num_widgets in reset widgets', self.num_widgets)
        for num in range(1, self.num_widgets+1):
            self.block_widget_dict[num][1].destroy()
            if self.attribute_value is not None:
                self.block_widget_dict[num][4].destroy()
            if (self.width_json>1):
                self.l4[num].destroy()
                self.l5[num].destroy()
            for i in range(self.width_json):
                self.block_widget_dict[num][2][i].destroy()
                self.block_widget_dict[num][3][i].destroy()
            self.block_widget_dict.pop(num, None)
        self.num_reforms = 0
        self.num_widgets = 0         
        self.button_generate_revenue_policy.destroy()
        self.button_add_reform.destroy()
        self.button_delete_reform.destroy()
        self.button_clear_reform.destroy()
        self.l3A.destroy()
                
    def delete_policy_widgets(self):
        self.num_widgets = len(self.block_widget_dict)
        num = self.num_widgets
        if num == 1:
            #showinfo("Warning", "cannot delete")
            self.block_widget_dict[1][1].delete(0, tk.END)
            for i in range(self.width_json):
                self.block_widget_dict[1][2][i].delete(0, tk.END)
                self.block_widget_dict[1][3][i].delete(0, tk.END)         
            #self.num_reforms += 1                   # increase num_reforms by 1 so that it doesnt reduce to zero in the next step when it is reduced by 1
        elif (num > 1):
            self.block_widget_dict[num][1].destroy()
            if self.attribute_value is not None:
                self.block_widget_dict[num][4].destroy()
            for i in range(self.width_json):            
                self.block_widget_dict[num][2][i].destroy()
                self.block_widget_dict[num][3][i].destroy()
            self.block_widget_dict.pop(num, None)
            self.num_widgets -= 1
            if (self.num_reforms > 0):
                self.num_reforms -= 1
            if (self.width_json==1):
                self.generate_revenue_policy_button_new_y = self.combo_y + 2*self.combo_combo_gap_y*(self.num_widgets-1) + self.combo_button_gap_y
                #print('button at 1 del ',self.generate_revenue_policy_button_new_y)
            else:
                self.l4[num].destroy()
                self.l5[num].destroy()  
                self.generate_revenue_policy_button_new_y = self.combo_y + 2*self.combo_combo_gap_y*(self.num_widgets-1) + self.combo_button_gap_y
                #print('button at >1 del ',self.generate_revenue_policy_button_new_y)
            self.button_generate_revenue_policy.place(relx = self.generate_revenue_policy_button_x, rely = self.generate_revenue_policy_button_new_y, anchor = "w")
        #print('block_widget_dict after ', self.block_widget_dict)
        #print('self.num_widgets after ',self.num_widgets)
        
    def policy_options(self, input_json):
        self.input_json_main = input_json
        #self.attribute_name = attribute_name
        # The self.attribute_value input parameter is only used for growfactors
        # where we would like to filter the entries
        if self.attribute_value is not None:
            self.input_json=self.input_json_main[self.attribute_value]
        else:
            self.input_json = self.input_json_main

        input_json_sorted = dict(sorted(self.input_json.items()))
        policy_options_list = []
        for k, s in input_json_sorted.items(): 
             #Don't show the current law rates and the elasticity items in the drop down list
            if self.elasticity:
                if (k[1:11] == 'elasticity'):
                    policy_options_list = policy_options_list + [k[1:]]
            elif (k[-8:] != 'curr_law') and (k[1:11] != 'elasticity'):
                policy_options_list = policy_options_list + [k[1:]]
        #print('policy_options_list ', policy_options_list)
        return (policy_options_list)
    
    def policy_reform():
        self.reform={}
        self.reform['policy']={}
        self.reform['policy']['_'+self.selected_item]={}
        self.updated_year = self.block_widget_dict[1][2].get()
        self.updated_value = self.block_widget_dict[1][3].get()
        self.reform['policy']['_'+selected_item][self.updated_year]=[self.updated_value]
        #print("Reform2: ", self.reform)
        
    def show_policy_selection(self, event, widget_dict):   
        global_vars = get_inputs(self)     
        #print("inside policy selection")
        active_widget_number = int(str(event.widget)[-1])
        # update the number of reforms only if we change the entries
        # beyond self.num_reforms
        num = len(widget_dict)
        if num > self.num_reforms:
            self.num_reforms += 1

        if self.attribute_value is not None:
            self.attribute_value = self.selected_attribute_widget.get()
            self.input_json=self.input_json_main[self.attribute_value]      
        selected_item = widget_dict[num][1].get()
        #print('vars ',vars)
        selected_param = {}
        selected_value = {}
        #print('input_json ', self.input_json)
        #print('self.input_json selected item \n', self.input_json['_'+ selected_item])
        start_year = int(global_vars['start_year'])
        end_year = int(global_vars['end_year'])
        k=0
        for j in range(len(self.input_json['_'+ selected_item][self.field_year])):
            param = int(self.input_json['_'+ selected_item][self.field_year][j])
            if int(param)==start_year:
                k=j
                break
        # growfactors may have many years but we only need those from start 
        # year to end year
        # k is the counter for the widgets i.e. start year to end year for growfactors
        # width is three for elasticity with three thresholds       
        i=0 
        for j in range(k, k+self.width_json):
            if (self.width_json==1):
                param = int(self.input_json['_'+ selected_item][self.field_year][-1])                
                value = self.input_json['_'+ selected_item][self.field_value][-1]
            else:
                param = int(self.input_json['_'+ selected_item][self.field_year][j])                
                value = self.input_json['_'+ selected_item][self.field_value][j]            
            #print('param ', param)
            #print('value ', value)
            if (self.width_json==1) and not self.elasticity:
                if (param < start_year):
                    param = start_year
            # start year and end year condition does not apply for elasticity
            if self.elasticity or ((param >= start_year) and (param <= end_year)):        
                selected_param[i] = param
                selected_value[i] = value
                if selected_param[i]>=1e99:
                    formatted_param = '{:.0e}'.format(selected_param[i])
                else:
                    formatted_param = selected_param[i]                
                widget_dict[num][2][i].config(state=tk.NORMAL)               
                widget_dict[num][2][i].delete(0, tk.END)
                widget_dict[num][2][i].insert(tk.END, formatted_param)
                if selected_value[i]>=1e99:
                    formatted_value = '{:.0e}'.format(selected_value[i])
                else:
                    formatted_value = selected_value[i]                
                if (not self.editable_field_year):
                    widget_dict[num][2][i].config(state=tk.DISABLED)             
                widget_dict[num][3][i].delete(0, tk.END)
                widget_dict[num][3][i].insert(tk.END, formatted_value)
                i=i+1

        if self.attribute_value is not None:
            widget_dict[num][4].delete(0, tk.END)
            widget_dict[num][4].insert(tk.END, self.attribute_value)     
        return widget_dict

    def display_widgets(self, tab):

        global_vars = get_inputs(self)

        self.root_title=tk.Label(tab,text="Tax Microsimulation Model",
                 font = self.fontStyle_title)
        self.root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")
        #print('Main Title relx = self.title_pos_x, rely = self.title_pos_y ', self.title_pos_x, self.title_pos_y)
       
        self.l3A=tk.Label(tab, text="Select Policy Parameter: ", font = self.fontStyle)
        self.l3A.place(relx = self.combo_label_x, 
                 rely = self.combo_label_y, anchor = "w")

        self.num_reforms = 0
        self.num_widgets = 1
       
        self.block_widget_dict[1] = {}
        #self.block_selected_dict[1] = {}
        self.selected_combo_value = tk.StringVar()                
        self.block_widget_dict[1][1] = ttk.Combobox(tab, textvariable=self.selected_combo_value, font=self.text_font, name=str(self.num_widgets))
        #self.block_widget_dict[1][1] = ttk.Combobox(tab, value=self.policy_options_list, font=self.text_font, name=str(self.num_widgets))

        #self.block_widget_dict[1][1].current(0)
        self.block_widget_dict[1][1].place(relx = self.combo_x, 
                        rely = self.combo_y, anchor = "w", width=250)
        #print('Combobox relx = ', self.combo_x, self.combo_y)
        
        #print('self.input_json ', self.input_json)
        self.block_widget_dict[1][1].bind("<<ComboboxSelected>>", lambda event: self.show_policy_selection(event, self.block_widget_dict))
        #self.block_widget_dict[1][1].bind("<<ComboboxSelected>>", lambda event: print(" baba"))
        
        # Year and Value widgets will be according to the length of the col_label
        # if col_label length is one or less then the first entry label will be the 
        # row_var and its value will be the row_label
        # if col_label length is more than 1 then there will be as many entry 
        # boxes as the length of the col_label and its value 
        # will be the col_labels
        self.l4 = {}
        if self.elasticity:
            self.l4[1]=tk.Label(tab,text=self.field_year.capitalize(), font = self.fontStyle)
        else:
            self.l4[1]=tk.Label(tab,text="Year: ", font = self.fontStyle)
        
        self.l4[1].place(relx = self.entry_1_label_x, 
                 rely = self.entry_1_label_y, anchor = "w")
        #print('Year: ', round(self.entry_1_label_x,2), self.entry_1_label_y)
        self.block_widget_dict[1][2] = {}

        start_year = int(global_vars['start_year'])
        end_year = int(global_vars['end_year'])
        year = start_year
        for i in range(self.width_json):
            if (year <= end_year):
                self.block_widget_dict[1][2][i] = tk.Entry(tab, width=8, font = self.fontStyle)
                if (self.width_json==1):
                    self.block_widget_dict[1][2][i].place(relx = self.entry_1_x, 
                                                          rely = self.entry_1_y, anchor = "w")
                else:
                    self.block_widget_dict[1][2][i].place(relx = self.entry_1_x + i*max(self.entry_1_width_x,self.entry_2_width_x)+(i+1)*self.entry_entry_gap_x, 
                                                          rely = self.entry_1_y, anchor = "w")
            year = year+1
            
        i=0
        #print('Year Entry: ', round(self.entry_1_x + i*max(self.entry_1_width_x,self.entry_2_width_x)+(i+1)*self.entry_entry_gap_x,2), self.entry_1_y)
        self.l5 = {}
        self.l5[1]=tk.Label(tab, text="Value: ", font = self.fontStyle)
        self.l5[1].place(relx = self.entry_2_label_x, 
                 rely = self.entry_2_label_y, anchor = "w")
        #print('Value: ', round(self.entry_2_label_x,2), self.entry_2_label_y)
        self.block_widget_dict[1][3] = {}
        year = start_year        
        for i in range(self.width_json):
            if (year <= end_year):            
                self.block_widget_dict[1][3][i] = tk.Entry(tab, width=10, font = self.fontStyle)
                if (self.width_json==1):          
                    self.block_widget_dict[1][3][i].place(relx = self.entry_2_x, rely = self.entry_2_y, anchor = "w")               
                else:
                    self.block_widget_dict[1][3][i].place(relx = self.entry_2_x + i*max(self.entry_1_width_x,self.entry_2_width_x)+(i+1)*self.entry_entry_gap_x, rely = self.entry_2_y, anchor = "w")               
            year = year+1
        
        if self.attribute_value is not None:
            self.block_widget_dict[1][4] = tk.Entry(tab, width=15, font = self.fontStyle)        
            self.block_widget_dict[1][4].place(relx = self.attribute_entry_x, rely = self.combo_y, anchor = "w")               
                
        i=0
        #print('Value Entry: ', round(self.entry_2_x + i*max(self.entry_1_width_x,self.entry_2_width_x)+(i+1)*self.entry_entry_gap_x,2), self.entry_1_y)
                
        '''Create a Button for creating a new reform line item '''     
        #self.num_reforms += 1
        self.button_add_reform = ttk.Button(tab, text="+", style='my.TButton', command= lambda: self.create_new_row_policy_widgets(tab), width=2)
        self.button_add_reform.place(relx = self.plus_button_x, rely = self.plus_button_y, anchor = "w")        
    
        '''Create a Button for deleting a reform line item '''
    
        self.button_delete_reform = ttk.Button(tab, text="-", style='my.TButton', command=self.delete_policy_widgets, width=2)
        self.button_delete_reform.place(relx = self.minus_button_x, rely = self.minus_button_y, anchor = "w") 
    
        '''Create a Button to Reset policy reform selection'''
    
        self.button_clear_reform = ttk.Button(tab, text="Reset", style='my.TButton', command=self.reset_policy_widgets, width=6)
        self.button_clear_reform.place(relx = self.reset_button_x, rely = self.reset_button_y, anchor = "w")
            
        self.button_generate_revenue_policy = ttk.Button(tab, text = "Generate Revenue under Reform", style='my.TButton')
        #self.button_generate_revenue_policy = ttk.Button(tab, text = "Generate Revenue under Reform", style='my.TButton', command=self.clicked_generate_policy_revenues)
        self.button_generate_revenue_policy.place(relx = self.generate_revenue_policy_button_x,
                                                    rely = self.generate_revenue_policy_button_y, anchor = "w")       
        
        self.image1 = Image.open("world_bank.png")
        self.image2 = self.image1.resize((700, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image2)
        # "world_bank.png"
        #self.image1 = ImageTk.PhotoImage(Image.open("egypt_flag.jpg"))
    
        #image = tk.PhotoImage(file="blank.png")
        self.pic = tk.Label(tab,image=self.image)
        self.pic.place(relx = 0.50, rely = 0.30, anchor = "nw")
        self.pic.image = self.image
        return (self.button_generate_revenue_policy, self.block_widget_dict)
         
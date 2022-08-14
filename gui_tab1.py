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

def initialize_vars(self):
    self.number = 0
    self.widgets = []
    self.completed_TAB1 = 0
    #self.grid()
    #self.createWidgets()

    self.reform={}
    self.selected_item = ""
    self.selected_value = ""
    self.selected_year = 2018
    self.sub_directory = "taxcalc"
    self.year_list = [2022, 2023, 2024, 2025, 2026, 2027]
    # Include a check whether the years are valid by looking at the 
    # selected growfactors file
    """    
    self.data_filename = "pit.csv"
    self.weights_filename = "pit_weights1.csv"
    self.records_variables_filename = "records_variables.json"
    self.cit_data_filename = "cit_cross.csv"
    self.cit_weights_filename = "cit_cross_wgts1.csv"
    self.cit_records_variables_filename = "corprecords_variables.json"
    self.gst_data_filename = "gst.csv"
    self.gst_weights_filename = "gst_weights.csv"
    self.gst_records_variables_filename = "gstrecords_variables.json"         
    self.policy_filename = "current_law_policy_cmie.json"
    self.growfactors_filename = "growfactors1.csv"             
    self.benchmark_filename = "tax_incentives_benchmark.json"
    self.elasticity_filename = "elasticity.json"
    self.pit_functions_filename = "functions.py"
    self.pit_function_names = "function_names.json"
    self.start_year = 2019
    self.end_year=2023
    self.SALARY_VARIABLE = "SALARY"
    """
    
    #if tax_type == 'pit':
    #self.vars['start_year'] = 2018
    #elif tax_type == 'cit':
    # self.vars['DEFAULTS_FILENAME'] = "current_law_policy_cit_egypt.json"    
    # self.vars['GROWFACTORS_FILENAME'] = "growfactors_egypt4.csv"
    # self.vars['start_year'] = 2020
   
    ##### NOTE 'Year' is a key word for year in records variable
   
    self.vars['pit_data_filename'] = "pit_macedonia_new.csv"
    self.vars['pit_weights_filename'] = "pit_weights_macedonia_new.csv"
    self.vars['pit_records_variables_filename'] = "records_variables_pit_macedonia_new.json"
    self.vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_macedonia_new.json"
    self.vars['pit_elasticity_filename'] = "elasticity_pit_macedonia_new.json"
    self.vars['pit_functions_filename'] = "functions_pit_macedonia_new.py"
    self.vars['pit_function_names_filename'] = "function_names_pit_macedonia_new.json"       
    self.vars['pit_distribution_json_filename'] = 'pit_distribution_macedonia.json'
    self.vars['gdp_filename'] = 'gdp_nominal_macedonia.csv'

    # self.vars['pit_data_filename'] = "pit_data_training.csv"
    # self.vars['pit_weights_filename'] = "pit_weights_training.csv"
    # self.vars['pit_records_variables_filename'] = "records_variables_pit_training.json"
    # self.vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_training.json"
    # self.vars['pit_elasticity_filename'] = "elasticity_pit_training.json"
    # self.vars['pit_functions_filename'] = "functions_pit_training.py"
    # self.vars['pit_function_names_filename'] = "function_names_pit_training.json"
    # self.vars['pit_distribution_json_filename'] = 'pit_distribution_macedonia.json'  
    

    # self.vars['DEFAULTS_FILENAME'] = "current_law_policy_pit_srilanka.json"
    # self.vars['GROWFACTORS_FILENAME'] = "growfactors_pit_srilanka.csv" 
    # self.vars['pit_data_filename'] = "pit_srilanka.csv"
    # self.vars['pit_weights_filename'] = "pit_weights_srilanka.csv"
    # self.vars['pit_records_variables_filename'] = "records_variables_pit_srilanka.json"
    # self.vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_srilanka.json"
    # self.vars['pit_elasticity_filename'] = "elasticity_pit_srilanka.json"
    # self.vars['pit_functions_filename'] = "functions_pit_srilanka.py"
    # self.vars['pit_function_names_filename'] = "function_names_pit_srilanka.json"
    # self.vars['pit_distribution_json_filename'] = 'pit_distribution_srilanka.json'
    # self.vars['gdp_filename'] = 'gdp_nominal_srilanka.csv'

    """
    self.vars['cit_data_filename'] = "cit_egypt.csv"
    self.vars['cit_weights_filename'] = "cit_weights_egypt.csv"
    self.vars['cit_records_variables_filename'] = "records_variables_cit_egypt.json"    
    self.vars['cit_benchmark_filename'] = "cit_tax_incentives_benchmark_egypt.json"
    self.vars['cit_elasticity_filename'] = "elasticity_cit_egypt.json"
    self.vars['cit_functions_filename'] = "functions_cit_egypt.py"
    self.vars['cit_function_names_filename'] = "function_names_cit_egypt.json"
    self.vars['gdp_filename'] = 'gdp_nominal_egypt.csv'    
    """
    self.vars['DEFAULTS_FILENAME'] = "current_law_policy_cit_training.json"    
    self.vars['GROWFACTORS_FILENAME'] = "growfactors_cit_training.csv"
    self.vars['cit_data_filename'] = "cit_data_training.csv"
    self.vars['cit_weights_filename'] = "cit_weights_training.csv"
    self.vars['cit_records_variables_filename'] = "records_variables_cit_training.json"    
    self.vars['cit_benchmark_filename'] = "tax_incentives_benchmark_cit.json"
    self.vars['cit_elasticity_filename'] = "elasticity_cit_training.json"
    self.vars['cit_functions_filename'] = "functions_cit_training.py"
    self.vars['cit_function_names_filename'] = "function_names_cit_training.json"
    self.vars['cit_distribution_json_filename'] = 'cit_distribution_egypt.json'
    
    self.vars['cit_max_lag_years'] = 10

    self.vars['vat_data_filename'] = "vat.csv"
    self.vars['vat_weights_filename'] = "vat_weights.csv"
    self.vars['vat_records_variables_filename'] = "vat_records_variables.json"   
    self.vars['vat_benchmark_filename'] = "vat_tax_incentives_benchmark.json"
    self.vars['vat_elasticity_filename'] = "vat_elasticity_macedonia.json"
    self.vars['vat_functions_filename'] = "vat_functions.py"
    self.vars['vat_function_names_filename'] = "vat_function_names.json"
    self.vars['vat_distribution_json_filename'] = 'vat_distribution.json'
    
    self.vars['pit_display_distribution_table_byincome'] = 0
    self.vars['pit_display_distribution_table_bydecile'] = 0
    self.vars['pit_display_revenue_table'] = 1
    
    self.vars['cit_display_distribution_table_byincome'] = 0
    self.vars['cit_display_distribution_table_bydecile'] = 0
    self.vars['cit_display_revenue_table'] = 1
    
    self.vars['vat_display_distribution_table_byincome'] = 0
    self.vars['vat_display_distribution_table_bydecile'] = 0
    self.vars['vat_display_revenue_table'] = 1
    

    
    self.vars['kakwani_list'] = []
    
    self.vars['start_year'] = 2022
    self.vars['end_year']=2027
    self.vars['data_start_year'] = 2018

    df= pd.read_csv(self.vars['gdp_filename'])
    df = df.set_index('Year')
    GDP_dict = df.to_dict()
    GDP_Nominal = {}
    for k,v in GDP_dict.items():
        for k1,v1 in v.items():
            GDP_Nominal[k1] = float(v1)
    
    self.vars['GDP_Nominal'] = GDP_Nominal
    self.vars['percent_gdp'] = 1
    #self.total_revenue_text1 = ""
    #self.reform_revenue_text1 = ""
    #self.reform_filename = "app01_reform.json"
    
    #self.vars['SALARY_VARIABLE'] = "gross_i_w"
    self.vars['SALARY_VARIABLE'] = "SALARY"

    self.vars['vat_id_var'] = 'id_n'
    
    self.vars['charts_ready'] = 0
    self.vars['chart_list'] = []
    #self.chart_list = []

    #initializing the display widgets    
    self.l1 = {}
    self.l2 = {}
    self.l3 = {}
    self.l31 = {}
    self.entry_data_filename = {}
    self.button_data_filename = {}
    self.entry_weights_filename = {}
    self.button_weights_filename = {}
    self.entry_records_filename = {}
    self.button_records_filename = {}
    self.entry_policy_filename = {}
    self.button_policy_filename = {}
    self.entry_growfactors_filename = {}
    self.button_growfactors_filename = {}
    self.entry_functions_filename = {}
    self.button_functions_filename = {}
    self.entry_functions_names_filename = {}
    self.button_function_names_filename = {}
    self.entry_benchmark_filename = {}
    self.button_benchmark_filename = {}    
    self.entry_gdp_filename = {}    
    self.button_gdp_filename = {}
    self.entry_salary_variable = {}
    self.entry_start_year = {}
    self.entry_end_year = {}    
               
    self.vars['show_error_log'] = 0
    self.vars['verbose'] = 0
    pass

def grid_placement(self, block_1_title_pos_x, block_1_title_pos_y=None):
    self.title_pos_x = 0.5
    self.title_pos_y = 0.0
    self.sub_title_pos_x = 0.5
    self.sub_title_pos_y = 0.05    
    self.block_1_title_pos_x = block_1_title_pos_x
    if block_1_title_pos_y is None:
        self.block_1_title_pos_y = 0.20
    else:
        self.block_1_title_pos_y = block_1_title_pos_y
    self.block_title_entry_gap_y = 0.05
    self.block_entry_entry_gap_y = 0.05
    self.block_1_entry_x = self.block_1_title_pos_x + 0.05
    self.entry_entry_gap_y = 0.03
    self.block_1_entry_1_y = (self.block_1_title_pos_y+self.block_title_entry_gap_y)
    self.block_1_entry_2_y = (self.block_1_entry_1_y+self.block_entry_entry_gap_y)
    self.block_1_entry_3_y = (self.block_1_entry_2_y+self.block_entry_entry_gap_y)
    self.block_1_entry_4_y = (self.block_1_entry_3_y+self.block_entry_entry_gap_y)
    self.block_1_entry_5_y = (self.block_1_entry_4_y+self.block_entry_entry_gap_y)
    self.block_1_entry_6_y = (self.block_1_entry_5_y+self.block_entry_entry_gap_y)
    self.block_1_entry_7_y = (self.block_1_entry_6_y+self.block_entry_entry_gap_y)
    self.block_1_entry_8_y = (self.block_1_entry_7_y+self.block_entry_entry_gap_y)
    self.block_1_entry_9_y = (self.block_1_entry_8_y+self.block_entry_entry_gap_y)
    self.block_1_entry_10_y = (self.block_1_entry_9_y+self.block_entry_entry_gap_y)
    self.block_1_entry_11_y = (self.block_1_entry_10_y+self.block_entry_entry_gap_y)     
    self.entry_button_gap = 0.02
    #self.vars={}
        
def display_entry(self, widget, tax_type):
    #self.initialize_vars(tax_type)
    self.vars[tax_type] = int(widget.get())
    #self.block_settings_pos_x = self.allocate_pos_x(self.pos_x, self.status,
                                                    #self.block_settings_pos_x)
    
    block_1_title_pos_x = self.block_settings_pos_x[tax_type] 
    if not self.vars[tax_type]:
        self.l1[tax_type].destroy()
        self.entry_data_filename[tax_type].destroy()
        self.button_data_filename[tax_type].destroy()
        self.entry_weights_filename[tax_type].destroy()
        self.button_weights_filename[tax_type].destroy()
        self.entry_records_filename[tax_type].destroy()
        self.button_records_filename[tax_type].destroy()
        self.entry_policy_filename[tax_type].destroy()
        self.button_policy_filename[tax_type].destroy()
        self. entry_growfactors_filename[tax_type].destroy()
        self.button_growfactors_filename[tax_type].destroy()
        self.entry_functions_filename[tax_type].destroy()
        self.button_functions_filename[tax_type].destroy() 
        self.entry_functions_names_filename[tax_type].destroy() 
        self.button_function_names_filename[tax_type].destroy()
        self.entry_benchmark_filename[tax_type].destroy()
        self.button_benchmark_filename[tax_type].destroy()      
        self.l2[tax_type].destroy() 
        self.entry_salary_variable[tax_type].destroy() 
        self.l3[tax_type].destroy() 
        self.entry_start_year[tax_type].destroy() 
        self.l31[tax_type].destroy() 
        self.entry_end_year[tax_type].destroy()
    else:
        if tax_type == 'pit':
            self.vars['DEFAULTS_FILENAME'] = "current_law_policy_pit_macedonia_new.json"
            self.vars['GROWFACTORS_FILENAME'] = "growfactors_pit_macedonia_new.csv"
            self.vars['start_year'] = 2022
            self.vars['data_start_year'] = 2018
            self.vars['SALARY_VARIABLE'] = "gross_i_w"
            self.vars['pit_id_var'] = 'id_n'
           
        elif tax_type == 'cit':
            #self.vars['DEFAULTS_FILENAME'] = "current_law_policy_cit_egypt.json"    
            #self.vars['GROWFACTORS_FILENAME'] = "growfactors_egypt.csv"
            self.vars['DEFAULTS_FILENAME'] = "current_law_policy_cit_training.json"    
            self.vars['GROWFACTORS_FILENAME'] = "growfactors_cit_training.csv"
            self.vars['start_year'] = 2020
            self.vars['data_start_year'] = 2020           
            self.vars['SALARY_VARIABLE'] = "SALARY"
            self.vars['cit_id_var'] = 'id_n'
        
        self.grid_placement(block_1_title_pos_x)
        self.l1[tax_type]=Label(self.TAB1,text="Data Inputs "+ tax_type.upper(),
                 font = self.fontStyle_sub_title)
        self.l1[tax_type].place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
        
        self.entry_data_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_data_filename[tax_type].place(relx = self.block_1_entry_x, 
                                  rely = self.block_1_entry_1_y,
                                  anchor = "e")
        self.entry_data_filename[tax_type].insert(END, self.vars[tax_type+'_data_filename'])
        self.button_data_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Data File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_data_filename[tax_type], tax_type+'_'+'data_filename'))
        self.button_data_filename[tax_type].place(relx = self.block_1_entry_x,
                                   rely = self.block_1_entry_1_y, anchor = "w")
        #button.place(x=140,y=50)
        
        self.entry_weights_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_weights_filename[tax_type].place(relx = self.block_1_entry_x,
                                     rely = self.block_1_entry_2_y, anchor = "e")
        self.entry_weights_filename[tax_type].insert(END, self.vars[tax_type+'_weights_filename'])
        self.button_weights_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Weights File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_weights_filename[tax_type], tax_type+'_'+'weights_filename'))
        self.button_weights_filename[tax_type].place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_2_y, anchor = "w")
    
        self.entry_records_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_records_filename[tax_type].place(relx = self.block_1_entry_x,
                                     rely = self.block_1_entry_3_y, anchor = "e")
        self.entry_records_filename[tax_type].insert(END, self.vars[tax_type+'_records_variables_filename'])
        
        self.button_records_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Records JSON File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_records_filename[tax_type], tax_type+'_'+'records_variables_filename'))
        self.button_records_filename[tax_type].place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_3_y, anchor = "w")
        
        self.entry_policy_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_policy_filename[tax_type].place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_4_y, anchor = "e")
        self.entry_policy_filename[tax_type].insert(END, self.vars['DEFAULTS_FILENAME'])
        self.button_policy_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Policy File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_policy_filename[tax_type], 'DEFAULTS_FILENAME', tax_type))
        self.button_policy_filename[tax_type].place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_4_y, anchor = "w")
        
        self.entry_growfactors_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_growfactors_filename[tax_type].place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_5_y, anchor = "e")
        self.entry_growfactors_filename[tax_type].insert(END, self.vars['GROWFACTORS_FILENAME'])
        self.button_growfactors_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Growfactors File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_growfactors_filename[tax_type], 'GROWFACTORS_FILENAME', tax_type))
        self.button_growfactors_filename[tax_type].place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_5_y, anchor = "w")
        
        self.entry_functions_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_functions_filename[tax_type].place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_6_y, anchor = "e")
        self.entry_functions_filename[tax_type].insert(END, self.vars[tax_type+'_functions_filename'])
        self.button_functions_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Functions File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_functions_filename[tax_type], tax_type+'_'+'functions_filename'))
        self.button_functions_filename[tax_type].place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_6_y, anchor = "w")
    
        self.entry_functions_names_filename[tax_type] = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_functions_names_filename[tax_type].place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_7_y, anchor = "e")
        self.entry_functions_names_filename[tax_type].insert(END, self.vars[tax_type+'_function_names_filename'])
        self.button_function_names_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Functions Names File", style='my.TButton', command=lambda: self.input_entry_data(self.entry_functions_names_filename[tax_type], tax_type+'_'+'function_names_filename'))
        self.button_function_names_filename[tax_type].place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_7_y, anchor = "w")
        
        self.entry_benchmark_filename[tax_type] = tk.Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_benchmark_filename[tax_type].place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_8_y, anchor = "e")
        self.entry_benchmark_filename[tax_type].insert(END, self.vars[tax_type+'_benchmark_filename'])
        self.button_benchmark_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Benchmark Filename", style='my.TButton', command=lambda: self.input_entry_data(self.entry_benchmark_filename[tax_type], tax_type+'_'+'benchmark_filename'))
        self.button_benchmark_filename[tax_type].place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_8_y, anchor = "w")

        self.entry_gdp_filename[tax_type] = tk.Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_gdp_filename[tax_type].place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_9_y, anchor = "e")
        self.entry_gdp_filename[tax_type].insert(END, self.vars['gdp_filename'])
        self.button_gdp_filename[tax_type] = ttk.Button(self.TAB1, text = "Change Nominal GDP Filename", style='my.TButton', command=lambda: self.input_entry_data(self.entry_gdp_filename[tax_type], 'gdp_filename'))
        self.button_gdp_filename[tax_type].place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_9_y, anchor = "w")
        
        self.l2[tax_type]=tk.Label(self.TAB1, text="Salary Variable: ", font = self.fontStyle)
        self.l2[tax_type].place(relx = self.block_1_entry_x - 3*self.entry_button_gap, 
                 rely = self.block_1_entry_10_y, anchor = "e")
    
        self.entry_salary_variable[tax_type] = ttk.Combobox(self.TAB1, value=self.show_salary_options(tax_type), font=self.text_font)
        self.entry_salary_variable[tax_type].current(3)
        self.entry_salary_variable[tax_type].place(relx = self.block_1_entry_x - 3*self.entry_button_gap, 
                        rely = self.block_1_entry_10_y, anchor = "w", width=100)
        self.entry_salary_variable[tax_type].bind("<<ComboboxSelected>>", lambda event: self.input_combo_data(event, self.entry_salary_variable[tax_type], 'SALARY_VARIABLE'))
          
        self.l3[tax_type]=tk.Label(self.TAB1, text="Start Year: ", font = self.fontStyle)
        self.l3[tax_type].place(relx = self.block_1_entry_x - 3*self.entry_button_gap, 
                 rely = self.block_1_entry_11_y, anchor = "e")
    
        self.entry_start_year[tax_type] = ttk.Combobox(self.TAB1, value=self.year_list, font=self.text_font)
        self.entry_start_year[tax_type].current(self.year_list.index(int(self.vars['start_year'])))
        self.entry_start_year[tax_type].place(relx = self.block_1_entry_x - 3*self.entry_button_gap, 
                        rely = self.block_1_entry_11_y, anchor = "w", width=80)
        self.entry_start_year[tax_type].bind("<<ComboboxSelected>>", lambda event: self.input_combo_data(event, self.entry_start_year[tax_type], 'start_year'))
    
        self.l31[tax_type]=tk.Label(self.TAB1, text="End Year: ", font = self.fontStyle)
        self.l31[tax_type].place(relx = self.block_1_entry_x + 2*self.entry_button_gap, 
                 rely = self.block_1_entry_11_y, anchor = "e")
        
        self.entry_end_year[tax_type] = ttk.Combobox(self.TAB1, value=self.year_list, font=self.text_font)
        self.entry_end_year[tax_type].current(self.year_list.index(int(self.vars['end_year'])))
        self.entry_end_year[tax_type].place(relx = self.block_1_entry_x + 2*self.entry_button_gap, 
                        rely = self.block_1_entry_11_y, anchor = "w", width=80)
        self.entry_end_year[tax_type].bind("<<ComboboxSelected>>", lambda event: self.input_combo_data(event, self.entry_end_year[tax_type], 'end_year'))    
        
        #self.chart_list = []

        #self.save_inputs()
        #self.completed_TAB1 = 1
        #self.tab6()

def tab1(self):    
    
    
    #self.save_inputs()
       
    """
    self.status['pit'] = tk.NORMAL if self.vars['pit'] else tk.DISABLED
    self.status['cit'] = tk.NORMAL if self.vars['cit'] else tk.DISABLED
    self.status['vat'] = tk.NORMAL if self.vars['vat'] else tk.DISABLED
    for tax_type in self.tax_list:
        if self.status[tax_type] == tk.NORMAL:
            self.vars[tax_type] = 1
    """
    #initializing the display widgets  
    self.initialize_vars()
    self.fontStyle = tkfont.Font(family="Calibri", size="12")
    self.fontStyle_sub_title = tkfont.Font(family="Calibri", size="14", weight="bold")         
    self.fontStyle_title = tkfont.Font(family="Calibri", size="18", weight="bold")
    self.s = ttk.Style()
    self.s.configure('my.TButton', font=self.fontStyle)        
    self.text_font = ('Calibri', '12')
    
    self.block_settings_pos_x = {}
    self.status = {}
    
    self.pos_x = [0.13, 0.40, 0.70]
    self.block_settings_pos_x['pit'] = self.pos_x[0]
    self.block_settings_pos_x['cit'] = self.pos_x[1]
    self.block_settings_pos_x['vat'] = self.pos_x[2]
    
    self.tax_list = ['pit', 'cit', 'vat']
    
    

    self.vars['pit'] = 0
    self.vars['cit'] = 0
    self.vars['vat'] = 0
    
    self.status['pit'] = tk.NORMAL
    self.status['cit'] = tk.DISABLED
    #self.status['vat'] = tk.NORMAL
    self.status['vat'] = tk.DISABLED
    
    self.block_1_title_pos_x = 0.15
    self.block_1_title_box_y = 0.15

    self.block_2_title_pos_x = 0.45
    
    self.block_3_title_pos_x = 0.75

    self.TAB1_root_title=tk.Label(self.TAB1,text="Tax Microsimulation Model",
             font = self.fontStyle_title)
    self.TAB1_root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")
    
    self.TAB1_root_title=tk.Label(self.TAB1,text="Setting",
             font = self.fontStyle_sub_title)
    self.TAB1_root_title.place(relx = self.title_pos_x, rely = self.sub_title_pos_y, anchor = "n")
    
    self.pit_chk = tk.IntVar()
    
    self.pit_chk_box = tk.Checkbutton(self.TAB1, text='Personal Income Tax', 
                                      font = self.fontStyle, variable=self.pit_chk,
                                      state = self.status['pit'],
                                      command=lambda: self.initiate_model(self.pit_chk, 'pit'))
    self.pit_chk_box.place(relx = self.pos_x[0], rely = self.block_1_title_box_y, anchor = "w", )

    self.cit_chk = tk.IntVar()
    self.cit_chk_box = tk.Checkbutton(self.TAB1, text='Corporate Income Tax', 
                                      font = self.fontStyle, variable=self.cit_chk,
                                      state = self.status['cit'],
                                      command=lambda: self.initiate_model(self.cit_chk, 'cit'))
    self.cit_chk_box.place(relx = self.pos_x[1], rely = self.block_1_title_box_y, anchor = "w")

    self.vat_chk = tk.IntVar()
    self.vat_chk_box = tk.Checkbutton(self.TAB1, text='Value Added Tax', 
                                      font = self.fontStyle, variable=self.vat_chk,
                                      state = self.status['vat'],
                                      command=lambda: self.initiate_model(self.vat_chk, 'vat'))
    self.vat_chk_box.place(relx = self.pos_x[2], rely = self.block_1_title_box_y, anchor = "w")    

    


# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:27:09 2020

@author: wb305167
"""

import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo
from tkinter import filedialog
from functools import partial
from threading import Thread
import time

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#from taxcalc import *

from PIL import Image,ImageTk
#import threaded_program as tp

class Progress_Bar:
    def __init__(self, master):
        self.progress_line(master)
    
    def progress_line(self, master):
        self._progress_label = tk.Label(text="Running...", anchor = "w")
        self._progress_label.place(relx = 0.1, rely = 0.78, anchor = "nw")
        # the value of "maximum" determines how fast progressbar moves
        self._progressbar = ttk.Progressbar(master, mode='indeterminate', 
                                            #maximum=4 # speed of progressbar
                                            )
        self._progressbar.place(relx = 0.1, rely = 0.8, anchor = "nw")
    
    @property
    def progressbar(self):
        return self._progressbar, self._progress_label  # return value of private member

class Application(Frame):
    #from generate_total_revenues import generate_total_revenues
    #from generate_policy_revenues1 import generate_policy_revenues
    #from generate_policy_revenues_behavior import generate_policy_revenues_behavior
    #from generate_policy_revenues1 import read_reform_dict
    #from generate_tax_expenditures import generate_tax_expenditures
    
    def __init__(self, master=None):
        super().__init__()

        Frame.__init__(self, master)
             
        #Create Tab Control
        TAB_CONTROL = ttk.Notebook(master)
        #TAB1
        self.TAB1 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB1, text=' Settings ')
        TAB_CONTROL.pack(expand=1, fill="both")

        self.TAB2 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB2, text=' Policy ')

        self.TAB3 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB3, text=' Revenue Forecast ')
        TAB_CONTROL.pack(expand=1, fill="both")
        
        self.TAB4 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB4, text=' Tax Expenditures ')
        TAB_CONTROL.pack(expand=1, fill="both")

        
        self.number = 0
        self.widgets = []
        #self.grid()
        self.createWidgets()

        self.reform={}
        self.selected_item = ""
        self.selected_value = ""
        self.selected_year = 2019
        self.sub_directory = "taxcalc"
        
        self.data_filename = "pit.csv"
        self.weights_filename = "pit_weights1.csv"
        self.records_variables_filename = "records_variables.json"
        self.cit_data_filename = "cit_cross.csv"
        self.cit_weights_filename = "cit_cross_wgts1.csv"
        self.corprecords_variables_filename = "corprecords_variables.json"
        self.gst_data_filename = "gst.csv"
        self.gst_weights_filename = "gst_weights.csv"
        self.gstrecords_variables_filename = "gstrecords_variables.json"         
        self.policy_filename = "current_law_policy_cmie.json"
        self.growfactors_filename = "growfactors1.csv"
        #self.growfactors_filename = "growfactors1.csv"              
        self.benchmark_filename = "tax_incentives_benchmark.json"
        self.fontStyle = tkfont.Font(family="Calibri", size="12")
        
        self.total_revenue_text1 = ""
        self.reform_revenue_text1 = ""
        #self.reform_filename = "app01_reform.json"


        self.fontStyle_sub_title = tkfont.Font(family="Calibri", size="14", weight="bold")         
        self.fontStyle_title = tkfont.Font(family="Calibri", size="18", weight="bold")
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        self.text_font = ('Calibri', '12')
                
        # positions
        
        self.title_pos_x = 0.5
        self.title_pos_y = 0.0
        
        self.block_1_title_pos_x = 0.15
        self.block_1_title_pos_y = 0.05
        self.block_title_entry_gap_y = 0.05
        self.block_entry_entry_gap_y = 0.05
        self.block_1_entry_x = self.block_1_title_pos_x + 0.05
        self.entry_entry_gap_y = 0.03
        self.block_1_entry_1_y = (self.block_1_title_pos_y+self.block_title_entry_gap_y)
        self.block_1_entry_2_y = (self.block_1_entry_1_y+self.block_entry_entry_gap_y)
        self.block_1_entry_3_y = (self.block_1_entry_2_y+self.block_entry_entry_gap_y)
        self.block_1_entry_4_y = (self.block_1_entry_3_y+self.block_entry_entry_gap_y)        
        self.entry_button_gap = 0.02
        
        # TAB Policy
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

        # TAB Tax Expenditure
        self.block_3_title_pos_x = self.block_1_title_pos_x
        self.block_3_title_pos_y = self.block_1_title_pos_y
        self.block_3_entry_x = self.block_1_entry_x
        self.block_3_entry_y = self.block_3_title_pos_y + self.block_title_entry_gap_y      
        self.button_3_pos_x = self.button_1_pos_x 
        self.button_3_pos_y = self.block_3_entry_y + 2*self.entry_button_gap        
             
        self.button_add_reform_x = self.block_2_TAB2_entry_1_3_x + self.block_2_TAB2_entry_entry_gap_x + 0.03
        
        self.root_title=Label(self.TAB2,text="Tax Microsimulation Model",
                 font = self.fontStyle_title)
        self.root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")
        
        self.l1=Label(self.TAB1,text="Data Inputs",
                 font = self.fontStyle_sub_title)
        self.l1.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
        #self.l1.place(relx = 0, rely = 0, anchor = "w")

        self.entry_data_filename = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_data_filename.place(relx = self.block_1_entry_x, 
                                  rely = self.block_1_entry_1_y,
                                  anchor = "e")
        self.entry_data_filename.insert(END, self.data_filename)
        self.button_data_filename = ttk.Button(self.TAB1, text = "Change Data File", style='my.TButton', command=self.input_data_filename)
        self.button_data_filename.place(relx = self.block_1_entry_x,
                                   rely = self.block_1_entry_1_y, anchor = "w")
        #button.place(x=140,y=50)
        
        self.entry_weights_filename = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_weights_filename.place(relx = self.block_1_entry_x,
                                     rely = self.block_1_entry_2_y, anchor = "e")
        self.entry_weights_filename.insert(END, self.weights_filename)
        self.button_weights_filename = ttk.Button(self.TAB1, text = "Change Weights File", style='my.TButton', command=self.input_weights_filename)
        self.button_weights_filename.place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_2_y, anchor = "w")
        
        self.entry_policy_filename = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_policy_filename.place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_3_y, anchor = "e")
        self.entry_policy_filename.insert(END, self.policy_filename)
        self.button_policy_filename = ttk.Button(self.TAB1, text = "Change Policy File", style='my.TButton', command=self.input_policy_filename)
        self.button_policy_filename.place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_3_y, anchor = "w")
        
        self.entry_growfactors_filename = Entry(self.TAB1, width=30, font = self.fontStyle)
        self.entry_growfactors_filename.place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_4_y, anchor = "e")
        self.entry_growfactors_filename.insert(END, self.growfactors_filename)
        self.button_growfactors_filename = ttk.Button(self.TAB1, text = "Change Growfactors File", style='my.TButton', command=self.input_growfactors_filename)
        self.button_growfactors_filename.place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_4_y, anchor = "w")
        #self.growfactors_filename = "taxcalc/"+self.growfactors_filename
        print(self.growfactors_filename)
        
        self.l1A=Label(self.TAB2, text="Current Law",
                 font = self.fontStyle_sub_title)
        self.l1A.place(relx = self.block_1_TAB2_title_pos_x, rely = self.block_1_TAB2_title_pos_y, anchor = "w")
        #(...)
        #action_with_arg = partial(action, arg)
        #button = Tk.Button(master=frame, text='press', command=action_with_arg)
        self.button_generate_revenue_curr_law = ttk.Button(self.TAB2, text = "Generate Current Law Total Revenues", style='my.TButton', command=self.clicked_generate_revenues)
        self.button_generate_revenue_curr_law.place(relx = self.button_1_TAB2_pos_x, 
                                                 rely = self.button_1_TAB2_pos_y, anchor = "w")
        
        self.l2=Label(self.TAB2, text="Reform", font = self.fontStyle_sub_title)
        self.l2.place(relx = self.block_1_title_pos_x, rely = self.block_2_TAB2_title_pos_y, anchor = "w")
        
        self.l3=Label(self.TAB2, text="Select Policy Parameter: ", font = self.fontStyle)
        self.l3.place(relx = self.block_2_TAB2_entry_1_1_x, 
                 rely = self.block_2_TAB2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        
        self.current_law_policy, self.policy_options_list = self.policy_options()
        #self.policy_options_list.remove('gst_rate')
        self.block_widget_dict = {}
        self.block_selected_dict = {}
        self.num_reforms = 1
        
       
        self.block_widget_dict[1] = {}
        self.block_selected_dict[1] = {}
        self.block_widget_dict[1][1] = ttk.Combobox(self.TAB2, value=self.policy_options_list, font=self.text_font, name=str(self.num_reforms))
        self.block_widget_dict[1][1].current(1)
        self.block_widget_dict[1][1].place(relx = self.block_2_TAB2_entry_1_1_x, 
                        rely = self.block_2_TAB2_entry_1_1_y, anchor = "w", width=300)
        
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
        
        self.num_reforms += 1
        self.button_add_reform = ttk.Button(self.TAB2, text="+", style='my.TButton', command=self.create_policy_widgets, width=2)
        self.button_add_reform.place(relx = self.button_add_reform_x, rely = self.block_2_TAB2_entry_1_1_y, anchor = "w")        
        
        self.button_generate_revenue_policy = ttk.Button(self.TAB2, text = "Generate Revenue under Reform", style='my.TButton', command=self.clicked_generate_policy_revenues)
        self.button_2_TAB2_pos_x = self.button_1_pos_x
        self.button_2_TAB2_pos_y = (self.block_2_TAB2_entry_1_1_y+(self.num_reforms-1)*(self.entry_entry_gap_y)) +self.entry_button_gap
        self.button_generate_revenue_policy.place(relx = self.button_2_TAB2_pos_x,
                                                    rely = self.button_2_TAB2_pos_y, anchor = "w")

        self.l3A=Label(self.TAB4,text="Tax Expenditures",
                 font = self.fontStyle_sub_title)
        self.l3A.place(relx = self.block_3_title_pos_x, rely = self.block_3_title_pos_y, anchor = "w")

        self.entry_benchmark_filename = Entry(self.TAB4, width=30, font = self.fontStyle)
        self.entry_benchmark_filename.place(relx = self.block_3_entry_x, 
                                  rely = self.block_3_entry_y,
                                  anchor = "e")
        self.entry_benchmark_filename.insert(END, self.benchmark_filename)
        self.button_benchmark_filename = ttk.Button(self.TAB4, text = "Change Benchmark File", style='my.TButton', command=self.input_benchmark_filename)
        self.button_benchmark_filename.place(relx = self.block_3_entry_x,
                                   rely = self.block_3_entry_y, anchor = "w")        
        self.button_generate_tax_expenditures = ttk.Button(self.TAB4, text = "Generate Tax Expenditures", style='my.TButton', command=self.clicked_generate_tax_expenditures)
        self.button_generate_tax_expenditures.place(relx = self.button_3_pos_x, 
                                                 rely = self.button_3_pos_y, anchor = "w")        
        
        self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
        #image = tk.PhotoImage(file="blank.png")
        self.pic = tk.Label(self.TAB2,image=self.image)
        self.pic.place(relx = 0.5, rely = 0.2, anchor = "nw")
        self.pic.image = self.image

   
    def clicked_generate_revenues(self):

        vars = {}
        vars['DEFAULTS_FILENAME'] = self.policy_filename
        #filename_list = self.growfactors_filename.split('/')
        #self.growfactors_filename_global = filename_list[-1]        
        vars['GROWFACTORS_FILENAME'] = self.growfactors_filename
        vars['pit_data_filename'] = self.data_filename
        vars['pit_weights_filename'] = self.weights_filename
        vars['records_variables_filename'] = self.records_variables_filename        
        vars['cit_data_filename'] = self.cit_data_filename
        vars['cit_weights_filename'] = self.cit_weights_filename
        vars['corprecords_variables_filename'] = self.corprecords_variables_filename
        vars['gst_data_filename'] = self.gst_data_filename
        vars['gst_weights_filename'] = self.gst_weights_filename
        vars['gstrecords_variables_filename'] = self.gstrecords_variables_filename        
        vars['benchmark_filename'] = self.benchmark_filename
        
        with open('global_vars.json', 'w') as f:
            json.dump(vars, f)
        f = open('global_vars.json')
        vars = json.load(f)
        print("vars in gui", vars)

        progress_bar = Progress_Bar(self.master)
        self.progressbar, self.progress_label = progress_bar.progressbar
        #self.foo_thread = Thread(target=self.generate_policy_revenues)
        from generate_revenues import generate_revenues       
        self.foo_thread = Thread(target=generate_revenues)        
        self.foo_thread.daemon = True
        self.progressbar.start(interval=10)
        self.foo_thread.start()
        self.master.after(20, self.check_thread)

    def check_thread(self):
        if self.foo_thread.is_alive():
            self.master.after(20, self.check_thread)
            #print("Hello in progress")
        else:
            print("Hello ended")
            self.progressbar.stop()
            self.progressbar.destroy()
            self.progress_label.destroy()
            self.foo_thread.join()

    def clicked_generate_policy_revenues(self):
        #from generate_policy_revenues1 import fact
        #print("self.num_reforms ", self.num_reforms)
        # fill the selected and modified policy value and year
        # of the last entry
        self.block_selected_dict[self.num_reforms-1]['selected_value']= self.block_widget_dict[self.num_reforms-1][3].get()
        self.block_selected_dict[self.num_reforms-1]['selected_year']= self.block_widget_dict[self.num_reforms-1][2].get()
        # save the selected policy variables in a json file       
        #print("block_selected_dict before json save: ",self.block_selected_dict)
        with open('reform.json', 'w') as f:
            json.dump(self.block_selected_dict, f)

        vars = {}
        vars['DEFAULTS_FILENAME'] = self.policy_filename
        #filename_list = self.growfactors_filename.split('/')
        #self.growfactors_filename_global = filename_list[-1]        
        vars['GROWFACTORS_FILENAME'] = self.growfactors_filename
        vars['pit_data_filename'] = self.data_filename
        vars['pit_weights_filename'] = self.weights_filename
        vars['records_variables_filename'] = self.records_variables_filename        
        vars['cit_data_filename'] = self.cit_data_filename
        vars['cit_weights_filename'] = self.cit_weights_filename
        vars['corprecords_variables_filename'] = self.corprecords_variables_filename
        vars['gst_data_filename'] = self.gst_data_filename
        vars['gst_weights_filename'] = self.gst_weights_filename
        vars['gstrecords_variables_filename'] = self.gstrecords_variables_filename        
        vars['benchmark_filename'] = self.benchmark_filename
        
        with open('global_vars.json', 'w') as f:
            json.dump(vars, f)
        f = open('global_vars.json')
        vars = json.load(f)
        print("vars in gui", vars)

        progress_bar = Progress_Bar(self.master)
        self.progressbar, self.progress_label = progress_bar.progressbar
        #self.foo_thread = Thread(target=self.generate_policy_revenues)
        from generate_policy_revenues import generate_policy_revenues       
        self.foo_thread = Thread(target=generate_policy_revenues)        
        self.foo_thread.daemon = True
        self.progressbar.start(interval=10)
        self.foo_thread.start()
        self.master.after(20, self.check_thread)

    def clicked_generate_tax_expenditures(self):
        progress_bar = Progress_Bar(self.master)
        self.progressbar, self.progress_label = progress_bar.progressbar
        self.foo_thread = Thread(target=self.generate_tax_expenditures)
        self.foo_thread.daemon = True
        self.progressbar.start(interval=10)
        self.foo_thread.start()
        self.master.after(20, self.check_thread)
        
    def Add_Reform(self, event=None):
        self.num_reforms.set(self.num_reforms.get() + 1)
            
    def createWidgets(self):
        #self.cloneButton = Button ( self, text='Clone', command=self.clone)
        #self.cloneButton.grid()
        return

    def create_policy_widgets(self):
        print("num_reforms in policy widget ", self.num_reforms)
        self.block_widget_dict[self.num_reforms] = {}
        self.block_selected_dict[self.num_reforms] = {}
        self.block_widget_dict[self.num_reforms][1] = ttk.Combobox(self.TAB2, value=self.policy_options_list, font=self.text_font, name=str(self.num_reforms))
        self.block_widget_dict[self.num_reforms][1].current(1)
        self.block_widget_dict[self.num_reforms][1].place(relx = self.block_2_TAB2_entry_1_1_x, 
                        rely = (self.block_2_TAB2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w", width=300)
        self.block_widget_dict[self.num_reforms][1].bind("<<ComboboxSelected>>", self.show_policy_selection)

        self.block_widget_dict[self.num_reforms][2] = Entry(self.TAB2, width=6, font=self.fontStyle)
        self.block_widget_dict[self.num_reforms][2].place(relx = self.block_2_TAB2_entry_1_2_x,
                                                          rely = (self.block_2_TAB2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w")

        self.block_widget_dict[self.num_reforms][3] = Entry(self.TAB2, width=14, font=self.fontStyle)
        self.block_widget_dict[self.num_reforms][3].place(relx = self.block_2_TAB2_entry_1_3_x,
                                                          rely = (self.block_2_TAB2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w")
        self.num_reforms += 1
        self.button_2_TAB2_pos_y = (self.block_2_TAB2_entry_1_1_y+(self.num_reforms-1)*(self.entry_entry_gap_y))+self.entry_button_gap        
        self.button_generate_revenue_policy.place(relx = self.button_2_TAB2_pos_x,
                                            rely = self.button_2_TAB2_pos_y, anchor = "w")

    
    def input_data_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.data_filename = filename_list[-1]
        self.entry_data_filename.delete(0,END)
        self.entry_data_filename.insert(0,self.data_filename)
    
    def input_weights_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #print(filez[0])
        #self.master.update()        
        #filename_path = tk.splitlist(filez)[0]
        #filename_list = filename_path.split('/')
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.weights_filename = filename_list[-1]
        self.entry_weights_filename.delete(0,END)
        self.entry_weights_filename.insert(0,self.weights_filename)
    
    def input_policy_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.policy_filename = filename_list[-1]
        self.entry_policy_filename.delete(0,END)
        self.entry_policy_filename.insert(0,self.policy_filename)

    def input_growfactors_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        print("filename_list ", filename_list)
        self.growfactors_filename = filename_list[-1]
        #self.growfactors_filename = filename_list[-2]+"/"+filename_list[-1]        
        self.entry_growfactors_filename.delete(0,END)
        self.entry_growfactors_filename.insert(0,self.growfactors_filename)
        
    def input_benchmark_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.benchmark_filename = filename_list[-1]
        self.entry_benchmark_filename.delete(0,END)
        self.entry_benchmark_filename.insert(0,self.benchmark_filename)
               
    
    def policy_options(self):
        with open(self.sub_directory+'/'+self.policy_filename) as f:
            current_law_policy = json.load(f)
        current_law_policy_sorted = dict(sorted(current_law_policy.items()))    
        policy_options_list = []
        for k, s in current_law_policy_sorted.items():
            #print(k)
            #print(current_law_policy[k]['description'])
            #policy_option_list = policy_option_list + [current_law_policy[k]['description']]
            policy_options_list = policy_options_list + [k[1:]]
        return (current_law_policy, policy_options_list)
    
    def policy_reform():
        self.reform={}
        self.reform['policy']={}
        self.reform['policy']['_'+self.selected_item]={}
        self.updated_year = self.block_widget_dict[1][2].get()
        self.updated_value = self.block_widget_dict[1][3].get()
        self.reform['policy']['_'+selected_item][self.updated_year]=[self.updated_value]
        print("Reform2: ", self.reform)
    
        
    def show_policy_selection(self, event):
        active_widget_number = int(str(event.widget)[-1])
        print("active_widget_number: ", active_widget_number)
        num = active_widget_number
        #for num in range(1, self.num_reforms):
        self.selected_item = self.block_widget_dict[num][1].get()
        self.selected_value = self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.selected_year = self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        self.block_selected_dict[num]['selected_item']= self.block_widget_dict[num][1].get()
        self.block_selected_dict[num]['selected_value']= self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.block_selected_dict[num]['selected_year']= self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        
        print("self.selected_value: ", self.selected_value)
        print("self.selected_year: ", self.selected_year)
        self.block_widget_dict[num][3].delete(0, END)
        self.block_widget_dict[num][3].insert(END, self.selected_value)
        self.block_widget_dict[num][2].delete(0, END)
        self.block_widget_dict[num][2].insert(END, self.selected_year)

        for num in range(1, self.num_reforms):        
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
        
        print("self.block_selected_dict in policy selection: ", self.block_selected_dict)
        #with open('reform.json', 'w') as f:
        #    json.dump(self.block_selected_dict, f)
        return
    # --- main ---
    
 
def main():
    root = tk.Tk()
    root.geometry('1000x600')
    root.title("World Bank Microsimulation Model")
    root.state('zoomed')
    #TAB_CONTROL.pack(expand=1, fill="both")
    app = Application(root)
    app.mainloop()


if __name__ == '__main__':
    main()
    #main()

    
    
"""
    
    #Button(self.TAB2, row=6, column=1, sticky = W, pady = (0,25), padx = (0,0))
    root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.master.title("Sample application")
    app.mainloop()
    
 """   

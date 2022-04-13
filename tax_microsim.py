# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:27:09 2020

@author: wb305167
"""
from tkinter import scrolledtext
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo
import traceback
import sys
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter import filedialog
from functools import partial
from threading import Thread
import time
import ctypes
import csv

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

        
class Application(tk.Frame):
    from guifuncs import save_inputs, get_inputs
    from guifuncs import get_inputs_after_saving_current_vars
    from guifuncs import get_growfactors_dict, update_grow_factors_csv 
    from gui_tab1 import tab1
    #from gui_tab1 import tab12
    from gui_tab1 import display_entry
    from gui_tab1 import grid_placement
    
    #from gui_tab21 import super_tab
    from gui_tab3 import tab3
    from gui_tab3 import display_elasticity
    from gui_tab3 import grid_placement_tab3
    from gui_tab4 import tab4
    from gui_tab4 import display_tax_expenditure   
    from gui_tab5 import tab5
    from gui_tab5 import display_distribution
    from gui_tab5 import display_distribution_table    
    from gui_tab6 import tab6
    from gui_tab6 import update_chart_list    
    from gui_tab6 import display_chart
    from gui_tab7 import tab7   
    from gui_tab7 import get_gf_dict
    from gui_tab8 import tab8
    from gui_tab8 import display_error    

   
    def __init__(self, master=None):
        super().__init__()

        tk.Frame.__init__(self, master)

        #Create Tab Control
        TAB_CONTROL = ttk.Notebook(master)

        self.TAB1 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB1, text=' Start ')
        TAB_CONTROL.pack(expand=1, fill="both")

        self.TAB2 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB2, text=' Policy ')

        self.TAB3 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB3, text=' Behavior ')
        TAB_CONTROL.pack(expand=1, fill="both")
        
        self.TAB4 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB4, text=' Tax Expenditures ')
        TAB_CONTROL.pack(expand=1, fill="both")

        self.TAB5 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB5, text=' Distribution ')
        TAB_CONTROL.pack(expand=1, fill="both")  
        
        self.TAB6 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB6, text=' Charts ')
        TAB_CONTROL.pack(expand=1, fill="both")  

        self.TAB7 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB7, text=' Growfactors ')
        TAB_CONTROL.pack(expand=1, fill="both")
        
        self.TAB8 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(self.TAB8, text=' Settings ')
        TAB_CONTROL.pack(expand=1, fill="both")        
     
        #initializing json container to hold all selections
        self.vars = {}
        with open('global_vars.json', 'w') as f:
            f.write(json.dumps(self.vars, indent=2))
        
        # TAB Start
        self.block_1_title_pos_x = 0.15
        self.grid_placement(self.block_1_title_pos_x)
        self.tab1()
        vars = self.get_inputs()
        sub_directory = 'taxcalc'
        tax_list = []
        if vars['pit']:
            tax_list = tax_list + ['pit']
        if vars['cit']:
            tax_list = tax_list + ['cit']
        if vars['vat']:
            tax_list = tax_list + ['vat']
        tax_type = tax_list[0]       
        if vars!={}:         
            with open(sub_directory+'/'+vars['DEFAULTS_FILENAME']) as f:
                self.current_law_policy = json.load(f)
            with open(sub_directory+'/'+vars[tax_type+'_records_variables_filename']) as vfile:
                self.vardict = json.load(vfile)                
            self.ATTRIBUTE_READ_VARS = set(k for k,
                      v in self.vardict['read'].items()
                      if v['attribute'] == 'Yes')
            self.growfactors = self.get_growfactors_dict(sub_directory+'/'+vars['GROWFACTORS_FILENAME'], self.ATTRIBUTE_READ_VARS)
            #print('self.growfactors ', self.growfactors)
        else:
            self.current_law_policy={}
            self.growfactors = {}
        #print(vars)
        #self.tab12()
        
        # TAB Policy
        from super_combo import super_combo
        self.year_value_pairs_policy_dict = 1       
        self.tab_generate_revenue_policy = super_combo(self.TAB2, self.current_law_policy, 'row_label', 'value', 0.01, 0.20)
        (self.button_generate_revenue_policy, self.block_widget_dict) = self.tab_generate_revenue_policy.display_widgets(self.TAB2)
        self.button_generate_revenue_policy.configure(command=self.clicked_generate_policy_revenues)

         # TAB Behavior
        self.tab3()
        
        # TAB Tax Expenditure
        self.tab4()

        # TAB Distribution
        self.tab5()
        
        # TAB Charts
        self.tab6()
        
        # TAB Growfactors
        #self.vars['GROWFACTORS_FILENAME']

        """
        self.year_value_pairs_growfactors_dict = len(self.growfactors[list(self.growfactors.keys())[0]]['Year']) 
        self.tab_growfactors = super_combo(self.TAB7, self.growfactors, 'Year', 'Value', 0.03, 0.20)
        (self.button_growfactors, self.growfactors_widget_dict) = self.tab_growfactors.display_widgets(self.TAB7)
        self.button_growfactors.configure(command=self.clicked_generate_policy_revenues)        
        """
        self.tab7()      

        # TAB Settings
        self.tab8()  
        
    def print_stdout(self):
        '''Illustrate that using 'print' writes to stdout'''
        print("this is stdout")

    def print_stderr(self):
        '''Illustrate that we can write directly to stderr'''
        sys.stderr.write("this is stderr\n")
                
    def on_closing(self, widget, window):
        widget.set(0)
        window.destroy()

    def find_active_taxes(self):
        active_tax = []
        for i in range(len(self.tax_list)):
            tax_var = self.vars[self.tax_list[i]]
            if tax_var:
                active_tax = active_tax + [self.tax_list[i]]    
        return(active_tax)

    def clear_chk(self, widget, window):
        widget.set(0)
        window.destroy()        

    def allocate_pos_x(self, pos_x, status, pos_x_dict):
        pos_x_dict['pit']=pos_x[0]
        pos_x_dict['cit']=pos_x[1]
        pos_x_dict['vat']=pos_x[2]        
        if status['pit'] == tk.NORMAL:
            if status['cit'] != tk.NORMAL:
                if status['vat'] == tk.NORMAL:
                    pos_x_dict['vat']=pos_x[1]
                    pos_x_dict['cit']=pos_x[2]                
        else:
            if status['cit'] == tk.NORMAL:
                pos_x_dict['cit']=pos_x[0]
                if status['vat'] == tk.NORMAL:
                    pos_x_dict['vat']=pos_x[1]
                    pos_x_dict['pit']=pos_x[2]
                else:
                    pos_x_dict['pit']=pos_x[1]                    
                    pos_x_dict['vat']=pos_x[2]  
        return pos_x_dict

# Once the the tax is selected populate the drop down lists
    def gui_tab1_control(self, widget_var, tax_type, pos_x):
        self.display_entry(widget_var, tax_type, pos_x)
        self.save_inputs()
        vars=self.get_inputs()
        sub_directory = 'taxcalc'
        if vars!={}:           
            with open(sub_directory+'/'+vars['DEFAULTS_FILENAME']) as f:
                self.current_law_policy = json.load(f)
            self.growfactors = self.get_growfactors_dict(sub_directory+'/'+vars['GROWFACTORS_FILENAME'], self.ATTRIBUTE_READ_VARS)
            #print(self.growfactors)
        else:
            self.current_law_policy={}
            self.growfactors = {}        
        self.block_widget_dict[1][1].config(values=self.tab_generate_revenue_policy.policy_options(self.current_law_policy))
        self.growfactors_widget_dict[1][1].config(values=self.tab_growfactors.policy_options(self.growfactors))

    def gui_tab6_control(self, widget_var, tax_type, pos_x):
        self.display_entry(widget_var, tax_type, pos_x)
        self.save_inputs()
        vars=self.get_inputs()
        self.growfactors_widget_dict[1][1].config(values=self.tab_growfactors.policy_options('taxcalc/'+vars['DEFAULTS_FILENAME']))

    def input_entry_data(self, widget, varname, tax_type=None):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        old_filename = widget.get()
        print('Old filename is: ', widget.get())       
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        filename = filename_list[-1]
        widget.delete(0,tk.END)
        widget.insert(0,filename)
        self.vars[varname] = filename
        if (tax_type is not None) :
            print('new filename is :', widget.get())
            if (varname=='GROWFACTORS_FILENAME'):
                if filename != old_filename:
                    self.vars[varname] = filename
                    self.entry_salary_variable[tax_type].config(values=self.show_salary_options(tax_type))
            if (varname=='DEFAULTS_FILENAME'):
                if filename != old_filename:
                    self.vars[varname] = filename
                    self.block_widget_dict[1][1].config(values=self.tab_generate_revenue_policy.policy_options())
             
    def input_combo_data(self, event, widget, varname):
        #print("method is called")
        selected = widget.get()
        if selected.isdigit():
            self.vars[varname] = int(widget.get())
        else:
            self.vars[varname] = widget.get()
        #print(self.vars[varname])

    def input_checkbox(self, widget, varname):
        #print("check method is called")
        self.vars[varname] = int(widget.get())
        #print(self.vars[varname])
        #self.vars['adjust_behavior'] = self.behavior_chk.get()

    def show_salary_options(self, tax_type):
        df = pd.read_csv(self.sub_directory+'/'+self.vars['GROWFACTORS_FILENAME'])
        varlist = list(df.columns)
        #print('varlist: ', varlist)
        return (varlist)
    
    def show_record_options(self, tax_type):        
        with open(self.sub_directory+'/'+self.vars[tax_type+'_records_variables_filename']) as f:
            record_variables = json.load(f)
        record_variables_sorted = dict(sorted(record_variables.items()))    
        record_variables_list = []
        for k, s in record_variables_sorted['read'].items(): 
            record_variables_list = record_variables_list + [k]
        return (record_variables_list)
        
    def clicked_generate_revenues(self):
        # self.get_inputs()
        # progress_bar = Progress_Bar(self.master)
        # self.progressbar, self.progress_label = progress_bar.progressbar
        # #self.foo_thread = Thread(target=self.generate_policy_revenues)
        # from generate_revenues import generate_revenues    
        # self.foo_thread = Thread(target=generate_revenues)        
        # self.foo_thread.daemon = True
        # self.progressbar.start(interval=10)
        # self.foo_thread.start()
        # self.master.after(20, self.check_thread)
        pass

    def check_thread(self):
        if self.foo_thread.is_alive():
            self.master.after(20, self.check_thread)
            #print("Hello in progress")
        else:
            if self.verbose:
                print("Run Completed")
            self.progressbar.stop()
            self.progressbar.destroy()
            self.progress_label.destroy()
            self.foo_thread.join()

    def generate_changes_dict(self, widget_dict, year_value_pairs, year_check=None, start_year=None, end_year=None):
        selected_dict={}
        #print('block_widget_dict ', self.block_widget_dict)
        #print('length block_widget_dict ', len(self.block_widget_dict))
        num_changes = len(widget_dict)
        self.selected_attribute_widget
        #print(widget_dict)
        #print('num_changes ', num_changes)
        for num in range(1, num_changes+1):
            #print('num ', num)
            selected_item = widget_dict[num][1].get()
            if (selected_item!=''):
                selected_dict[num]={}            
                selected_dict[num]['selected_item']= selected_item
                selected_dict[num]['selected_year'] = []
                selected_dict[num]['selected_value'] = []
                for i in range(year_value_pairs):        
                    selected_dict[num]['selected_year']= selected_dict[num]['selected_year'] + [widget_dict[num][2][i].get()]
                    selected_dict[num]['selected_value']= selected_dict[num]['selected_value'] + [widget_dict[num][3][i].get()]   
                    #print('selected_dict ', selected_dict)
                    if year_check:
                        #print('i ', i)
                        #print(selected_dict[num]['selected_year'][i])
                        #print(start_year)
                        if int(selected_dict[num]['selected_year'][i]) < int(start_year):
                            showinfo("Warning", "Reform Year is earlier than Start Year")
                            return
                        if int(selected_dict[num]['selected_year'][i]) > int(end_year):
                            showinfo("Warning", "Reform Year is later than End Year")            
                            return
        print('selected_dict ', selected_dict)
        return selected_dict
    
    def clicked_generate_policy_revenues(self):
        #Save all the GUI inputs into global_vars.json file"
        # and retrieve the saved inputs for use
        vars = self.get_inputs_after_saving_current_vars()
        if vars['show_error_log']:
            self.logger.clear()
        self.verbose = vars['verbose']
        self.block_selected_dict = self.generate_changes_dict(self.block_widget_dict, self.year_value_pairs_policy_dict, year_check=True, start_year=vars['start_year'], end_year=vars['end_year'])

        with open('reform.json', 'w') as f:
            f.write(json.dumps(self.block_selected_dict, indent=2))
        
        if self.verbose:
            print('Reform dictionary: ', self.block_selected_dict)

        self.growfactors_selected_dict = self.generate_changes_dict(self.growfactors_widget_dict, 
                                                                    self.year_value_pairs_growfactors_dict, year_check=False)

        if self.verbose:      
            print("Growfactors Changes Dict ",self.growfactors_selected_dict)            

        self.update_grow_factors_csv(self.growfactors, self.growfactors_selected_dict,
                               'Year', 'Value', 
                                self.sub_directory+'/'+vars['GROWFACTORS_FILENAME'])
        
        progress_bar = Progress_Bar(self.master)
        self.progressbar, self.progress_label = progress_bar.progressbar
        from generate_policy_revenues import generate_policy_revenues       
        self.foo_thread = Thread(target=generate_policy_revenues)        
        self.foo_thread.daemon = True
        self.progressbar.start(interval=10)
        self.foo_thread.start()
        self.master.after(20, self.check_thread)
        # self.image = tk.PhotoImage(file="world_bank.png")
        # self.pic = tk.Label(self.TAB6,image=self.image)
        # self.pic.place(relx = 0.45, rely = 0.2, anchor = "nw")
        # self.pic.image = self.image 
        
        
    def clicked_generate_tax_expenditures(self):
        progress_bar = Progress_Bar(self.master)
        self.progressbar, self.progress_label = progress_bar.progressbar
        self.foo_thread = Thread(target=self.generate_tax_expenditures)
        self.foo_thread.daemon = True
        self.progressbar.start(interval=10)
        self.foo_thread.start()
        self.master.after(20, self.check_thread)
        
    def clicked_display_charts(self):
        pass
    
    """        
    def Add_Reform(self, event=None):
        self.num_reforms.set(self.num_reforms.get() + 1)
            
    def createWidgets(self):
        #self.cloneButton = Button ( self, text='Clone', command=self.clone)
        #self.cloneButton.grid()
        return
    """

    def elasticity_options(self, tax_type):
        with open(self.sub_directory+'/'+self.vars['DEFAULTS_FILENAME']) as f:
            current_law_policy = json.load(f)
        current_law_policy_sorted = dict(sorted(current_law_policy.items()))
        elasticity_dict={}
        elasticity_items_list = []
        for k, s in current_law_policy_sorted.items(): 
            #print(k)
            #print(current_law_policy[k]['description'])
            #policy_option_list = policy_option_list + [current_law_policy[k]['description']]
            if (k[1:11] == 'elasticity'):
                if (k[-5:] == 'value'):
                    item = k[1:-6] 
                    elasticity_dict[k] = {}
                    elasticity_dict[k]['item'] = item
                    elasticity_dict[k]['long_name'] = current_law_policy[k]['long_name']
                    elasticity_dict[k]['value0']= current_law_policy[k]['value'][0][0]
                    elasticity_dict[k]['value1']= current_law_policy[k]['value'][0][1]
                    elasticity_dict[k]['value2']= current_law_policy[k]['value'][0][2]
                    elasticity_dict[k]['year']= current_law_policy[k]['row_label'][0]
                    
                    v = k[:-6]+'_threshold'
                    elasticity_dict[k]['threshold0']= current_law_policy[v]['value'][0][0]
                    elasticity_dict[k]['threshold1']= current_law_policy[v]['value'][0][1]
                    elasticity_dict[k]['threshold2']= current_law_policy[v]['value'][0][2]

                    elasticity_items_list = elasticity_items_list + [item]
        print("elasticity_dict in elasticity_options: ", elasticity_dict)        
        return (elasticity_dict, elasticity_items_list)
    
    def elasticity_reform():
        self.elasticity={}
        self.elasticity[self.selected_elasticity_item]={}
        
        self.updated_bracket1 = self.elasticity_widget_dict[1][2].get()
        self.updated_value = self.block_widget_dict[1][3].get()
        self.reform['policy']['_'+selected_item][self.updated_year]=[self.updated_value]
        print("Reform2: ", self.reform)
           
    def show_elasticity_selection(self, event, elasticity_dict, selected_dict, widget, tax_type):
        active_widget_number = int(str(event.widget)[-1])
        print("active_widget_number in show_elasticity_selection: ", active_widget_number)
        num = active_widget_number
        #print(elasticity_dict)
        #for num in range(1, self.num_reforms):
        self.selected_elasticity_item = '_'+widget[num][1].get()
        print('elasticity_dict in show_elasticity_selection',elasticity_dict)
        print('item in show_elasticity_selection', self.selected_elasticity_item) 
        self.selected_threshold1 = elasticity_dict[self.selected_elasticity_item+'_value']['threshold0']
        self.selected_threshold2 = elasticity_dict[self.selected_elasticity_item+'_value']['threshold1']
        self.selected_threshold3 = elasticity_dict[self.selected_elasticity_item+'_value']['threshold2']
        self.selected_elasticity1 = elasticity_dict[self.selected_elasticity_item+'_value']['value0']
        self.selected_elasticity2 = elasticity_dict[self.selected_elasticity_item+'_value']['value1']
        self.selected_elasticity3 = elasticity_dict[self.selected_elasticity_item+'_value']['value2']
        self.selected_year = elasticity_dict[self.selected_elasticity_item+'_value']['year']

        selected_dict[num]['selected_item']= self.selected_elasticity_item
        selected_dict[num]['selected_threshold1']= self.selected_threshold1
        selected_dict[num]['selected_threshold2']= self.selected_threshold2
        selected_dict[num]['selected_threshold3']= self.selected_threshold3
        selected_dict[num]['selected_elasticity1']= self.selected_elasticity1
        selected_dict[num]['selected_elasticity2']= self.selected_elasticity2
        selected_dict[num]['selected_elasticity3']= self.selected_elasticity3
        selected_dict[num]['selected_year']= self.selected_year
                   
        print("self.selected_item: ", self.selected_elasticity_item)
        print("self.selected_threshold1: ", self.selected_threshold1)
        print("self.selected_threshold2: ", self.selected_threshold2)
        print("self.selected_threshold3: ", self.selected_threshold3)
        print("self.selected_elasticity1: ", self.selected_elasticity1)
        print("self.selected_elasticity2: ", self.selected_elasticity2)
        print("self.selected_elasticity3: ", self.selected_elasticity3)
        print("self.selected_year: ", self.selected_year)        
        widget[num][2].delete(0, END)
        widget[num][2].insert(END, self.selected_threshold1)
        widget[num][3].delete(0, END)
        widget[num][3].insert(END, self.selected_threshold2)
        widget[num][4].delete(0, END)
        widget[num][4].insert(END, self.selected_threshold3)
        widget[num][5].delete(0, END)
        widget[num][5].insert(END, self.selected_elasticity1)
        widget[num][6].delete(0, END)
        widget[num][6].insert(END, self.selected_elasticity2)
        widget[num][7].delete(0, END)
        widget[num][7].insert(END, self.selected_elasticity3) 
        
        """
        for num in range(1, self.num_reforms):        
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
        
        print("self.block_selected_dict in policy selection: ", self.block_selected_dict)
        """
        #with open('reform.json', 'w') as f:
        #    json.dump(self.block_selected_dict, f)
        return

    def show_elasticity_selection1(self, event):
        return

   
    def create_elasticity_widgets(self, tab, selected_dict, widget, num_elasticity, tax_type):
        print('tax type func: ',tax_type)
        #t_type = str(event.widget)[-5:-2]
        #print('tax type widget: ',t_type)
        self.grid_placement_tab3(self.block_elasticity_pos_x[tax_type])
        print("entries in elasticity widget ", num_elasticity)
        print("num in create: ", num_elasticity)
        print("self num in create: ", self.num_elasticity_changes[tax_type])
        widget[num_elasticity] = {}
        print('selected_dict before', selected_dict)
        selected_dict[num_elasticity] = {}
        #print('selected_dict after', selected_dict)
        widget[num_elasticity][1] = ttk.Combobox(tab, value=self.elasticity_items_list[tax_type], font=self.text_font, name=tax_type+'_'+str(num_elasticity))
        widget[num_elasticity][1].current(1)
        widget[num_elasticity][1].place(relx = self.block_2_TAB3_entry_1_1_x, 
                        rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w", width=200)
        widget[num_elasticity][1].bind("<<ComboboxSelected>>", lambda event: self.show_elasticity_selection(event, self.elasticity_dict[tax_type], selected_dict, widget, tax_type))

        self.TAB3_l4=Label(self.TAB3,text="Threshold1: ", font = self.fontStyle)
        self.TAB3_l4.place(relx = self.block_2_TAB3_entry_1_2_x, 
             rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))-self.text_entry_gap, anchor = "w")        
        widget[num_elasticity][2] = Entry(tab, width=10, font=self.fontStyle)
        widget[num_elasticity][2].place(relx = self.block_2_TAB3_entry_1_2_x,
                                                          rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w")
        self.TAB3_l5=Label(self.TAB3,text="Threshold2: ", font = self.fontStyle)
        self.TAB3_l5.place(relx = self.block_2_TAB3_entry_1_3_x,
                       rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))-self.text_entry_gap, anchor = "w") 
        widget[num_elasticity][3] = Entry(tab, width=10, font=self.fontStyle)
        widget[num_elasticity][3].place(relx = self.block_2_TAB3_entry_1_3_x,
                                                          rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w")
        self.TAB3_l6=Label(self.TAB3,text="Threshold3: ", font = self.fontStyle)
        self.TAB3_l6.place(relx = self.block_2_TAB3_entry_1_4_x,
                       rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))-self.text_entry_gap, anchor = "w")        
        widget[num_elasticity][4] = Entry(tab, width=10, font=self.fontStyle)
        widget[num_elasticity][4].place(relx = self.block_2_TAB3_entry_1_4_x,
                                                          rely = (self.block_2_TAB3_entry_1_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w")

        self.TAB3_l7=Label(self.TAB3,text="Value1: ", font = self.fontStyle)
        self.TAB3_l7.place(relx = self.block_2_TAB3_entry_1_2_x, 
                           rely = (self.block_2_TAB3_entry_2_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))-self.text_entry_gap, anchor = "w")        
        widget[num_elasticity][5] = Entry(tab, width=10, font=self.fontStyle)
        widget[num_elasticity][5].place(relx = self.block_2_TAB3_entry_1_2_x,
                                                          rely = (self.block_2_TAB3_entry_2_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w")
        self.TAB3_l8=Label(self.TAB3,text="Value2: ", font = self.fontStyle)
        self.TAB3_l8.place(relx = self.block_2_TAB3_entry_1_3_x,
                           rely = (self.block_2_TAB3_entry_2_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))-self.text_entry_gap, anchor = "w") 
        widget[num_elasticity][6] = Entry(tab, width=10, font=self.fontStyle)
        widget[num_elasticity][6].place(relx = self.block_2_TAB3_entry_1_3_x,
                                                          rely = (self.block_2_TAB3_entry_2_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w")
        self.TAB3_l9=Label(self.TAB3,text="Value3: ", font = self.fontStyle)
        self.TAB3_l9.place(relx = self.block_2_TAB3_entry_1_4_x,
                           rely = (self.block_2_TAB3_entry_2_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))-self.text_entry_gap, anchor = "w")        
        widget[num_elasticity][7] = Entry(tab, width=10, font=self.fontStyle)
        widget[num_elasticity][7].place(relx = self.block_2_TAB3_entry_1_4_x,
                                                          rely = (self.block_2_TAB3_entry_2_1_y+
                                2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y)), anchor = "w")
        
        #print("create widget: ",widget[num_elasticity][7].get())
        #print("create self: ", self.elasticity_widget_dict[tax_type][num_elasticity][7].get())
        num_elasticity += 1
        self.button_2_TAB3_pos_y = (self.block_2_TAB3_entry_1_1_y+2*(num_elasticity-1)*(self.block_2_TAB3_entry_entry_gap_y))+self.entry_button_gap        
        self.button_generate_elasticity_dict[tax_type].place(relx = self.button_2_TAB3_pos_x,
                                            rely = self.button_2_TAB3_pos_y, anchor = "w")
        #print('selected_dict after', selected_dict)        
        self.elasticity_widget_dict[tax_type] = widget
        self.num_elasticity_changes[tax_type] = num_elasticity
        #self.elasticity_selected_dict[tax_type] = selected_dict
    
    def clicked_generate_elasticity_dict(self, selected_dict, widget, tax_type):
        #Capture the latest Reform Selection
        #print("clicked: ", self.elasticity_widget_dict[tax_type][2][7].get())
        print('num reforms in clicked_generate_elasticity_dict', self.num_elasticity_changes[tax_type])          

        adjusted_dict={}
        adj_num = 1
        for num in range(1, self.num_elasticity_changes[tax_type]):
            adjusted_dict[adj_num]={}
            adjusted_dict[adj_num+1] = {}
            print('num in clicked_generate_elasticity_dict', num)            
            adjusted_dict[adj_num]['selected_item'] = widget[num][1].get() + '_value'
            adjusted_dict[adj_num]['selected_value'] = [widget[num][5].get(),
                                                    widget[num][6].get(),
                                                    widget[num][7].get()]
            adjusted_dict[adj_num]['selected_year'] = selected_dict[num]['selected_year']
            adjusted_dict[adj_num+1]['selected_item'] = widget[num][1].get() + '_threshold'
            adjusted_dict[adj_num+1]['selected_value'] = [widget[num][2].get(),
                                                      widget[num][3].get(),
                                                      widget[num][4].get()]          
            adjusted_dict[adj_num+1]['selected_year'] = selected_dict[num]['selected_year']
            adj_num = adj_num+2
            print('adjusted_dict in clicked_generate_elasticity_dict', adjusted_dict)       
        print("final adjusted_dict in clicked generate elasticity dict: ", adjusted_dict)
        with open(tax_type+'_elasticity_selection.json', 'w') as f:
            json.dump(adjusted_dict, f)
            
    # --- main ---
    
 
def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.geometry('1000x600')
    root.title("World Bank Microsimulation Model")
    root.state('zoomed')
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

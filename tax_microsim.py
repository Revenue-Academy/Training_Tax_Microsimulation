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
    from guifuncs import save_inputs, save_widget_inputs, get_inputs
    from guifuncs import get_inputs_after_saving_current_vars
    from guifuncs import get_growfactors_dict, update_grow_factors_csv
    from guifuncs import get_elasticity_dict, update_elasticity
    from gui_tab1 import tab1
    from gui_tab1 import initialize_vars
    from gui_tab1 import display_entry
    from gui_tab1 import grid_placement   
    from gui_tab2 import tab2
    from gui_tab3 import tab3
    from gui_tab3 import display_elasticity
    #from gui_tab3 import grid_placement_tab3
    from gui_tab4 import tab4
    from gui_tab4 import display_tax_expenditure   
    from gui_tab5 import tab5
    from gui_tab5 import display_distribution
    from gui_tab5 import display_distribution_table    
    from gui_tab6 import tab6
    from gui_tab6 import update_chart_list    
    from gui_tab6 import display_chart
    from gui_tab6 import get_attribute_selection
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
        self.tax_list=['pit','cit','vat']
        with open('global_vars.json', 'w') as f:
            f.write(json.dumps(self.vars, indent=2))
        
        # TAB Start
        self.block_1_title_pos_x = 0.15
        self.grid_placement(self.block_1_title_pos_x)
        self.tab1()


# Once the the tax is selected in tab1 populate the drop down lists
    def initiate_model(self, widget_var, tax_type):
        self.vars[tax_type]=widget_var.get()
        self.display_entry(widget_var, tax_type)        
        if self.vars[tax_type]:
            self.save_inputs()
            self.save_widget_inputs()
            global_vars = self.get_inputs()
            self.adjust_status()
            self.sub_directory = 'taxcalc'
            self.active_tax_list = self.find_active_taxes()
            #print('self.active_tax_list ', self.active_tax_list)
            # we currently only use one active tax. We will expand the model
            # to run on multiple taxes
            self.tax_type = self.active_tax_list[0]
            if global_vars!={}:         
                with open(self.sub_directory+'/'+global_vars['DEFAULTS_FILENAME']) as f:
                    self.current_law_policy = json.load(f)
                with open(self.sub_directory+'/'+global_vars[self.tax_type+'_records_variables_filename']) as vfile:
                    self.vardict = json.load(vfile)              
                self.ATTRIBUTE_READ_VARS = set(k for k,
                          v in self.vardict['read'].items()
                          if v['attribute'] == 'Yes')
                self.vars['attribute_vars'] = list(self.ATTRIBUTE_READ_VARS)
                self.growfactors = self.get_growfactors_dict(self.sub_directory+'/'+global_vars['GROWFACTORS_FILENAME'], self.ATTRIBUTE_READ_VARS)            
                #print('self.growfactors ', self.growfactors)
                #self.elasticity_json = self.get_elasticity_dict(self.tax_type)
                #print('self.elasticity_json ', self.elasticity_json)
            
            else:
                self.current_law_policy={}
                self.growfactors = {}
                self.elasticity_json = {}
            #print(vars)
            #self.tab12()
            
            # TAB Policy
            self.tab2(self.tax_type)
            
            # TAB Behavior
            # Note that function initiate_model activates the drop down list 
            self.tab3(self.tax_type)
            
            # TAB Tax Expenditure
            self.tab4()
    
            # TAB Distribution
            self.tab5()
            
            # TAB Charts
            self.tab6()
            
            # TAB Growfactors
    
            self.tab7()      
    
            # TAB Settings
            self.tab8()
            
    
            vars=self.get_inputs()
            self.sub_directory = 'taxcalc'
            if vars!={}:           
                with open(self.sub_directory+'/'+vars['DEFAULTS_FILENAME']) as f:
                    self.current_law_policy = json.load(f)
                self.growfactors = self.get_growfactors_dict(self.sub_directory+'/'+vars['GROWFACTORS_FILENAME'], self.ATTRIBUTE_READ_VARS)
                #print(self.growfactors)
            else:
                self.current_law_policy={}
                self.growfactors = {}        
            self.block_widget_dict[1][1].config(values=self.tab_generate_revenue_policy.policy_options(self.current_law_policy))
            self.growfactors_widget_dict[1][1].config(values=self.tab_growfactors.policy_options(self.growfactors))
            #self.elasticity_widget_dict[1][1].config(values=self.tab_elasticity.policy_options(self.elasticity_json))
            
        
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
        #print('Old filename is: ', widget.get())       
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        filename = filename_list[-1]
        widget.delete(0,tk.END)
        widget.insert(0,filename)
        #print(filename)
        self.vars[varname] = filename
        if (tax_type is not None) :
            #print('new filename is :', widget.get())
            if (varname=='GROWFACTORS_FILENAME'):
                if filename != old_filename:
                    self.vars[varname] = filename
                    self.entry_salary_variable[tax_type].config(values=self.show_salary_options(tax_type))
            if (varname=='DEFAULTS_FILENAME'):
                if filename != old_filename:
                    #print('file changed')
                    self.vars[varname] = filename
                    with open(self.sub_directory+'/'+filename) as f:
                        self.current_law_policy = json.load(f)                  
                    #print(self.current_law_policy)
                    self.block_widget_dict[1][1].config(values=self.tab_generate_revenue_policy.policy_options(self.current_law_policy))                    
            if (varname==tax_type+'_records_variables_filename'):            
                with open(self.sub_directory+'/'+filename) as vfile:
                    self.vardict = json.load(vfile)              
                self.ATTRIBUTE_READ_VARS = set(k for k,
                      v in self.vardict['read'].items()
                      if v['attribute'] == 'Yes')
                self.vars['attribute_vars'] = list(self.ATTRIBUTE_READ_VARS)
                
    def input_combo_data(self, event, widget, varname):
        #print("method is called")
        selected = widget.get()
        if selected.isdigit():
            self.vars[varname] = int(widget.get())
        else:
            self.vars[varname] = widget.get()
        self.save_inputs()
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

    def adjust_status(self):
        self.status['pit'] = tk.NORMAL if self.vars['pit'] else tk.DISABLED
        self.status['cit'] = tk.NORMAL if self.vars['cit'] else tk.DISABLED
        self.status['vat'] = tk.NORMAL if self.vars['vat'] else tk.DISABLED
        
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
            global_vars = self.get_inputs()
            #print('global_vars[chart_list] ', global_vars['chart_list'])
            self.tab6()
            self.chart_combo.config(values=global_vars['chart_list'])
            self.progressbar.stop()
            self.progressbar.destroy()
            self.progress_label.destroy()
            self.foo_thread.join()


    def generate_changes_dict(self, widget_dict, year_value_pairs, year_check=None, start_year=None, end_year=None, sector_widget=None):
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
                if sector_widget:
                    selected_dict[num]['selected_attribute'] = widget_dict[num][4].get()
                #print('year_value_pairs', year_value_pairs)
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
        if self.verbose:
            print('Changes to Parameters ', selected_dict)
        return selected_dict
    
    #def clicked_generate_policy_revenues(self, run_type):
    #    self.run_core_program(run_type)
    
    def clicked_generate_policy_revenues(self):
        self.run_core_program('revenue')

    def run_core_program(self, run_type):
        #Save all the GUI inputs into global_vars.json file"
        # and retrieve the saved inputs for use
        #global_vars = self.get_inputs()
        #print('before revenue table in clicked_generate_policy_revenues', global_vars['cit'+'_display_revenue_table'])        
        global_vars = self.get_inputs_after_saving_current_vars()
        if global_vars['show_error_log']:
            self.logger.clear()
        self.verbose = global_vars['verbose']
        if run_type=='dist_by_decile':
            self.vars[self.tax_type+'_display_distribution_table_bydecile'] = 1
            self.vars[self.tax_type+'_display_distribution_table_byincome'] = 0
            self.vars[self.tax_type+'_display_revenue_table'] = 0
        elif run_type=='dist_by_income':
            self.vars[self.tax_type+'_display_distribution_table_bydecile'] = 0
            self.vars[self.tax_type+'_display_distribution_table_byincome'] = 1
            self.vars[self.tax_type+'_display_revenue_table'] = 0
           
        #elif run_type == 'rev_behavior':
        else:
            self.vars[self.tax_type+'_display_distribution_table_bydecile'] = 0
            self.vars[self.tax_type+'_display_distribution_table'] = 0
            self.vars[self.tax_type+'_display_revenue_table'] = 1
            
        self.save_inputs()

        self.block_selected_dict = self.generate_changes_dict(self.block_widget_dict, 
                                                              self.year_value_pairs_policy_dict, 
                                                              year_check=1, 
                                                              start_year=global_vars['start_year'], 
                                                              end_year=global_vars['end_year'],
                                                              sector_widget=0)

        with open('reform.json', 'w') as f:
            f.write(json.dumps(self.block_selected_dict, indent=2))

        if self.verbose:
            print('Reform dictionary: ', self.block_selected_dict)
        
        if global_vars[self.tax_type+'_adjust_behavior']:
            self.elasticity_selected_dict = self.generate_changes_dict(self.elasticity_widget_dict, 
                                                                    self.year_value_pairs_elasticity_dict, 
                                                                    year_check=0, sector_widget=0)       
            #print('self.elasticity_selected_dict ', self.elasticity_selected_dict)
            self.update_elasticity(self.elasticity_json, self.elasticity_selected_dict,
                       'threshold', 'value', 
                        self.sub_directory+'/'+self.tax_type+'_elasticity_selection.json')
            if self.verbose:
                print('Elasticity Changes Dictionary: ', self.elasticity_selected_dict)
        if (len(self.attribute_columns)==0):
            sector_widget=0
        else:
            sector_widget=1
        self.growfactors_selected_dict = self.generate_changes_dict(self.growfactors_widget_dict, 
                                                                    self.year_value_pairs_growfactors_dict, 
                                                                    year_check=0, sector_widget=sector_widget)

        if self.verbose:      
            print("Growfactors Changes Dictionary ",self.growfactors_selected_dict)            

        self.update_grow_factors_csv(self.growfactors, self.growfactors_selected_dict,
                               'Year', 'Value', 
                                self.sub_directory+'/'+global_vars['GROWFACTORS_FILENAME'])
        
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
        vars = self.get_inputs_after_saving_current_vars()
        if vars['show_error_log']:
            self.logger.clear()
        self.verbose = vars['verbose']
        progress_bar = Progress_Bar(self.master)
        self.progressbar, self.progress_label = progress_bar.progressbar
        from generate_tax_expenditures import generate_tax_expenditures  
        self.foo_thread = Thread(target=generate_tax_expenditures)
        self.foo_thread.daemon = True
        self.progressbar.start(interval=10)
        self.foo_thread.start()
        self.master.after(20, self.check_thread)

    def clicked_generate_distribution(self, run_type):        
        self.run_core_program(run_type)
            
    def clicked_display_charts(self):
        pass
    

    
 
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

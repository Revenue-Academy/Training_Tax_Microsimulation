# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:06:26 2022

@author: wb305167
"""
import json
import pandas as pd
import numpy as np
import csv

def save_inputs(self):  
    with open('global_vars.json', 'w') as f:        
        f.write(json.dumps(self.vars, indent=2))
        
def save_widget_inputs(self):
    tax_list = []
    if self.vars['pit']:
        tax_list = tax_list + ['pit']
    if self.vars['cit']:
        tax_list = tax_list + ['cit']
    if self.vars['vat']:
        tax_list = tax_list + ['vat']
    tax_type = tax_list[0]    
    widget_list = [self.entry_data_filename[tax_type], self.entry_weights_filename[tax_type],
                   self.entry_records_filename[tax_type], self.entry_policy_filename[tax_type],
                   self.entry_growfactors_filename[tax_type], self.entry_functions_filename[tax_type],
                   self.entry_functions_names_filename[tax_type], self.entry_salary_variable[tax_type],
                   self.entry_start_year[tax_type], self.entry_end_year[tax_type]]    

    varlist = [tax_type+'_data_filename', tax_type+'_weights_filename',
                   tax_type+'_records_variables_filename', 'DEFAULTS_FILENAME',
                   'GROWFACTORS_FILENAME', tax_type+'_functions_filename',
                   tax_type+'_functions_names_filename', 'SALARY_VARIABLE',
                   'start_year', 'end_year']
    i=0
    for widget in widget_list:
        self.vars[varlist[i]] = widget.get()
        i=i+1    
    with open('global_vars.json', 'w') as f:        
        f.write(json.dumps(self.vars, indent=2))
        
def get_inputs_after_saving_current_vars(self):
    save_widget_inputs(self)
    f = open('global_vars.json')
    vars = json.load(f)
    return vars

def get_inputs(self):
    f = open('global_vars.json')
    vars = json.load(f)
    return vars

def get_growfactors_dict(self, filename, ATTRIBUTE_READ_VARS):
    def make_sub_dict(df):
        #print(df.columns)
        subdict={}
        for j in range(1, len(df.columns)):
            subdict['_'+df.columns[j]] = {}
            year_list = []
            value_list = []
            for i in range(0, len(df)):
                year_list = year_list + [df.iloc[i,0]]
                value_list = value_list + [df.iloc[i,j]]      
            subdict['_'+df.columns[j]][df.columns[0]] = year_list
            subdict['_'+df.columns[j]]['Value'] = value_list
        return subdict

    df = pd.read_csv(filename)
    # shift column 'Year' to first position
    first_column = df.pop('Year')     
    df.insert(0, 'Year', first_column)   
    self.attribute_columns = list(ATTRIBUTE_READ_VARS.intersection(set(df.columns)))
    self.gf_columns_all = list(df.columns)   
    if (len(self.attribute_columns)==0):
        mydict = make_sub_dict(df)
        self.attribute_types=[]
    else:     
        self.attribute_types = list(set(df[self.attribute_columns[0]]))
        self.gf_columns_all.remove(self.attribute_columns[0])
        mydict={}
        for val in self.attribute_types:
            subdict = make_sub_dict(df[df[self.attribute_columns[0]]==val][self.gf_columns_all])
            mydict[val] = subdict
    #print('mydict ', mydict)
    return mydict

def make_grow_factors_csv(mydict, index, value, filename):  
    output_dict={}
    output_dict[index] = mydict[list(mydict.keys())[0]][index]
    for k in mydict.keys():
        output_dict[k[1:]] = mydict[k][value]
    with open(filename, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(output_dict.keys())
        transposed_values = (np.array(list(output_dict.values())).T).tolist()
        for i in range(len(transposed_values)):
            w.writerow(transposed_values[i])
        
def update_grow_factors_csv(self, mydict, update_dict, field_year, field_value, filename):    
    print('update_dict ', update_dict)
    if len(update_dict)>0:
        for i in range(1, len(update_dict)+1):
            k = '_' + update_dict[i]['selected_item']
            v = update_dict[i]['selected_value']
            mydict[k][field_value]=v
        #print('mydict ', mydict)
        output_dict={}
        output_dict[field_year] = mydict[list(mydict.keys())[0]][field_year]
        for k in mydict.keys():
            output_dict[k[1:]] = mydict[k][field_value]
        #print('output_dict ', output_dict)
        with open(filename, 'w', newline='') as f:
             w = csv.writer(f)
             w.writerow(output_dict.keys())
             transposed_values = (np.array(list(output_dict.values())).T).tolist()
             for i in range(len(transposed_values)):
                 w.writerow(transposed_values[i])   
    
    
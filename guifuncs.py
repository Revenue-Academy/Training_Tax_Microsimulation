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
    self.vars = self.get_inputs()
    #print('self.vars', self.vars)
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
                   'start_year', 'end_year', 'pit_distribution_table',
                   'cit_distribution_table', 'vat_distribution_table']
    i=0
    for widget in widget_list:
        self.vars[varlist[i]] = widget.get()
        i=i+1    
    self.save_inputs()

"""
def save_distribution_inputs(self):
    self.vars = self.get_inputs()
                   self.pit_distribution_chk, self.cit_distribution_chk,
                   self.vat_distribution_chk
"""
                   
def get_inputs_after_saving_current_vars(self):
    self.save_inputs()
    save_widget_inputs(self)
    f = open('global_vars.json')
    global_vars = json.load(f)
    return global_vars

def get_inputs(self):
    f = open('global_vars.json')
    global_vars = json.load(f)
    return global_vars

def get_elasticity_dict(self, tax_type):
    with open(self.sub_directory+'/'+self.vars['DEFAULTS_FILENAME']) as f:
        current_law_policy = json.load(f)
    #current_law_policy_sorted = dict(sorted(current_law_policy.items()))
    elasticity_dict={}
    elasticity_items_list = []
    for k, s in current_law_policy.items():
        if (k[1:11] == 'elasticity'):
            if (k[-5:] == 'value'):
                item = k[1:-6]
                k1 = k[:-6]
                elasticity_dict[k1] = {}
                elasticity_dict[k1]['item'] = item
                elasticity_dict[k1]['value']= [current_law_policy[k]['value'][0][0],
                                              current_law_policy[k]['value'][0][1],
                                              current_law_policy[k]['value'][0][2]]
                
                #elasticity_dict[k1]['year']= current_law_policy[k]['row_label'][0]
                elasticity_dict[k1]['year']= self.vars['start_year']
                
                v = k[:-6]+'_threshold'
                elasticity_dict[k1]['threshold']= [current_law_policy[v]['value'][0][0],
                                                  current_law_policy[v]['value'][0][1],
                                                  current_law_policy[v]['value'][0][2]]

                elasticity_items_list = elasticity_items_list + [item]     
    return elasticity_dict

def update_elasticity(self, mydict, update_dict, field_param, field_value, filename):
    output_dict={}
    if len(update_dict)>0:
        for i in range(1, len(update_dict)+1):
            k = '_' + update_dict[i]['selected_item']
            v = update_dict[i]['selected_value']
            mydict[k][field_value]=v
        i=1
        for k,v in mydict.items():
            k1 = k+'_value'
            output_dict[str(i)]={}
            k2 = k+'_threshold'
            output_dict[str(i+1)]={}         
            output_dict[str(i)]['selected_item'] = k1[1:]
            output_dict[str(i)]['selected_value'] = [mydict[k][field_value]]
            output_dict[str(i)]['selected_year'] = [mydict[k]['year']]
            output_dict[str(i+1)]['selected_item'] = k2[1:]       
            output_dict[str(i+1)]['selected_value'] = [mydict[k][field_param]]
            output_dict[str(i+1)]['selected_year'] = [mydict[k]['year']]
            i=i+2
    with open(filename, 'w') as f:
        f.write(json.dumps(output_dict, indent=2))      
            
    
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
        
def update_grow_factors_csv(self, mydict, update_dict, field_param, field_value, filename):    
    def update_values(mydict, k, field_param, field_value, v_year, v_value):
        j=0    
        for i in range(len(mydict[k][field_param])-1):           
            if j==(len(v_year)-1):
                #print("I am here")
                break
            if (int(v_year[j]) == int(mydict[k][field_param][i])):             
                mydict[k][field_value][i]=v_value[j]
                j=j+1
        return mydict
    if len(update_dict)>0:
        for i in range(1, len(update_dict)+1):
            k = '_' + update_dict[i]['selected_item']
            v_year = update_dict[i]['selected_year']
            v_value = update_dict[i]['selected_value']  
            if len(self.attribute_columns)>0:
                attribute_value = update_dict[i]['selected_attribute']
                mydict[attribute_value] = update_values(mydict[attribute_value], 
                                                        k, field_param, field_value, 
                                                        v_year, v_value)                
            else: # update values only from start_year to end_year
                mydict = update_values(mydict, k, field_param, field_value, 
                                       v_year, v_value)
        output_dict={}
        if len(self.attribute_columns)>0:
            first_level_keys = list(mydict.keys())
            second_level_keys = list(mydict[first_level_keys[0]].keys())
            for i in first_level_keys:
                output_dict[i] = {}
                for j in second_level_keys:
                    field_year_val = mydict[i][j][field_param]
                    output_dict[i][field_param] = field_year_val
                    output_dict[i][j[1:]] = mydict[i][j][field_value]
            second_level_keys1 = [i[1:] for i in second_level_keys]
            with open(filename, 'w', newline='') as f:
                 w = csv.writer(f)
                 cols = [self.attribute_columns[0]]+[field_param]+second_level_keys1
                 w.writerow(cols)
                 for i in first_level_keys:
                     transposed_values = (np.array(list(output_dict[i].values())).T).tolist()
                     for j in range(len(transposed_values)):
                         w.writerow([i]+transposed_values[j])                   
        else:
            output_dict[field_param] = mydict[list(mydict.keys())[0]][field_param]
            for k in mydict.keys():
                output_dict[k[1:]] = mydict[k][field_value]
            with open(filename, 'w', newline='') as f:
             w = csv.writer(f)
             w.writerow(output_dict.keys())
             transposed_values = (np.array(list(output_dict.values())).T).tolist()
             for i in range(len(transposed_values)):
                 w.writerow(transposed_values[i])   
    
    
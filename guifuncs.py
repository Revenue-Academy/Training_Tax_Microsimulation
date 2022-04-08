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
        
def get_inputs_after_saving_current_vars(self):
    save_inputs(self)
    f = open('global_vars.json')
    vars = json.load(f)
    return vars

def get_inputs(self):
    f = open('global_vars.json')
    vars = json.load(f)
    return vars

def get_growfactors_dict(self, filename):
    df = pd.read_csv(filename)
    mydict={}
    for j in range(1, len(df.columns)):
        mydict['_'+df.columns[j]] = {}
        year_list = []
        value_list = []
        for i in range(1, len(df)):
            year_list = year_list + [df.iloc[i,0]]
            value_list = value_list + [df.iloc[i,j]]      
        mydict['_'+df.columns[j]][df.columns[0]] = year_list
        mydict['_'+df.columns[j]]['Value'] = value_list
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
        
   
    
    
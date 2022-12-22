# -*- coding: utf-8 -*-
"""

@author: jsimonov@worldbank.org

AUTOMATIC CREATION OF JSON FILES FROM FUNCTION TXT FILE, WEIGHTS AND GROWTH FACTORS FILES FOR MICROSIMULATION MODEL


In order for this script to be able to create the 6-files listed below, it is necessary to create the following files beforehand, which will then be imported inside, including:

    - Function files( In txt version)
    - Sample file 

After executing this script the following files will be created: JSON functions names,JSON with records variable, JSON with current law policy , CSV with weights, CSV growth factors


Steps in executing the script:    

1. Setting path, country name and type of tax
2. Creating JSON file with functions names
3. Creating JSON file with records variable
4. Creating JSON file current law policy
5. Creating table with weights 
6. Creating table with growth factors

"""

# In[1]: Setting path and import TXT file created from file with functions

# Setting country name and type of tax
import_name_country = 'macedonia'
type_of_tax = 'cit'

# Setting time horizont for tables with weights and growth factors
initial_year=2021
last_year=2030

import os
import numpy as np
import pandas as pd
from pathlib import Path
import json
import ast

os.getcwd()
os.listdir()

os.chdir('C:/Users/User/Documents/WB/CIT/CIT_FINAL_MODEL/Automatic creation files/')

file_reader = open('C:/Users/User/Documents/WB/CIT/CIT_FINAL_MODEL/Automatic creation files/functions_cit_macedonia.txt')   
os.getcwd()

# In[0]: Extract function names and arguments from function files

# Import file in string format
with open ('functions_cit_macedonia.txt', 'r') as txtFile:
       text = txtFile.read()

def get_names_and_functions(text):
    root = ast.parse(text)
    for node in ast.walk(root):
        if isinstance(node, ast.FunctionDef):
            yield node.name
            for arg in node.args.args:
                yield arg.arg
        elif isinstance(node, ast.Name):
            yield node.id

found = set(get_names_and_functions(text))

VariablesNames = list(found)

# Remove predifiend words: e.g min, max
VariablesNames.remove('iterate_jit')

# Extract in text format
f = open("VariablesNames.txt", "w")
for item in VariablesNames:
   f.write(item + "\n")
f.close()

# In[2]: Extracting names of functions from TXT file and create a new JSON file for microsimulation model

os.chdir('C:/Users/User/Documents/WB/CIT/CIT_FINAL_MODEL/Automatic creation files/')
file_reader = open('C:/Users/User/Documents/WB/CIT/CIT_FINAL_MODEL/Automatic creation files/VariablesNames.txt')   
os.getcwd()

def extractng_functions_names():
    names = Path('VariablesNames.txt').read_text().strip().split("\n")   # split(",\n") Separator with comma
    names = {x for x in names if x.startswith("fun_")}
    names_dict = {index: name for index, name in enumerate(names)}
    with open(f'function_names_{type_of_tax}_{import_name_country}.json',"w") as file:
        json.dump(names_dict, file, indent=4)

# Executing the created function
extractng_functions_names()

# In[3] Extracting names of variables from TXT file and create a new JSON with records variablse for microsimulation model

def extracting_records_variable_names():
    names = Path('VariablesNames.txt').read_text().strip().split("\n")
    attributes = {
        "type": "float",
        "desc": " ",
        "form": {"2019": " "},
        "cross_year": "No",
        "attribute": "No"
    }
    read_names = {
        "id_n": {
            "required": True,
            "type": "int",
            "desc": " ",
            "form": {"2021": " "},
            "cross_year": "No",
            "attribute": "No"
            },
        "Year": {
            "required": True,
            "type": "int",
            "desc": "Assessment Year",
            "form": {"2021": "private info"},
            "cross_year": "No",
            "attribute": "No"
            },
        }
    read_names.update({x: attributes for x in names if x.endswith("_r")})
    calc_names = {x: attributes for x in names if x.endswith("_calc")}
    names_dict = {"read": read_names, "calc": calc_names}
    with open(f'records_variables_{type_of_tax}_{import_name_country}.json', "w") as file: # Stack prasanje
        json.dump(names_dict, file, indent=4)

# Executing the created function
extracting_records_variable_names()


# In[4] Extracting names of variables from TXT file and create a new JSON with current law policy variables for microsimulation model

def extracting_current_law_variable_names():
    names = Path('VariablesNames.txt').read_text().strip().split("\n")
    attributes =  {
        "long_name": " ",
        "description": " ",
        "itr_ref": " ",
        "notes": "",
        "row_var": "AYEAR",
        "row_label": ["2021"],
        "start_year": 2021,
        "cpi_inflatable": False,
        "cpi_inflated": False,
        "col_var": "",
        "col_label": "",
        "boolean_value": False,
        "integer_value": False,
        "value": [0.10],
        "range": {"min": 0, "max": 1},
        "out_of_range_minmsg": "",
        "out_of_range_minmsg": "",
        "out_of_range_maxmsg": "",
        "out_of_range_action": "stop"
    }
    read_names = {f"_{x}": attributes for x in names if "_" not in x}
    with open(f'current_law_policy_{type_of_tax}_{import_name_country}.json', "w") as file:
        json.dump(read_names, file, indent=4)

# Executing the created function
'Attention: Due to the different values of current law policy variables, it is not possible to set them in advance. Because of this, a default value of 0.1 is set'
extracting_current_law_variable_names()

# In[5] Extracting weights from the sample and creating a new separate file with weights for the microsimulation model

filename= "C:/Users/User/Documents/WB/CIT/CIT_FINAL_MODEL/Automatic creation files/cit_data_macedonia1.csv"
df_cit_sample=pd.read_csv(filename)

# Extract columns with title weights
weights=df_cit_sample['weight']

# Create a table
df_weights=pd.DataFrame(columns=range(initial_year,last_year+1)).add_prefix('WT')

# fill first column with range of values
df_weights.iloc[:,0]= weights

# Populated all columns with weights
df_weights=df_weights.ffill(axis=1)

# Export CSV file with weights
df_weights.to_csv(f'{type_of_tax}_weights_{import_name_country}.csv',index=False)

# In[6] Creating table with growth factors

# Extract names from sample
listName=list(df_cit_sample.columns)

# Remove unnecessary columns
to_remove = ['Unnamed: 0','index','id_n','nace','bin','weight']
filteredlistName = [x for x in listName if x not in to_remove]
	
# Fixed first two columns names
cols = ['CPI', 'SALARY']

# Creating table
growfactors_df = (pd.DataFrame({'Year': range(initial_year, last_year+1)})
        .reindex(columns=['Year']+cols+filteredlistName, fill_value=1))

# Export CSV file with growth factors
growfactors_df.to_csv(f'growfactors_{type_of_tax}_{import_name_country}.csv',index=False)

# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 22:58:13 2022

@author: wb305167
"""
import json


#add/edit parameter to json file and saves it under a new name
def add_parameter(json_filename):
    with open(json_filename) as vfile:
        vardict = json.load(vfile)
        vfile.close()     
    for x, y in vardict["read"].items():
      #print("key: ", x, "value: ", y)
      print(vardict["read"][x])
      vardict["read"][x]["cross_year"]='No'
      vardict["read"][x]["attribute"]='No'
      for p, q in y.items():
          print("second level key: ", p, "second level value: ", q)
        
    with open(json_filename, 'w') as f:
        f.write(json.dumps(vardict, indent=2))

#add/edit parameter to policy json file
def edit_parameter(json_filename):
    newdict={}
    with open(json_filename) as vfile:
        vardict = json.load(vfile)
        vfile.close() 
    for x, y in vardict.items():
      newdict[x] = y
      #print("key: ", x, "value: ", y)
      print(x)
      if x[1:11] !='elasticity':
          print(newdict[x]["col_var"])
          print(newdict[x]["col_label"])
          newdict[x]["col_var"]='Value'
          newdict[x]["col_label"]=['Value']
    with open(json_filename[:-5]+"1"+".json", 'w') as f:
        f.write(json.dumps(newdict, indent=2))

        
def make_functions_dict():
    func_list = ['Net_accounting_profit', 'Total_additions_to_GP',
                 'Total_taxable_profit','Op_WDV_depr','Tax_depr_Bld', 
                 'Tax_depr_Intang','Tax_depr_Mach','Tax_depr_Others', 
                 'Tax_depr_Comp',  'Tax_depreciation', 'Cl_WDV_depr',
                 'Total_deductions','Net_taxable_profit', 
                 'Net_taxable_profit_behavior',  'Donations_allowed',
                 'Carried_forward_losses', 'Tax_base_CF_losses', 
                 'Net_tax_base','Net_tax_base_Egyp_Pounds',  'cit_liability']
    
    func_dict = {}
    for i in range(len(func_list)):
        func_dict[i] = func_list[i]
    with open('taxcalc/cit_function_names_egypt.json', 'w') as f:
        f.write(json.dumps(func_dict, indent=2))
    return func_dict


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
    func_list = ['calc_EmpInc','calc_BussInc','calc_InvestIncome','calc_OtherIncome',
                 'calc_AssessibleIncome','calc_ReliefEmpIncome','calc_ReliefForeignIncome',
                 'calc_ReliefRentalIncome','calc_ReliefInterestIncome','calc_PersonalRelief',
                 'calc_TotalRelief','calc_QualifyingPaymentAllowed','calc_TotalDudAsseIncome',
                 'calc_TaxableIncome','calc_TaxTerminalBenefit','calc_TaxIncomeBetting',
                 'calc_CapitalGains','calc_BalanceIncome','calc_BalanceIncomeProgressive',
                 'calc_tti_behavior','calc_pit_progressive','calc_TotalTaxPayable']
    
    func_dict = {}
    for i in range(len(func_list)):
        func_dict[i] = func_list[i]
    with open('taxcalc/function_names_srilanka.json', 'w') as f:
        f.write(json.dumps(func_dict, indent=2))
    return func_dict


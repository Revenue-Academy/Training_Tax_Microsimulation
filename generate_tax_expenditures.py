# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:28:24 2021

@author: wb305167
"""
import copy
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
from datetime import datetime

#from taxcalc import *
from taxcalc.utils import *
from taxcalc.display_funcs import *
from PIL import Image,ImageTk


def make_float(item):
    if isinstance(item, list):
        return [float(x) for x in item]
    else:
        return float(item)
    
def read_reform_dict(block_selected_dict):
    #print('block_selected_dict in read_reform_dict: ',block_selected_dict)
    years=[]
    for k in block_selected_dict.keys():
        if (block_selected_dict[k]['selected_year'] not in years):
            years = years + [block_selected_dict[k]['selected_year'][0]]
    ref = {}
    ref['policy']={}
    #print(' years ', years)
    for year in years:
        policy_dict = {}
        for k in block_selected_dict.keys():
            #print('block_selected_dict.keys() ', k)
            if block_selected_dict[k]['selected_year'][0]==year:
                policy_dict['_'+block_selected_dict[k]['selected_item']]=[make_float(block_selected_dict[k]['selected_value'][0])]
        ref['policy'][int(year)] = policy_dict
    years = [int(x) for x in years]
    years.sort()
    return years, ref

def concat_dicts(block_selected_dict, elasticity_dict):
    years=[]
    max = 0
    for k in block_selected_dict.keys():
        if int(k) > max:
            max = int(k)
    for i in range(1,len(elasticity_dict)+1):
        block_selected_dict[str(max+i)] = elasticity_dict[str(i)]
    #ref = {}
    return block_selected_dict

def write_file(df, text_data, filename, window=None, footer_row_num=None):
    df.to_csv(filename+'.csv', mode='w')
    # a = open(filename+'.csv','w')
    # a.write("\n")
    # a.write("\n")
    # a.close
    with open(filename+'.txt','w') as f:
        f.write(text_data)
    f.close
    if (window is not None) and (footer_row_num is not None):
        footer = ["footer", "*Data saved in file "+ filename]
        display_table(window, data=footer, footer=footer_row_num+2)
    
def weighted_total_tax(calc, tax_list, category, year, tax_dict, gdp=None, attribute_var = None):
    for tax_type in tax_list:
        tax_dict[tax_type][year][category] = {}
        tax_dict[tax_type][year][category]['value'] = calc.weighted_total_tax_dict(tax_type, tax_type+'ax')       

        tax_dict[tax_type][year][category]['value_bill'] = {}
        tax_dict[tax_type][year][category]['value_bill_str'] = {}
        if gdp is not None:
            tax_dict[tax_type][year][category]['value_gdp'] = {}
            tax_dict[tax_type][year][category]['value_gdp_str'] = {}        
        for k in tax_dict[tax_type][year][category]['value'].keys():
            tax_dict[tax_type][year][category]['value_bill'][k] = tax_dict[tax_type][year][category]['value'][k]/10**9
            tax_dict[tax_type][year][category]['value_bill_str'][k] = '{0:.2f}'.format(tax_dict[tax_type][year][category]['value_bill'][k])        
            if gdp is not None:
                tax_dict[tax_type][year][category]['value_gdp'][k] = ((tax_dict[tax_type][year][category]['value'][k]/10**9)/gdp[str(year)])*100
                tax_dict[tax_type][year][category]['value_gdp_str'][k] = '{0:.2f}'.format(tax_dict[tax_type][year][category]['value_gdp'][k])  
    #print('tax_dict ', tax_dict)
    return tax_dict
       
def weighted_total_tax_diff(tax_list, category1, category2, year, tax_dict, gdp=None, attribute_var = None):
    for tax_type in tax_list:
        tax_dict[tax_type][year][category2]['value_bill_diff'] = {}
        tax_dict[tax_type][year][category2]['value_bill_diff_str'] = {}
        if gdp is not None:
            tax_dict[tax_type][year][category2]['value_diff_gdp'] = {}
            tax_dict[tax_type][year][category2]['value_diff_gdp_str'] = {}
        for k in tax_dict[tax_type][year][category1]['value_bill'].keys():
            tax_dict[tax_type][year][category2]['value_bill_diff'][k] = (tax_dict[tax_type][year][category2]['value_bill'][k] -
                                                                  tax_dict[tax_type][year][category1]['value_bill'][k])
            tax_dict[tax_type][year][category2]['value_bill_diff_str'][k] = '{0:.2f}'.format(tax_dict[tax_type][year][category2]['value_bill_diff'][k])
            if gdp is not None:
                tax_dict[tax_type][year][category2]['value_diff_gdp'][k] = ((tax_dict[tax_type][year][category2]['value_bill'][k] -
                                                                  tax_dict[tax_type][year][category1]['value_bill'][k])/gdp[str(year)])*100
                tax_dict[tax_type][year][category2]['value_diff_gdp_str'][k] = '{0:.2f}'.format(tax_dict[tax_type][year][category2]['value_diff_gdp'][k])                
    return tax_dict

def screen_print(tax_list, category, year, tax_dict, item, item_desc):
    for tax_type in tax_list:
        print("The "+tax_type.upper()+" "+item_desc+" in billions is: ", tax_dict[tax_type][year][category][item]['All'])

    
def generate_tax_expenditures():
    from taxcalc.growfactors import GrowFactors
    from taxcalc.policy import Policy
    from taxcalc.records import Records
    from taxcalc.gstrecords import GSTRecords
    from taxcalc.corprecords import CorpRecords
    from taxcalc.parameters import ParametersBase
    from taxcalc.calculator import Calculator
    from taxcalc.utils import dist_variables

    f = open('global_vars.json')
    global_variables = json.load(f)
    #print('global_variables in generate policy revenues ', global_variables)
    verbose = global_variables['verbose']
    start_year = int(global_variables['start_year'])
    end_year = int(global_variables['end_year'])
    data_start_year = int(global_variables['data_start_year'])
    attribute_varlist = global_variables['attribute_vars']
    percent_gdp=global_variables['percent_gdp']
    if percent_gdp==0:
        GDP_Nominal = None
    else:
        GDP_Nominal = global_variables['GDP_Nominal']       
    #print('display_revenue_table in generate policy revenues ',global_variables['cit'+'_display_revenue_table'])
    if len(attribute_varlist)==0: 
        attribute_var = None
    else:
        attribute_var = attribute_varlist[0]
    tax_list=[]
    tax_collection_var_list = []
    id_varlist = []
    # start the simulation for pit/cit/vat    
    if global_variables['pit']:
        tax_list = tax_list + ['pit']
        tax_collection_var_list = tax_collection_var_list + ['pitax']
        id_varlist = id_varlist + [global_variables['pit_id_var']]        
        recs = Records(data=global_variables['pit_data_filename'], weights=global_variables['pit_weights_filename'], gfactors=GrowFactors(growfactors_filename=global_variables['GROWFACTORS_FILENAME']))
    else:
        recs = None
    if global_variables['cit']:
        tax_list = tax_list + ['cit']
        tax_collection_var_list = tax_collection_var_list + ['citax']
        id_varlist = id_varlist + [global_variables['cit_id_var']]        
        crecs = CorpRecords(data=global_variables['cit_data_filename'], weights=global_variables['cit_weights_filename'], gfactors=GrowFactors(growfactors_filename=global_variables['GROWFACTORS_FILENAME']))
    else:
        crecs = None
    if global_variables['vat']:
        tax_list = tax_list + ['vat']
        tax_collection_var_list = tax_collection_var_list + ['vatax']
        id_varlist = id_varlist + [global_variables['vat_id_var']]         
        grecs = GSTRecords(data=global_variables['vat_data_filename'], weights=global_variables['vat_weights_filename'], gfactors=GrowFactors(growfactors_filename=global_variables['GROWFACTORS_FILENAME']))
    else:
        grecs = None
    
    # create Policy object containing current-law policy
    pol = Policy(DEFAULTS_FILENAME=global_variables['DEFAULTS_FILENAME'])
    
    # specify Calculator objects for current-law policy
    calc1 = Calculator(policy=pol, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)    
    assert isinstance(calc1, Calculator)
    assert calc1.current_year == data_start_year

    data_row = {}
    row_num = {}
    window_dict={}
    revenue_dict0={}
    revenue_dict={}
    for tax_type in tax_list:
        revenue_dict[tax_type]={} 
        for year in range(start_year, start_year+1):
            revenue_dict[tax_type][year]={}
        window_dict[tax_type] = tk.Toplevel()
        window_dict[tax_type].geometry("800x600+600+140")            
        #display_table(window, header=True)
        # Adjust this for number of years selected
        header = ["header","Tax Incentive", "Current Law", "Benchmark", "Tax Expenditure"]
        title_header = [["title", tax_type.upper()+" Expenditure (billions)"],
                        header]
        if percent_gdp:
            title_header = [["title", tax_type.upper()+" Expenditure (% of GDP)"],
                        header]
        row_num[tax_type] = display_table(window_dict[tax_type], data=title_header, header=True)
    
    calc1.advance_to_year(start_year)
    calc1.calc_all()    
    revenue_dict0 = weighted_total_tax(calc1, tax_list, 'current_law', year, revenue_dict, GDP_Nominal, attribute_var)
    np.seterr(divide='ignore', invalid='ignore')
    #pol2 = Policy()
    reform = Calculator.read_json_param_objects(global_variables['pit_benchmark_filename'], None)    
    ref_dict = reform['policy']
    var_list = []
    tax_expenditure_var_list = []
    year=start_year
    for pkey, sdict in ref_dict.items():
            #print(f'pkey: {pkey}')
            #print(f'sdict: {sdict}')
            for k, s in sdict.items():
                reform.pop("policy")
                mydict={}
                mydict[k]=s
                mydict0={}
                mydict0[pkey]=mydict
                reform['policy']=mydict0
                #print('reform:', reform)
                #print(f'k: {k}')
                #print(f's: {s}')
                pol2 = Policy()
                pol2.implement_reform(reform['policy'])
                calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)
                calc2.advance_to_year(start_year)
                calc2.calc_all()
                revenue_dict = weighted_total_tax(calc2, tax_list, 'reform', year, revenue_dict0, GDP_Nominal, attribute_var)                    
                revenue_dict = weighted_total_tax_diff(tax_list, 'current_law', 'reform', year, revenue_dict, GDP_Nominal, attribute_var)
                for tax_type in tax_list:
                    if percent_gdp:
                        data_row[tax_type] = [k[1:], revenue_dict[tax_type][year]['current_law']['value_gdp_str']['All'], 
                                          revenue_dict[tax_type][year]['reform']['value_gdp_str']['All'], 
                                          revenue_dict[tax_type][year]['reform']['value_diff_gdp_str']['All']]                     
                    else:
                        data_row[tax_type] = [k[1:], revenue_dict[tax_type][year]['current_law']['value_bill_str']['All'], 
                                          revenue_dict[tax_type][year]['reform']['value_bill_str']['All'], 
                                          revenue_dict[tax_type][year]['reform']['value_bill_diff_str']['All']]

                    row_num[tax_type] = display_table(window_dict[tax_type], 
                                                      data = data_row[tax_type], 
                                                      row = row_num[tax_type])
                    

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:45:56 2021

@author: wb305167
"""

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.font as tkfont
from taxcalc import *
from taxcalc.display_funcs import *

from PIL import Image,ImageTk

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
        
def weighted_total_tax(calc, tax_list, category, year, tax_dict):
    for tax_type in tax_list:
        tax_dict[tax_type][year][category] = {}
        if tax_type == 'pit':
            tax_dict[tax_type][year][category]['value'] = calc.weighted_total_pit(tax_type+'ax')       
        if tax_type == 'cit':
            tax_dict[tax_type][year][category]['value'] = calc.weighted_total_cit(tax_type+'ax')           
        if tax_type == 'vat':
            tax_dict[tax_type][year][category]['value'] = calc.weighted_total_gst(tax_type+'ax')

        tax_dict[tax_type][year][category]['value_bill'] =  tax_dict[tax_type][year][category]['value']/10**9
        tax_dict[tax_type][year][category]['value_bill_str'] =  '{0:.2f}'.format(tax_dict[tax_type][year][category]['value_bill'])        
    return tax_dict
       
def weighted_total_tax_diff(tax_list, category1, category2, year, tax_dict):
    for tax_type in tax_list:
        tax_dict[tax_type][year][category2]['value_bill_diff'] = (tax_dict[tax_type][year][category2]['value_bill'] -
                                                                  tax_dict[tax_type][year][category1]['value_bill'])
        tax_dict[tax_type][year][category2]['value_bill_diff_str'] = '{0:.2f}'.format(tax_dict[tax_type][year][category2]['value_bill_diff'])
    return tax_dict

def screen_print(tax_list, category, year, tax_dict, item, item_desc):
    for tax_type in tax_list:
        print("The "+tax_type.upper()+" "+item_desc+" in billions is: ", tax_dict[tax_type][year][category][item])



def generate_tax_expenditures():
    from taxcalc.growfactors import GrowFactors
    from taxcalc.policy import Policy
    from taxcalc.records import Records
    from taxcalc.gstrecords import GSTRecords
    from taxcalc.corprecords import CorpRecords
    from taxcalc.parameters import ParametersBase
    from taxcalc.calculator import Calculator
    from taxcalc.utils import dist_variables

    fontStyle = tkfont.Font(family="Helvetica", size="12")
    
    f = open('global_vars.json')
    vars = json.load(f)
    verbose = vars['verbose']
    start_year = int(vars['start_year'])
    end_year = int(vars['end_year'])
    
    tax_list=[]
    tax_collection_var_list = []  
    # start the simulation for pit/cit/vat    
    if vars['pit']:
        tax_list = tax_list + ['pit']
        tax_collection_var_list = tax_collection_var_list + ['pitax']
        recs = Records(data=vars['pit_data_filename'], weights=vars['pit_weights_filename'], gfactors=GrowFactors(growfactors_filename=vars['GROWFACTORS_FILENAME']))
        elasticity_filename = vars['pit_elasticity_filename']
    else:
        recs = None
    if vars['cit']:
        tax_list = tax_list + ['cit']
        tax_collection_var_list = tax_collection_var_list + ['citax']
        crecs = CorpRecords(data=vars['cit_data_filename'], weights=vars['cit_weights_filename'], gfactors=GrowFactors(growfactors_filename=vars['GROWFACTORS_FILENAME']))
        #print("crecs is created ")
        elasticity_filename = vars['cit_elasticity_filename']
    else:
        crecs = None
    if vars['vat']:
        tax_list = tax_list + ['vat']
        tax_collection_var_list = tax_collection_var_list + ['vatax']
        grecs = GSTRecords(data=vars['vat_data_filename'], weights=vars['vat_weights_filename'], gfactors=GrowFactors(growfactors_filename=vars['GROWFACTORS_FILENAME']))
        elasticity_filename = vars['vat_elasticity_filename']
    else:
        grecs = None  
    
    #Current Law Policy
    pol = Policy(DEFAULTS_FILENAME=vars['DEFAULTS_FILENAME'])

    # specify Calculator objects for current-law policy
    calc1 = Calculator(policy=pol, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)
    assert isinstance(calc1, Calculator)
    assert calc1.current_year == int(vars["start_year"])
    np.seterr(divide='ignore', invalid='ignore')

    # Produce DataFrame of results using cross-section
   
    dump_vars = ['Taxpayer_ID', 'Net_accounting_profit', 'Total_taxable_profit', \
                'Donations_Govt', 'Donations_allowed', 'Investment_incentive', \
                'Net_taxable_profit', 'Tax_base', 'Net_tax_base', 'citax']

    # This is the Overall Tax Expenditures
    pol2 = Policy()
    reform = Calculator.read_json_param_objects(vars['cit_benchmark_filename'], None)
    pol2.implement_reform(reform['policy'])
        
    calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)
        # popup window for the Results
    # window = tk.Toplevel()
    # window.geometry("700x600+140+140")
    # label = tk.Label(window, text="Tax Expenditures", font=fontStyle)
    # label.place(relx = 0.40, rely = 0.02)
    # s = tk.Style()
    # s.configure('my.TButton', font=fontStyle)         
    
    # total_revenue_text={}
    # reform_revenue_text={}
    # tax_expenditure_text = {}        
    revenue_dict={}
    # revenue_amount_dict = {}
    # tax_expenditure = {}
    # num = 1

    
    window_dict={}
    row_num = {}
    data_row = {}
    l_TAB3 = {}
    for tax_type in tax_list:
        revenue_dict[tax_type]={}
        for year in range(start_year, end_year+1):
            revenue_dict[tax_type][year]={}
        window_dict[tax_type] = tk.Toplevel()
        window_dict[tax_type].geometry("800x600+600+140")
        #display_table(window, header=True)
        # Adjust this for number of years selected
        header = ["header","Year", "Current Law", "Benchmark", "Tax Exp"]
        # if vars[tax_type+'_adjust_behavior']:
        #     header = header + ['Reform (Behavior)', "Diff"]
        title_header = [["title", tax_type.upper()+" Projections"], header]            
        row_num[tax_type] = display_table(window_dict[tax_type], data=title_header, header=True)
    
    for year in range(start_year, end_year+1):  
        calc1.advance_to_year(year)        
        calc2.advance_to_year(year)
        calc1.calc_all()
        # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
        #       so we can continue to use pol and recs in this script without any
        #       concern about side effects from Calculator method calls on calc1.
    
        # Produce DataFrame of results using cross-section
        
        calc2.calc_all()
         
              
        revenue_dict = weighted_total_tax(calc1, tax_list, 'current_law', year, revenue_dict)              
        if verbose:
            print(f'TAX COLLECTION FOR THE YEAR - {year} \n')        
            screen_print(tax_list, 'current_law', year, revenue_dict, 'value_bill', 'Collection')
           
        revenue_dict = weighted_total_tax(calc2, tax_list, 'reform', year, revenue_dict)
        if verbose:        
            print(f'\nTAX COLLECTION FOR THE YEAR UNDER REFORM - {year} \n')       
            screen_print(tax_list, 'reform', year, revenue_dict, 'value_bill', 'Collection')
            
        revenue_dict = weighted_total_tax_diff(tax_list, 'current_law', 'reform', year, revenue_dict)
        if verbose:        
            screen_print(tax_list, 'reform', year, revenue_dict, 'value_bill_diff', 'Collection difference under Reform')

        for tax_type in tax_list:        
            data_row[tax_type] = [str(year), revenue_dict[tax_type][year]['current_law']['value_bill_str'], 
                                  revenue_dict[tax_type][year]['reform']['value_bill_str'], 
                                  revenue_dict[tax_type][year]['reform']['value_bill_diff_str']]       
        # if adjust_behavior:
        # #redo the calculations by including behavioral adjustment
        #     calc3.advance_to_year(year)
        #     calc3.calc_all()
        #     revenue_dict = weighted_total_tax(calc3, tax_list, 'reform_behavior', year, revenue_dict)
        #     if verbose:            
        #         print(f'\nTAX COLLECTION FOR THE YEAR UNDER REFORM WITH BEHAVIOR ADJUSTMENT - {year} \n')
        #         screen_print(tax_list, 'reform_behavior', year, revenue_dict, 
        #                      'value_bill', 'Collection with Behavioral Adjustment')
            
        #     revenue_dict = weighted_total_tax_diff(tax_list, 'current_law', 'reform_behavior', year, revenue_dict)
        #     if verbose:
        #         screen_print(tax_list, 'reform_behavior', year, revenue_dict, 
        #                      'value_bill_diff',
        #                      'Collection difference with Behavioral Adjustment')
        #     for tax_type in tax_list:            
        #         data_row[tax_type] = data_row[tax_type] + [revenue_dict[tax_type][year]['reform_behavior']['value_bill_str'], 
        #                                                    revenue_dict[tax_type][year]['reform_behavior']['value_bill_diff_str']]
        for tax_type in tax_list:         
            row_num[tax_type] = display_table(window_dict[tax_type], 
                                              data = data_row[tax_type], 
                                              row = row_num[tax_type])
    
    with open('revenue_dict.json', 'w') as f:
        json.dump(revenue_dict, f)
    #save the results of each tax type in separate files
    
    df = {}
    # save the results into a csv file
    for tax_type in tax_list:
        #filename1 = 'Revenue Data_'+'_'+tax_type+'_'+date_time
        filename_taxexp = tax_type+'_tax_expenditures'
        revenue_dict_df = {}
        for k, v in revenue_dict[tax_type].items():
            revenue_dict_df[k] = {}
            revenue_dict_df[k]['current_law'] = revenue_dict[tax_type][k]['current_law']['value_bill_str']
            revenue_dict_df[k]['benchmark'] = revenue_dict[tax_type][k]['reform']['value_bill_str']
            revenue_dict_df[k]['tax_expenditure'] = revenue_dict[tax_type][k]['reform']['value_bill_diff_str']
            
        df[tax_type] = pd.DataFrame.from_dict(revenue_dict_df)   
        df_str = df[tax_type].to_string()
        df_reform = pd.DataFrame.from_dict(reform)
        df_reform_str = df_reform.to_string()
        text_output1 = df_str + '\n\n' + df_reform_str + '\n\n'
        write_file(df[tax_type], text_output1, filename_taxexp)
        last_row = row_num[tax_type]
        l_TAB3[tax_type] = tk.Button(window_dict[tax_type],
                                     text="Save Results",
                                     command=lambda: write_file(df[tax_type], 
                                                                text_output1, 
                                                                filename_taxexp, 
                                                                window_dict[tax_type], 
                                                                last_row
                                                                ))
        l_TAB3[tax_type].grid(row=row_num[tax_type]+2, column=2, pady = 10, sticky=tk.W)
    
    
            
        
       
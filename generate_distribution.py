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
    
def weighted_total_tax(calc, tax_list, category, year, tax_dict, attribute_var = None):
    for tax_type in tax_list:
        tax_dict[tax_type][year][category] = {}
        tax_dict[tax_type][year][category]['value'] = calc.weighted_total_tax_dict(tax_type, tax_type+'ax')       

        tax_dict[tax_type][year][category]['value_bill'] = {}
        tax_dict[tax_type][year][category]['value_bill_str'] = {}     
        for k in tax_dict[tax_type][year][category]['value'].keys():
            tax_dict[tax_type][year][category]['value_bill'][k] = tax_dict[tax_type][year][category]['value'][k]/10**9
            tax_dict[tax_type][year][category]['value_bill_str'][k] = '{0:.2f}'.format(tax_dict[tax_type][year][category]['value_bill'][k])        
    #print('tax_dict ', tax_dict)
    return tax_dict
       
def weighted_total_tax_diff(tax_list, category1, category2, year, tax_dict, attribute_var = None):
    for tax_type in tax_list:
        tax_dict[tax_type][year][category2]['value_bill_diff'] = {}
        tax_dict[tax_type][year][category2]['value_bill_diff_str'] = {}
        for k in tax_dict[tax_type][year][category1]['value_bill'].keys():
            tax_dict[tax_type][year][category2]['value_bill_diff'][k] = (tax_dict[tax_type][year][category2]['value_bill'][k] -
                                                                  tax_dict[tax_type][year][category1]['value_bill'][k])
            tax_dict[tax_type][year][category2]['value_bill_diff_str'][k] = '{0:.2f}'.format(tax_dict[tax_type][year][category2]['value_bill_diff'][k])
    return tax_dict

def screen_print(tax_list, category, year, tax_dict, item, item_desc):
    for tax_type in tax_list:
        print("The "+tax_type.upper()+" "+item_desc+" in billions is: ", tax_dict[tax_type][year][category][item]['All'])

    
def generate_policy_revenues():
    from taxcalc.growfactors import GrowFactors
    from taxcalc.policy import Policy
    from taxcalc.records import Records
    from taxcalc.gstrecords import GSTRecords
    from taxcalc.corprecords import CorpRecords
    from taxcalc.parameters import ParametersBase
    from taxcalc.calculator import Calculator
    from taxcalc.utils import dist_variables

    f = open('global_vars.json')
    global_vars = json.load(f)
    verbose = global_vars['verbose']
    start_year = int(global_vars['start_year'])
    end_year = int(global_vars['end_year'])
    attribute_varlist = global_vars['attribute_vars']
    if len(attribute_varlist)==0: 
        attribute_var = None
    else:
        attribute_var = attribute_varlist[0]
    tax_list=[]
    tax_collection_var_list = []  
    # start the simulation for pit/cit/vat    
    if global_vars['pit']:
        tax_list = tax_list + ['pit']
        tax_collection_var_list = tax_collection_var_list + ['pitax']
        recs = Records(data=global_vars['pit_data_filename'], weights=global_vars['pit_weights_filename'], gfactors=GrowFactors(growfactors_filename=global_vars['GROWFACTORS_FILENAME']))
    else:
        recs = None
    if global_vars['cit']:
        tax_list = tax_list + ['cit']
        tax_collection_var_list = tax_collection_var_list + ['citax']
        crecs = CorpRecords(data=global_vars['cit_data_filename'], weights=global_vars['cit_weights_filename'], gfactors=GrowFactors(growfactors_filename=global_vars['GROWFACTORS_FILENAME']))
    else:
        crecs = None
    if global_vars['vat']:
        tax_list = tax_list + ['vat']
        tax_collection_var_list = tax_collection_var_list + ['vatax']
        grecs = GSTRecords(data=global_vars['vat_data_filename'], weights=global_vars['vat_weights_filename'], gfactors=GrowFactors(growfactors_filename=global_vars['GROWFACTORS_FILENAME']))
    else:
        grecs = None  
    
    adjust_behavior = 0
    for tax_type in tax_list:
        adjust_behavior = adjust_behavior or global_vars[tax_type+'_adjust_behavior']

    distribution_json_filename = {}
    distribution_vardict_dict = {}
    income_measure = {}
    for tax_type in tax_list:
        if global_vars[tax_type+'_distribution_table']:
            #CIT_VAR_INFO_FILENAME = 'taxcalc/'+vars['cit_records_variables_filename']
            #self.max_lag_years = vars['cit_max_lag_years']
            distribution_json_filename[tax_type] = 'taxcalc/'+global_vars[tax_type+'_distribution_json_filename']
            f = open(distribution_json_filename[tax_type])
            distribution_vardict_dict[tax_type] = json.load(f)
            #print('distribution_vardict_dict[tax_type] ', distribution_vardict_dict[tax_type])
            income_measure[tax_type] = distribution_vardict_dict[tax_type]['income_measure']
 
    f = open('reform.json')
    block_selected_dict = json.load(f)
    #print("block_selected_dict from json",block_selected_dict)
    
    # create Policy object containing current-law policy
    pol = Policy(DEFAULTS_FILENAME=global_vars['DEFAULTS_FILENAME'])
    
    # specify Calculator objects for current-law policy
    calc1 = Calculator(policy=pol, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)    
    assert isinstance(calc1, Calculator)
    assert calc1.current_year == start_year
    np.seterr(divide='ignore', invalid='ignore')
    pol2 = Policy(DEFAULTS_FILENAME=global_vars['DEFAULTS_FILENAME'])      
    years, reform=read_reform_dict(block_selected_dict)
    pol2.implement_reform(reform['policy'])
    calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)

    tax_collection_var = tax_collection_var_list[0]

    if adjust_behavior:
        elasticity_dict = {}
        for tax_type in tax_list:
            f = open('taxcalc/'+tax_type+'_elasticity_selection.json')
            elasticity_dict[tax_type] = json.load(f)
            #print(elasticity_dict)
            block_selected_dict = concat_dicts(block_selected_dict, elasticity_dict[tax_type])
        #print('block_selected_dict in adjust behavior',block_selected_dict)
        pol3 = Policy(DEFAULTS_FILENAME=global_vars['DEFAULTS_FILENAME'])   
        years, reform=read_reform_dict(block_selected_dict)
        #print('reform dict in adjust behavior', reform)
        pol3.implement_reform(reform['policy'])
        calc3 = Calculator(policy=pol3, records=recs, corprecords=crecs, gstrecords=grecs, verbose=verbose)
      
    #print("block_selected_dict after merging: ", block_selected_dict)       
    total_revenue_text={}
    reform_revenue_text={}
    revenue_dict={}
    revenue_amount_dict = {}
    num = 1
    first_time = True
    i=1
    j=0
    #rows = []
    
    window_dict={}
    row_num = {}
    data_row = {}
    l_TAB3 = {}
    dt1 = {}
    dt2 = {}
    dt1_percentile = {}
    dt2_percentile = {}
    dt = {}
    dt_percentile = {}  
    for tax_type in tax_list:
        revenue_dict[tax_type]={}
        dt1[tax_type] = {}
        dt2[tax_type] = {}
        dt1_percentile[tax_type] = {}
        dt2_percentile[tax_type] = {}
        dt[tax_type] = {}
        dt_percentile[tax_type] = {}             
        for year in range(start_year, end_year+1):
            revenue_dict[tax_type][year]={}
        window_dict[tax_type] = tk.Toplevel()
        window_dict[tax_type].geometry("800x600+600+140")
        #display_table(window, header=True)
        # Adjust this for number of years selected
        header = ["header","Year", "Current Law", "Reform", "Diff"]
        if global_vars[tax_type+'_adjust_behavior']:
            header = header + ['Reform (Behavior)', "Diff"]
        title_header = [["title", tax_type.upper()+" Projections"],
                        header]            
        row_num[tax_type] = display_table(window_dict[tax_type], data=title_header, header=True)
   
    for year in range(start_year, end_year+1):       
        calc1.advance_to_year(year)
        calc2.advance_to_year(year)
        calc1.calc_all()
        calc2.calc_all()
        
        revenue_dict = weighted_total_tax(calc1, tax_list, 'current_law', year, revenue_dict, attribute_var)              
        if verbose:
            print(f'TAX COLLECTION FOR THE YEAR - {year} \n')        
            screen_print(tax_list, 'current_law', year, revenue_dict, 'value_bill', 'Collection')
           
        revenue_dict = weighted_total_tax(calc2, tax_list, 'reform', year, revenue_dict, attribute_var)
        if verbose:        
            print(f'\nTAX COLLECTION FOR THE YEAR UNDER REFORM - {year} \n')       
            screen_print(tax_list, 'reform', year, revenue_dict, 'value_bill', 'Collection')
            
        revenue_dict = weighted_total_tax_diff(tax_list, 'current_law', 'reform', year, revenue_dict, attribute_var)
        if verbose:        
            screen_print(tax_list, 'reform', year, revenue_dict, 'value_bill_diff', 'Collection difference under Reform')

        for tax_type in tax_list:        
            data_row[tax_type] = [str(year), revenue_dict[tax_type][year]['current_law']['value_bill_str']['All'], 
                                  revenue_dict[tax_type][year]['reform']['value_bill_str']['All'], 
                                  revenue_dict[tax_type][year]['reform']['value_bill_diff_str']['All']]       
        if adjust_behavior:
        #redo the calculations by including behavioral adjustment
            calc3.advance_to_year(year)
            calc3.calc_all()
            revenue_dict = weighted_total_tax(calc3, tax_list, 'reform_behavior', year, revenue_dict, attribute_var)
            if verbose:            
                print(f'\nTAX COLLECTION FOR THE YEAR UNDER REFORM WITH BEHAVIOR ADJUSTMENT - {year} \n')
                screen_print(tax_list, 'reform_behavior', year, revenue_dict, 
                             'value_bill', 'Collection with Behavioral Adjustment')
            
            revenue_dict = weighted_total_tax_diff(tax_list, 'current_law', 'reform_behavior', year, revenue_dict, attribute_var)
            if verbose:
                screen_print(tax_list, 'reform_behavior', year, revenue_dict, 
                             'value_bill_diff',
                             'Collection difference with Behavioral Adjustment')
            for tax_type in tax_list:            
                data_row[tax_type] = data_row[tax_type] + [revenue_dict[tax_type][year]['reform_behavior']['value_bill_str']['All'], 
                                                           revenue_dict[tax_type][year]['reform_behavior']['value_bill_diff_str']['All']]
        for tax_type in tax_list:         
            row_num[tax_type] = display_table(window_dict[tax_type], 
                                              data = data_row[tax_type], 
                                              row = row_num[tax_type])
        #display_table(window, revenue_dict_pit=revenue_dict_pit, year=year, row=i)
        i=i+1
        dt1[tax_type][year]={}
        dt2[tax_type][year]={}
        dt1_percentile[tax_type][year]={}
        dt2_percentile[tax_type][year]={}      
        if global_vars[tax_type+'_distribution_table']:
            output_in_averages = True
            #output_categories = 'standard_income_bins'
            output_categories = 'weighted_deciles'
            # pd.options.display.float_format = '{:,.3f}'.format
            # dt1, dt2 = calc1.distribution_tables(calc2, 'weighted_deciles')
            dt1[tax_type][year], dt2[tax_type][year] = calc1.distribution_tables_dict(tax_type, calc2, output_categories, 
                                                distribution_vardict_dict[tax_type], income_measure=income_measure[tax_type],
                                                averages=output_in_averages,
                                                scaling=True, attribute_var=attribute_var)
            print('year ', year)
            print('dt1 ', dt1[tax_type][year]['All'])
            print('dt2 ', dt2[tax_type][year]['All'])
            output_categories = 'weighted_percentiles'
            dt1_percentile[tax_type][year], dt2_percentile[tax_type][year] = calc1.distribution_tables_dict(tax_type, calc2, output_categories, 
                                                 distribution_vardict_dict[tax_type], income_measure=income_measure[tax_type],
                                                 averages=output_in_averages,
                                                 scaling=True, attribute_var=attribute_var)
            #print('dt1_percentile[tax_type][year] ', dt1_percentile[tax_type][year])
    #print('dt1 ',dt1)
        
    def merge_distribution_table_dicts(dt1, dt2, tax_type, start_year, end_year):
        #print('dt1 ',dt1)
        #print('dt1[tax_type][start_year] ', dt1[tax_type][start_year])
        attribute_types = dt1[tax_type][start_year].keys()
        dt = {}
        for year in range(start_year, end_year+1):
            for attribute_value in attribute_types:
                dt1[tax_type][year][attribute_value] = dt1[tax_type][year][attribute_value].rename(columns={tax_collection_var:tax_collection_var+'_'+str(year), income_measure[tax_type]:income_measure[tax_type]+'_'+str(year)})
                dt2[tax_type][year][attribute_value] = dt2[tax_type][year][attribute_value].rename(columns={tax_collection_var:tax_collection_var+'_ref_'+str(year), income_measure[tax_type]:income_measure[tax_type]+'_ref_'+str(year)})               
        #print('dt1 ',dt1)
        #print('dt2 ',dt2)
        for attribute_value in attribute_types:
            dt[attribute_value] = dt1[tax_type][start_year][attribute_value][[tax_collection_var+'_'+str(start_year), income_measure[tax_type]+'_'+str(start_year)]]
            for year in range(start_year, end_year+1):
                dt[attribute_value]=dt[attribute_value].join(dt2[tax_type][year][attribute_value][[tax_collection_var+'_ref_'+str(year), income_measure[tax_type]+'_ref_'+str(year)]])     
        return dt 
    
    with open('revenue_dict.json', 'w') as f:
        json.dump(revenue_dict, f)
    #save the results of each tax type in separate files
    now = datetime.now() # current date and time
    date_time = now.strftime("%d_%m_%Y_%H_%M_%S")
    df = {}
    # save the results into a csv file
    for tax_type in tax_list:
        #filename1 = 'Revenue Data_'+'_'+tax_type+'_'+date_time
        filename_chart_rev_projection = tax_type+'_revenue_projection'
        revenue_dict_df = {}
        for k, v in revenue_dict[tax_type].items():
            revenue_dict_df[k] = {}
            for k1 in revenue_dict[tax_type][year]['current_law']['value'].keys():
                revenue_dict_df[k]['current_law_'+k1] = revenue_dict[tax_type][k]['current_law']['value_bill_str'][k1]
                revenue_dict_df[k]['reform_'+k1] = revenue_dict[tax_type][k]['reform']['value_bill_str'][k1]
                if adjust_behavior:
                    revenue_dict_df[k]['reform_behavior_'+k1] = revenue_dict[tax_type][k]['reform_behavior']['value_bill_str'][k1]
                    
        df[tax_type] = pd.DataFrame.from_dict(revenue_dict_df)   
        df_str = df[tax_type].to_string()
        df_reform = pd.DataFrame.from_dict(reform)
        df_reform_str = df_reform.to_string()
        text_output1 = df_str + '\n\n' + df_reform_str + '\n\n'
        write_file(df[tax_type], text_output1, filename_chart_rev_projection)
        last_row = row_num[tax_type]
        l_TAB3[tax_type] = tk.Button(window_dict[tax_type],
                                     text="Save Results",
                                     command=lambda: write_file(df[tax_type], 
                                                                text_output1, 
                                                                filename_chart_rev_projection, 
                                                                window_dict[tax_type], 
                                                                last_row
                                                                ))
        l_TAB3[tax_type].grid(row=row_num[tax_type]+2, column=2, pady = 10, sticky=tk.W)
    #footer = ["footer", "*Data saved in file "+ filename1]
    #row_num = display_table(window, data=footer, footer=row_num+2)
    ###### DISTRIBUTION TABLES ##############
    window_dist = {}
    row_num = {}
    dt={}
    for tax_type in tax_list:        
        if global_vars[tax_type+'_distribution_table']:
            dt[tax_type] = merge_distribution_table_dicts(dt1, dt2, tax_type, start_year, end_year)
            dt_percentile[tax_type] = merge_distribution_table_dicts(dt1_percentile, dt2_percentile, tax_type, start_year, end_year)            
            #print(dt)
            dt[tax_type]['All'].update(dt[tax_type]['All'].select_dtypes(include=np.number).applymap('{:,.0f}'.format))
            dt[tax_type]['All'].to_pickle('file.pkl')
            dt[tax_type]['All'] = pd.read_pickle('file.pkl')
            #dt[tax_type]['All'] = dt[tax_type]['All'].reset_index() 
            dt_tax_all = dt[tax_type]['All'][dt[tax_type]['All'].columns[dt[tax_type]['All'].columns.str.contains(tax_collection_var)]]
            print('dt_tax_all ', dt_tax_all)     
            dt_tax_all = dt_tax_all.reset_index()
            print('dt_tax_all ', dt_tax_all)
            #print('dt_percentile ',dt_percentile)
            dt_percentile[tax_type]['All']['ETR'] = dt_percentile[tax_type]['All'][tax_collection_var+'_'+str(start_year)]/dt_percentile[tax_type]['All'][income_measure[tax_type]+'_'+str(start_year)]            
            dt_percentile[tax_type]['All']['ETR_ref'] = dt_percentile[tax_type]['All'][tax_collection_var+'_ref_'+str(start_year)]/dt_percentile[tax_type]['All'][income_measure[tax_type]+'_ref_'+str(start_year)]            
            dt_percentile[tax_type]['All'].update(dt_percentile[tax_type]['All'].select_dtypes(include=np.number).applymap('{:,.4f}'.format))            
            #dt = dt.reset_index()
            # Adjust this for number of years selected
            #now = datetime.now() # current date and time
            #date_time = now.strftime("%d_%m_%Y_%H_%M_%S")
            filename2 = tax_type+'_distribution_table'
            text_output2 = dt[tax_type]['All'].to_string() + '\n\n'
            write_file(dt_tax_all, text_output2, filename2)
            filename_etr = tax_type+'_etr'
            text_output_etr = dt_percentile[tax_type]['All'].to_string() + '\n\n'
            write_file(dt_percentile[tax_type]['All'], text_output_etr, filename_etr)            
            if global_vars[tax_type+'_display_distribution_table']:
                window_dist[tax_type] = tk.Toplevel()
                window_dist[tax_type].geometry("900x700+600+140")
                header1 = ["header","", tax_type.upper()]
                header2 = ["header",'Decile','Current Law '+str(start_year)]
                for year in range(start_year, end_year+1):
                    header1 = header1+[tax_type.upper()]
                    header2 = header2+['Reform '+str(year)]          
                title_header = [["title", tax_type.upper()+" Distribution"],
                                header1, header2]     
                #footer = ["footer", "*Data saved in file datadump.csv"]         
                row_num[tax_type] = display_table(window_dist[tax_type], data=title_header, header=True)   
                row_num[tax_type] = display_table(window_dist[tax_type], row = row_num[tax_type], dataframe=dt_tax_all)
                l = tk.Button(window_dist[tax_type],text="Save Results",command=lambda: write_file(dt_tax_all, text_output2, filename2, window_dist[tax_type], row_num[tax_type]))
                l.grid(row=row_num[tax_type]+2, column=2, pady = 10, sticky=tk.W)
        #footer = ["footer", "*Data saved in file "+ filename1]
        #row_num = display_table(window_dist, data=footer, footer=row_num+2)
    
    global_vars['charts_ready'] = 1
    with open('global_vars.json', 'w') as f:
        f.write(json.dumps(global_vars, indent=2))
    #pt = Table(f, dataframe=dt,
       #showtoolbar=True, showstatusbar=True)
        
"""    
    #redo the calculations by including behavioral adjustment
    recs = Records(data=vars['pit_data_filename'], weights=vars['pit_weights_filename'], gfactors=GrowFactors(growfactors_filename=vars['GROWFACTORS_FILENAME']))
    pol2 = Policy(DEFAULTS_FILENAME=vars['DEFAULTS_FILENAME'])   
    years, reform=read_reform_dict(block_selected_dict)
    #print("reform dictionary: ",reform) 
    pol2.implement_reform(reform['policy'])
    calc2 = Calculator(policy=pol2, records=recs, verbose=False)
    assert isinstance(calc2, Calculator)
    assert calc2.current_year == 2017
    np.seterr(divide='ignore', invalid='ignore')

    for year in range(2019, 2023):
        calc2.advance_to_year(year)
        calc2.adjust_behavior(first_year=2019)
        calc2.calc_all()
        
        weighted_pitax3 = calc2.weighted_total_pit('pitax')                
        pitax_collection_billions3 = weighted_pitax3/10**9        
        pitax_collection_str3 = '{0:.2f}'.format(pitax_collection_billions3)
        
        print('\n\n\n')
        print(f'TAX COLLECTION FOR THE YEAR UNDER REFORM WITH BEHAVIOR ADJUSTMENT - {year} \n')   
        print("The PIT Collection in billions is: ", pitax_collection_billions3)

        pitax_diff_collection_billions4 = (pitax_collection_billions3-pitax_collection_billions1)        
        pitax_diff_collection_str4 = '{0:.2f}'.format(pitax_diff_collection_billions4)
                          
        #save the results
        
        revenue_dict_pit[year]['reform_behavior']=pitax_collection_str3
        revenue_dict_pit[year]['reform_behavior_difference']=pitax_diff_collection_str4
        
        display_table(window, revenue_dict_pit=revenue_dict_pit, year=year, row=i)
        i=i+1

   
    display_table(window, footer=i)
"""
    
"""
    #print(revenue_amount_dict)
    df_revenue_proj = pd.DataFrame(revenue_amount_dict)
    df_revenue_proj = df_revenue_proj.T
    df_revenue_proj['Current Law'] = df_revenue_proj['current_law'].apply(pd.Series)
    df_revenue_proj['Reform'] = df_revenue_proj['reform'].apply(pd.Series)
    df_revenue_proj = df_revenue_proj.drop(['current_law', 'reform'], axis=1)
    df_revenue_proj['Current Law'] = pd.to_numeric(df_revenue_proj['Current Law'])
    df_revenue_proj['Reform'] = pd.to_numeric(df_revenue_proj['Reform'])
    print("Revenues\n", df_revenue_proj)
    ax = df_revenue_proj.plot(y=["Current Law", "Reform"], kind="bar", rot=0,
                        figsize=(8,8))
    ax.set_ylabel('(billion )')
    ax.set_xlabel('')
    ax.set_title('CIT Revenue - Current Law vs. Reforms', fontweight="bold")
    pic_filename2 = 'PIT - Current Law and Reforms.png'
    
    plt.savefig(pic_filename2)
    
    img1 = Image.open(pic_filename2)
    img2 = img1.resize((500, 500), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img2)
    pic.configure(image=img3)
    pic.image = img3
"""
       
    

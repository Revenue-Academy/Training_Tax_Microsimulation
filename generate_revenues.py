# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:28:24 2021

@author: wb305167
"""

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont


#from taxcalc import *
from taxcalc.utils import *
    
from PIL import Image,ImageTk

def display_table(window, revenue_dict_cit, revenue_dict_pit, header=None, year=None, row=None, footer=None, all=None):
        # Display the results in a popup window
        # popup window for the Results but only one time after first 
        # set of results start coming in
        fontStyle_sub_title = tkfont.Font(family="Calibri", size="14", weight="bold")         

        if header:
            i=1
            #window = tk.Toplevel()
            #window.geometry("800x400+140+140")
            tk.Label0 = tk.Label(window, text="")
            tk.Label0.grid(row=i, column=0, sticky=tk.NSEW, padx=20)            
            tk.Label1 = tk.Label(window, text="Tax Collections and Projections", font=fontStyle_sub_title)
            tk.Label1.grid(row=i, column=2, columnspan=5)
            i=i+1
            #mainloop()
            l00 = tk.Label(window, text="", padx=20)
            l00.grid(row=i, column=0)
            l01 = tk.Label(window, text="Year", font=fontStyle_sub_title, relief=RIDGE)
            l01.grid(row=i, column=1, sticky=tk.NSEW)
            l02 = tk.Label(window, text="Corporate Income Tax (bill.)", font=fontStyle_sub_title,relief=RIDGE)
            l02.grid(row=i, column=2, sticky=tk.NSEW)
            l03 = tk.Label(window, text="Personal Income Tax (bill.)", font=fontStyle_sub_title,relief=RIDGE)
            l03.grid(row=i, column=3, sticky=tk.NSEW)
                        
            i=i+1
        
        if row is not None:
            i=row+2
            l0 = tk.Label(window, text="", padx=20)
            l0.grid(row=i, column=0, sticky=tk.NSEW)        
            l1 = tk.Label(window, text=str(year), font=fontStyle_sub_title, relief=RIDGE)
            l1.grid(row=i, column=1, sticky=tk.NSEW)
            l2 = tk.Label(window, text=str(revenue_dict_cit[year]['current_law']), font=fontStyle_sub_title, relief=RIDGE)
            l2.grid(row=i, column=2, sticky=tk.NSEW)
            l3 = tk.Label(window, text=str(revenue_dict_pit[year]['current_law']), font=fontStyle_sub_title, relief=RIDGE)
            l3.grid(row=i, column=3, sticky=tk.NSEW)            
            i=i+1
        
        if footer is not None:
            i=footer+3
            l4 = tk.Label(window, text="*Data saved in file datadump.csv")
            l4.grid(row=i, column=1, pady = 10, columnspan = 3, sticky=tk.W)        
    


def read_reform_dict(block_selected_dict):
    years=[]
    for k in block_selected_dict.keys():
        if (block_selected_dict[k]['selected_year'] not in years):
            years = years + [block_selected_dict[k]['selected_year']]
    ref = {}
    ref['policy']={}
    for year in years:
        policy_dict = {}
        for k in block_selected_dict.keys():
            if block_selected_dict[k]['selected_year']==year:
                policy_dict['_'+block_selected_dict[k]['selected_item']]=[float(block_selected_dict[k]['selected_value'])]
        ref['policy'][int(year)] = policy_dict
    years.sort()
    years = [int(x) for x in years]
    return years, ref

def fact():
    print("12345")
    f = open('reform.json')
    vars = json.load(f)
    print("block_selected_dict from json",vars)
    print("54321")
   
def generate_revenues():
    from taxcalc.growfactors import GrowFactors
    from taxcalc.policy import Policy
    from taxcalc.records import Records
    from taxcalc.gstrecords import GSTRecords
    from taxcalc.corprecords import CorpRecords
    from taxcalc.parameters import ParametersBase
    from taxcalc.calculator import Calculator
    

    """
    for num in range(1, num_reforms):
        block_selected_dict[num]['selected_item']= block_widget_dict[num][1].get()
        block_selected_dict[num]['selected_value']= block_widget_dict[num][3].get()
        block_selected_dict[num]['selected_year']= block_widget_dict[num][2].get()
    print(block_selected_dict)
    """
    f = open('reform.json')
    block_selected_dict = json.load(f)
    print("block_selected_dict from json",block_selected_dict)
    #print(block_selected_dict)
    # create Records object containing pit.csv and pit_weights.csv input data
    #print("growfactors filename ", growfactors_filename)
    #recs = Records(data=data_filename, weights=weights_filename, gfactors=GrowFactors(growfactors_filename=growfactors_filename))
    #recs = Records(data=data_filename, weights=weights_filename, gfactors=GrowFactors(growfactors_filename=growfactors_filename))

    #recs.increment_year1(3.0)
    
    #grecs = GSTRecords()
    f = open('global_vars.json')
    vars = json.load(f)
        
    print("data_filename: ", vars['cit_data_filename'])
    print("weights_filename: ", vars['cit_weights_filename'])
    print("growfactors_filename: ", vars['GROWFACTORS_FILENAME'])
    print("policy_filename: ", vars['DEFAULTS_FILENAME'])
    # create CorpRecords object using cross-section data
    #crecs1 = CorpRecords(data='cit_cross.csv', weights='cit_cross_wgts1.csv')
    crecs1 = CorpRecords(data=vars['cit_data_filename'], weights=vars['cit_weights_filename'], gfactors=GrowFactors(growfactors_filename=vars['GROWFACTORS_FILENAME']))
    #crecs1 = CorpRecords(data=vars['cit_weights_filename'], weights=vars['cit_weights_filename'])

    # Note: weights argument is optional
    assert isinstance(crecs1, CorpRecords)
    assert crecs1.current_year == 2017
    
    # create Policy object containing current-law policy
    pol = Policy(DEFAULTS_FILENAME=vars['DEFAULTS_FILENAME'])
    
    # specify Calculator objects for current-law policy
    #calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
    #                   gstrecords=grecs, verbose=False)
    calc1 = Calculator(policy=pol, corprecords=crecs1, verbose=False)    
    #calc1.increment_year1(3.8)
    assert isinstance(calc1, Calculator)
    assert calc1.current_year == 2017

    np.seterr(divide='ignore', invalid='ignore')
    
    calc1.calc_all()
    revenue_dict_cit={}
           
    for year in range(2019, 2024):
        cols = []
        calc1.advance_to_year(year)       

        # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
        #       so we can continue to use pol and recs in this script without any
        #       concern about side effects from Calculator method calls on calc1.

        # Produce DataFrame of results using the calculator
        
        # First run the calculator for the corporate income tax
        calc1.calc_all()
        
        print("***** Year ", year)
        weighted_citax1 = calc1.weighted_total_cit('citax')                
        citax_collection_billions1 = weighted_citax1/10**9       
        citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
              
        print("The CIT Collection in billions is: ", citax_collection_billions1)
 
        # Store Results
        revenue_dict_cit[year]={}
        revenue_dict_cit[year]['current_law']=citax_collection_str1
        
    # start a new round of simulation for pit
    recs = Records(data=vars['pit_data_filename'], weights=vars['pit_weights_filename'], gfactors=GrowFactors(growfactors_filename=vars['GROWFACTORS_FILENAME']))
    
    # create Policy object containing current-law policy
    pol = Policy(DEFAULTS_FILENAME=vars['DEFAULTS_FILENAME'])
    
    # specify Calculator objects for current-law policy
    #calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
    #                   gstrecords=grecs, verbose=False)
    calc1 = Calculator(policy=pol, records=recs, verbose=False)    
    #calc1.increment_year1(3.8)
    assert isinstance(calc1, Calculator)
    assert calc1.current_year == 2017

    np.seterr(divide='ignore', invalid='ignore')
        
    total_revenue_text={}
    reform_revenue_text={}
    revenue_dict_pit={}
    revenue_amount_dict = {}
    num = 1
    first_time = True
    i=1
    j=0
    #rows = []
    
    window = tk.Toplevel()
    window.geometry("800x400+140+140")
    display_table(window, revenue_dict_cit, revenue_dict_pit, header=True)

    #for year in range(years[0], years[-1]+1):            
    for year in range(2019, 2024):
        cols = []
        calc1.advance_to_year(year)       

        # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
        #       so we can continue to use pol and recs in this script without any
        #       concern about side effects from Calculator method calls on calc1.

        # Produce DataFrame of results using the calculator
        
        # First run the calculator for the corporate income tax
        calc1.calc_all()
        
        weighted_pitax1 = calc1.weighted_total_pit('pitax')                
        pitax_collection_billions1 = weighted_pitax1/10**9        
        pitax_collection_str1 = '{0:.2f}'.format(pitax_collection_billions1)
        
        print('\n\n\n')
        print(f'TAX COLLECTION FOR THE YEAR - {year} \n')   
        print("The PIT Collection in billions is: ", pitax_collection_billions1)       
        #total_revenue_text[year] = "PIT COLLECTION UNDER CURRENT LAW FOR THE YEAR - " + str(year)+" : "+str(pitax_collection_str1)+" bill"
        
        #save the results
        revenue_dict_pit[year]={}
        revenue_dict_pit[year]['current_law']=pitax_collection_str1
        
        display_table(window, revenue_dict_cit, revenue_dict_pit, year=year, row=i)
        i=i+1
   
    display_table(window, revenue_dict_cit, revenue_dict_pit, footer=i)

    
    
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
       
    

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:45:56 2021

@author: wb305167
"""

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk

from taxcalc import *

from PIL import Image,ImageTk

def generate_tax_expenditures(self):
    
    # create Records object containing pit.csv and pit_weights.csv input data
    #recs = Records()
    recs = Records(data=self.data_filename, weights=self.weights_filename, gfactors=GrowFactors(growfactors_filename=self.growfactors_filename))
    
    grecs = GSTRecords()
    
    crecs1 = CorpRecords()
    #crecs1 = CorpRecords(data=self.data_filename, weights=self.weights_filename)

    # Note: weights argument is optional
    assert isinstance(recs, Records)
    assert recs.current_year == 2017
    
    # create Policy object containing current-law policy
    pol = Policy()
    
    # specify Calculator objects for current-law policy
    calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
                       gstrecords=grecs, verbose=False)
    assert isinstance(calc1, Calculator)
    assert calc1.current_year == 2017

    np.seterr(divide='ignore', invalid='ignore')

    # Produce DataFrame of results using cross-section
    calc1.calc_all()
    #sector=calc1.carray('sector')
    weight = calc1.carray('weight')
    
    dump_vars = ['FILING_SEQ_NO', 'ST_CG_AMT_1', 'ST_CG_AMT_2', 'LT_CG_AMT_1', 'LT_CG_AMT_2', 
                 'pitax']
    dumpdf = calc1.dataframe_cit(dump_vars)
    #create the weight variable
    dumpdf['weight']= weight
    dumpdf= dumpdf.rename(columns={'citax':"tax_collected_under_current_policy"})
    dumpdf['weighted_tax_collected_under_current_policy']= dumpdf['weight']*dumpdf['tax_collected_under_current_policy']
    dumpdf['ID_NO']= "A"+ dumpdf['CIT_ID_NO'].astype('str') 
    benchmark = Calculator.read_json_param_objects(self.benchmark_filename, None)
    base_year = list(benchmark['policy'].keys())[0]
    #reform = dict(benchmark)
    reform = copy.deepcopy(benchmark)
    with open('taxcalc/'+self.policy_filename) as f:
        current_law_policy = json.load(f)             
    ref_dict = benchmark['policy']
    var_list = []
    tax_expediture_list = []
    tax_expediture_list_polish = []
    for pkey, sdict in ref_dict.items():
            for k, s in sdict.items():
                reform.pop("policy")
                mydict={}
                mydict[k]=s
                mydict0={}
                mydict0[pkey]=mydict
                reform['policy']=mydict0            
                pol2 = Policy()
                pol2.implement_reform(reform['policy'])
                calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                                   gstrecords=grecs, verbose=False)
                calc2.calc_all()
                weight2 = calc2.carray('weight')                   
                dump_vars = ['CIT_ID_NO', 'citax']     
                dumpdf_2 = calc2.dataframe_cit(dump_vars)
                dumpdf_2['weight']= weight2
                dumpdf_2['ID_NO']= "A"+ dumpdf_2['CIT_ID_NO'].astype('int').astype('str')
                dumpdf_2 = dumpdf_2.rename(columns={'citax':"tax_collected_under_benchmark"+ k})
                dumpdf_2['weighted_tax_collected_under_benchmark'+ k]= dumpdf_2['weight']*dumpdf_2['tax_collected_under_benchmark'+ k]
                dumpdf = pd.merge(dumpdf, dumpdf_2, how="inner", on="ID_NO")
                #calculating expenditure
                dumpdf['tax_expenditure_'+current_law_policy[k]['description']]= (dumpdf["weighted_tax_collected_under_benchmark"+ k]- dumpdf['weighted_tax_collected_under_current_policy'])/10**6
                dumpdf['tax_expenditure_'+current_law_policy[k]['long_name']]= (dumpdf["weighted_tax_collected_under_benchmark"+ k]- dumpdf['weighted_tax_collected_under_current_policy'])/10**6            
                var_list = var_list + [k]
                tax_expediture_list = tax_expediture_list + ['tax_expenditure_'+current_law_policy[k]['description']]
                tax_expediture_list_polish = tax_expediture_list_polish + ['tax_expenditure_'+current_law_policy[k]['long_name']]
                
    #Summarize here
    tax_expenditure_df = dumpdf[tax_expediture_list].sum(axis = 0)
    tax_expenditure_df= tax_expenditure_df.reset_index()
    tax_expenditure_df.columns = ['Tax Expenditure', 'Million ']
    tax_expenditure_df.to_csv('tax_expenditures_sum.csv',index=False, float_format='%.0f')
    print("Tax Expenditures\n", tax_expenditure_df)
    tax_expenditure_df = dumpdf[tax_expediture_list_polish].sum(axis = 0)
    tax_expenditure_df= tax_expenditure_df.reset_index()
    tax_expenditure_df.columns = ['Wydatki Podatkowe', 'Milion ']
    tax_expenditure_df.to_csv('tax_expenditures_sum_polish.csv', encoding='utf-8', index=False, float_format='%.0f')
    tax_expenditure_df.to_csv('tax_expenditures_sum_polish.txt', encoding='utf-8', sep=',', index=False)       
            
    # This is the Overall Tax Expenditures
    pol3 = Policy()
    reform = Calculator.read_json_param_objects(self.benchmark_filename, None)
    pol3.implement_reform(reform['policy'])
    
    calc2 = Calculator(policy=pol3, records=recs, corprecords=crecs1,
                       gstrecords=grecs, verbose=False)
    # popup window for the Results
    window = tk.Toplevel()
    window.geometry("700x600+140+140")
    label = tk.Label(window, text="Tax Expenditures", font=self.fontStyle_sub_title)
    label.place(relx = 0.40, rely = 0.02)
    self.s = ttk.Style()
    self.s.configure('my.TButton', font=self.fontStyle)         
    button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
    button_close.place(relx = 0.50, rely = 0.90)
    
    total_revenue_text={}
    reform_revenue_text={}
    tax_expenditure_text = {}        
    revenue_dict={}
    revenue_amount_dict = {}
    tax_expenditure = {}
    num = 1
    #for year in range(years[0], years[-1]+1):            
    for year in range(2019, 2024):  
        calc1.advance_to_year(year)        
        calc2.advance_to_year(year)
        # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
        #       so we can continue to use pol and recs in this script without any
        #       concern about side effects from Calculator method calls on calc1.

        # Produce DataFrame of results using cross-section
        calc1.calc_all()
        
        dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
                     'income_tax_base_after_deductions', 'citax']
        dumpdf_1 = calc1.dataframe_cit(dump_vars)
        dumpdf_1.to_csv('app00_poland1.csv', index=False, float_format='%.0f')
        
        Business_Profit1 = calc1.carray('income')
        Tax_Free_Incomes1 = calc1.carray('tax_free_income_total')
        Tax_Base_Before_Deductions1 = calc1.carray('tax_base_before_deductions')
        Deductions1 = calc1.carray('deductions_from_tax_base')
        Tax_Base_After_Deductions1 = calc1.carray('income_tax_base_after_deductions')
        citax1 = calc1.carray('citax')
        weight1 = calc1.carray('weight')
        etr1 = np.divide(citax1, Business_Profit1)
        weighted_etr1 = etr1*weight1.values
        weighted_etr_overall1 = (sum(weighted_etr1[~np.isnan(weighted_etr1)])/
                                 sum(weight1.values[~np.isnan(weighted_etr1)]))
        
        wtd_citax1 = citax1 * weight1
        
        citax_collection1 = wtd_citax1.sum()
        
        citax_collection_billions1 = citax_collection1/10**9
        
        citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
        
        print('\n\n\n')
        print('TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - '+str(year)+': ', citax_collection_billions1)
        
        total_revenue_text[year] = "TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str1)+" bill "
        #self.l6.config(text=total_revenue_text1)
        #self.l6.place(relx = 0.1, rely = 0.7+(num-1)*0.1, anchor = "w")
        # Produce DataFrame of results using cross-section
        calc2.calc_all()
        
        dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
                     'income_tax_base_after_deductions', 'citax']
        dumpdf_2 = calc2.dataframe_cit(dump_vars)
        dumpdf_2.to_csv('app00_poland2.csv', index=False, float_format='%.0f')
        
        Business_Profit2 = calc2.carray('income')
        Tax_Free_Incomes2 = calc2.carray('tax_free_income_total')
        Tax_Base_Before_Deductions2 = calc2.carray('tax_base_before_deductions')
        Deductions2 = calc2.carray('deductions_from_tax_base')
        Tax_Base_After_Deductions2 = calc2.carray('income_tax_base_after_deductions')
        citax2 = calc2.carray('citax')
        weight2 = calc2.carray('weight')
        etr2 = np.divide(citax2, Business_Profit2)
        weighted_etr2 = etr2*weight2.values
        weighted_etr_overall2 = (sum(weighted_etr2[~np.isnan(weighted_etr2)])/
                                 sum(weight2.values[~np.isnan(weighted_etr2)]))
        
        wtd_citax2 = citax2 * weight2
        
        citax_collection2 = wtd_citax2.sum()
        
        citax_collection_billions2 = citax_collection2/10**9
        citax_expenditure_billions = citax_collection_billions2 -  citax_collection_billions1
        citax_collection_str2 = '{0:.2f}'.format(citax_collection_billions2)
        
        citax_expenditure_billions_str = '{0:.5f}'.format(citax_expenditure_billions)
        
        print('\n\n\n')
        print('TAX COLLECTION UNDER BENCHMARK POLICY FOR THE YEAR - '+str(year)+': ', citax_collection_billions2)
             
        revenue_amount_dict[year]={}
        revenue_amount_dict[year]['current_law']={}            
        revenue_amount_dict[year]['current_law']['amount'] = citax_collection_billions1
        revenue_amount_dict[year]['benchmark']={}
        revenue_amount_dict[year]['benchmark']={}
        revenue_amount_dict[year]['benchmark']['amount'] = citax_collection_billions2
        
        revenue_amount_dict[year]['tax_expenditure']={}
        revenue_amount_dict[year]['tax_expenditure']={}                     
        revenue_amount_dict[year]['tax_expenditure']['amount'] = citax_expenditure_billions    
        
        reform_revenue_text[year] = "TAX COLLECTION UNDER BENCHMARK FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str2)+" bill "

        tax_expenditure_text[year] = "TAX EXPENDITURES FOR THE YEAR - " + str(year)+" : "+citax_expenditure_billions_str+" bill "
        
        revenue_dict[year]={}
        revenue_dict[year]['current_law'] = {}
        revenue_dict[year]['current_law']['Label'] = Label(window, text=total_revenue_text[year], font=self.fontStyle)
        revenue_dict[year]['current_law']['Label'].place(relx = 0.05, rely = 0.1+(num-1)*0.2, anchor = "w") 
        revenue_dict[year]['benchmark'] = {}
        revenue_dict[year]['benchmark']['Label'] = Label(window, text=reform_revenue_text[year], font=self.fontStyle)
        revenue_dict[year]['benchmark']['Label'].place(relx = 0.05, rely = 0.13+(num-1)*0.2, anchor = "w") 
        revenue_dict[year]['tax_expenditure'] = {}
        revenue_dict[year]['tax_expenditure']['Label'] = Label(window, text=tax_expenditure_text[year], font=self.fontStyle)
        revenue_dict[year]['tax_expenditure']['Label'].place(relx = 0.05, rely = 0.16+(num-1)*0.2, anchor = "w")            
        num += 1
    
    #print(revenue_amount_dict)
    df_revenue_proj = pd.DataFrame(revenue_amount_dict)
    df_revenue_proj = df_revenue_proj.T
    df_revenue_proj['Current Law'] = df_revenue_proj['current_law'].apply(pd.Series)
    df_revenue_proj['Benchmark'] = df_revenue_proj['benchmark'].apply(pd.Series)
    df_revenue_proj = df_revenue_proj.drop(['current_law', 'benchmark'], axis=1)
    df_revenue_proj['Current Law'] = pd.to_numeric(df_revenue_proj['Current Law'])
    df_revenue_proj['Benchmark'] = pd.to_numeric(df_revenue_proj['Benchmark'])
    print("Revenue Projections2\n", df_revenue_proj)
    ax = df_revenue_proj.plot(y=["Current Law", "Benchmark"], kind="bar", rot=0,
                        figsize=(8,8))
    ax.set_ylabel('(billion )')
    ax.set_xlabel('')
    ax.set_title('CIT - Tax Collection under Current Law vs. Benchmark', fontweight="bold")
    pic_filename3 = 'CIT - Current Law and Benchmark.png'
    plt.savefig(pic_filename3)
    
    img1 = Image.open(pic_filename3)
    img2 = img1.resize((500, 500), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img2)
    self.pic.configure(image=img3)
    self.pic.image = img3
    
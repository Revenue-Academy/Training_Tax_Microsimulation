"""
app_dist_Tables00.py illustrates use of pitaxcalc-demo release 2.0.0
(India version).
USAGE: python app_dist_Tables00.py
"""

import json
import locale
import pandas as pd
from taxcalc import *
import numpy as np
import matplotlib.pyplot as plt
from babel.numbers import format_currency

def remove_decimal(S):
    S = str(S)
    S = S[:-3]
    return S

def ind_currency(curr):
    curr_str = format_currency(curr, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    return(remove_decimal(curr_str))

def convert_df(df, cols):
    # breakup the dataframe into cols and others
    df1 = df[cols].copy(deep=True)
    cols_other = df.columns.difference(cols)
    df2 = df[cols_other].copy(deep=True)
    # strip the first row and make it into a list
    for i in range(len(df)):
        #print('i '+ str(i))
        row = df1.loc[i].values.tolist()
        #print(row)
        # take the list and build a new list element by element
        row1=[]
        for j in range(len(row)):
            #row1.append(format_it(str(row[i])))
            #row1.append(format_it(row[i]))
            #value_str = format_currency(row[j], 'INR', locale='en_IN').replace(u'\xa0', u' ')
            value_str = ind_currency(row[j])
            row1.append(value_str)
        # replace the row with the changed list
        df1.loc[i] =  row1
        # reassemble the dataframe
    df = pd.concat([df2, df1], axis=1)     
    return(df)




data_filename = "pit.csv"
weights_filename = "pit_weights.csv"
records_variables_filename = "records_variables.json"
cit_data_filename = "cit_cross.csv"
cit_weights_filename = "cit_cross_wgts1.csv"
corprecords_variables_filename = "corprecords_variables.json"
gst_data_filename = "gst.csv"
gst_weights_filename = "gst_weights.csv"
gstrecords_variables_filename = "gstrecords_variables.json"         
policy_filename = "current_law_policy_cmie11.json"
growfactors_filename = "growfactors1.csv"           
benchmark_filename = "tax_incentives_benchmark.json"
functions_filename = "functions1.py"
function_names = "function_names.json"
start_year = 2017
end_year=2023
SALARY_VARIABLE = "SALARY"
elasticity_filename = "elasticity.json"
DIST_VARIABLES = ['weight', 'GTI', 'pitax']
DIST_TABLE_COLUMNS = DIST_VARIABLES
DIST_TABLE_LABELS = ['Returns',
                     'Gross Total Income',
                     'PITax']
DECILE_ROW_NAMES = ['0-10n', '0-10z', '0-10p',
                    '10-20', '20-30', '30-40', '40-50',
                    '50-60', '60-70', '70-80', '80-90', '90-100',
                    'ALL',
                    '90-95', '95-99', 'Top 1%']
STANDARD_ROW_NAMES = ['<0', '=0', '0-1L', '1-10L', '10-15L',
                      '15-20L', '20-30L', '30-40L', '40-50L',
                      '50-100L', '>100L', 'ALL']
STANDARD_INCOME_BINS = [-9e99, -1e-9, 1e-9, 5e5, 10e5, 15e5, 20e5, 30e5,
                        40e5, 50e5, 100e5, 9e99]    
income_measure = "GTI"

vars = {}
vars['DEFAULTS_FILENAME'] = policy_filename        
vars['GROWFACTORS_FILENAME'] = growfactors_filename
vars['pit_data_filename'] = data_filename
vars['pit_weights_filename'] = weights_filename
vars['records_variables_filename'] = records_variables_filename        
vars['cit_data_filename'] = cit_data_filename
vars['cit_weights_filename'] = cit_weights_filename
vars['corprecords_variables_filename'] = corprecords_variables_filename
vars['gst_data_filename'] = gst_data_filename
vars['gst_weights_filename'] = gst_weights_filename
vars['gstrecords_variables_filename'] = gstrecords_variables_filename        
vars['benchmark_filename'] = benchmark_filename
vars['functions_filename'] = functions_filename
vars['function_names'] = function_names
vars["start_year"] = start_year
vars["end_year"] = end_year
vars["SALARY_VARIABLE"] = SALARY_VARIABLE
vars['elasticity_filename'] = elasticity_filename
vars['DIST_VARIABLES'] = DIST_VARIABLES
vars['DIST_TABLE_COLUMNS'] = DIST_TABLE_COLUMNS        
vars['DIST_TABLE_LABELS'] = DIST_TABLE_LABELS
vars['DECILE_ROW_NAMES'] = DECILE_ROW_NAMES
vars['STANDARD_ROW_NAMES'] = STANDARD_ROW_NAMES
vars['STANDARD_INCOME_BINS'] = STANDARD_INCOME_BINS
vars['income_measure'] = income_measure

with open('global_vars.json', 'w') as f:
    json.dump(vars, f)

from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()
#grecs = GSTRecords()
#crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, verbose=False)

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('Budget2019_reform.json', None)
#print(reform['policy'])
pol.implement_reform(reform['policy'])

calc2 = Calculator(policy=pol, records=recs, verbose=False)
# loop through years 2017, 2018, 2019, and 2020 and print out pitax

START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019
wtd_tax_clp={}
wtd_tax_ref={}
wtd_tot={}
for year in range(START_YEAR, END_YEAR+1):
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    calc2.calc_all()
    weighted_tax1 = calc1.weighted_total_pit('pitax')
    weighted_tax2 = calc2.weighted_total_pit('pitax')
    total_weights = calc1.total_weight_pit()
    wtd_tax_clp[year] = weighted_tax1
    wtd_tax_ref[year] = weighted_tax2
    wtd_tot[year] = total_weights
    if (year>=BASE_YEAR):
        print(f'****************  Total Tax Collection for {year}', end=' ')
        print('****************')
        print('\n')
        print(f'Current Law: Tax Collection in Rs. Cr. for {year}:', end=' ')
        print(f'{weighted_tax1 * 1e-7:,.2f}')
        print(f'Reform     : Tax Collection in Rs. Cr. for {year}:', end=' ')
        print(f'{weighted_tax2 * 1e-7:,.2f}')
        print('               Difference in Tax Collection:', end=' ')
        print(f'{(weighted_tax2-weighted_tax1) * 1e-7:,.2f} Cr.')
        print('\n')
        print(f'Representing: {total_weights * 1e-5:,.2f} Lakh taxpayers')
        print('\n')
        for output_in_averages in [False, True]:
            #output_categories = 'standard_income_bins'
            output_categories = 'weighted_deciles'
            # pd.options.display.float_format = '{:,.3f}'.format
            # dt1, dt2 = calc1.distribution_tables(calc2, 'weighted_deciles')
            dt1, dt2 = calc1.distribution_tables(calc2, output_categories,
                                                 averages=output_in_averages,
                                                 scaling=True)
            dt2['pitax_diff'] = dt2['pitax'] - dt1['pitax']
            if (output_categories == 'standard_income_bins'):
                dt1.rename_axis('Income_Bracket', inplace=True)
                dt2.rename_axis('Income_Bracket', inplace=True)
            else:
                dt1.rename_axis('Decile', inplace=True)
                dt2.rename_axis('Decile', inplace=True)
            dt1 = dt1.reset_index().copy()
            dt2 = dt2.reset_index().copy()
            dt1 = dt1.fillna(0)
            dt2 = dt2.fillna(0)
            if output_in_averages:
                print('***************************  Average Tax Burden ', end=' ')
                print(f'(in Rs.) per Taxpayer for {year}  ***************************')
                pd.options.display.float_format = '{:.0f}'.format
            else:
                print('*****************  Distribution Tables ', end=' ')
                print(f'for Total Tax Collection (in Rs. crores) for {year} *********')
                #pd.options.display.float_format = '{:,.0f}'.format
                pd.options.display.float_format = '{:.0f}'.format
            
            print(dt1)
            # list of columns for printing in rupees
            col_list1 = list(dt1.columns)
            if (output_categories == 'standard_income_bins'):
                col_list1.remove('Income_Bracket')
            else:
                col_list1.remove('Decile')
            col_list1.remove('weight')
            print('\n')
            print('  *** CURRENT-LAW DISTRIBUTION TABLE ***')
            #print('\n')
            print(convert_df(dt1, col_list1))
            print('\n')
            print('  *** POLICY-REFORM DISTRIBUTION TABLE ***')
            #print('\n')
            col_list2 = col_list1
            col_list2.append('pitax_diff')
            print(convert_df(dt2, col_list2))
            print('\n')
            # print text version of each complete distribution table to a file
            if output_in_averages:
                with open('dist-table-all-clp-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile)
                with open('dist-table-all-ref-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile)
                # print text version of each partial distribution table to a file
                to_include = ['weight', 'GTI', 'pitax']
                with open('dist-table-part-clp-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile, columns=to_include)
                with open('dist-table-part-ref-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile, columns=to_include)                
            else:
                with open('dist-table-all-clp-total-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile)
                with open('dist-table-all-ref-total-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile)
                # print text version of each partial distribution table to a file
                to_include = ['weight', 'GTI', 'pitax']
                with open('dist-table-part-clp-total-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile, columns=to_include)
                with open('dist-table-part-ref-total-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile, columns=to_include)

# Print the total taxes in the end

for year in range(BASE_YEAR, END_YEAR+1):
    wtd_tax_clp_rs = ind_currency(wtd_tax_clp[year] * 1e-7)
    wtd_tax_ref_rs = ind_currency(wtd_tax_ref[year] * 1e-7)
    wtd_tax_diff_rs = ind_currency((wtd_tax_ref[year]-wtd_tax_clp[year]) * 1e-7)
    print(f'****************  Total Tax Collection for {year}', end=' ')
    print('****************')
    #print('\n')
    print(f'Current Law: Tax Collection in Rs. Cr. for {year}:', end=' ')
    print(f'{ind_currency(wtd_tax_clp[year] * 1e-7)}')
    print(f'Reform     : Tax Collection in Rs. Cr. for {year}:', end=' ')
    print(f'{ind_currency(wtd_tax_ref[year] * 1e-7)}')
    print('                   Difference in Tax Collection:', end=' ')
    print(f'{ind_currency((wtd_tax_ref[year]-wtd_tax_clp[year]) * 1e-7)} Cr.')
    print(f'Representing: {wtd_tot[year] * 1e-5:,.2f} Lakh taxpayers')
    print('\n')


# Generate Charts
# first merge the files
START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019
year = START_YEAR
a={}
for year in range(BASE_YEAR, END_YEAR+1):
    filename1='dist-table-all-clp-avg-'+str(year)+'.txt'
    df1 = pd.read_fwf(filename1)
    df1.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df1.columns[1:] + '_avg_clp_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df1.columns = col_list
    filename2='dist-table-all-clp-total-'+str(year)+'.txt'
    df2 = pd.read_fwf(filename2)       
    df2.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df2.columns[1:] + '_total_clp_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df2.columns = col_list
    a[year] = pd.merge(df1, df2, how="inner", on="Income_Bracket")
    filename3='dist-table-all-ref-avg-'+str(year)+'.txt'
    df3 = pd.read_fwf(filename3)       
    df3.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df3.columns[1:] + '_avg_ref_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df3.columns = col_list
    a[year] = pd.merge(a[year], df3, how="inner", on="Income_Bracket")
    filename4='dist-table-all-ref-total-'+str(year)+'.txt'
    df4 = pd.read_fwf(filename4)       
    df4.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df4.columns[1:] + '_total_ref_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df4.columns = col_list
    a[year] = pd.merge(a[year], df4, how="inner", on="Income_Bracket")

df=a[BASE_YEAR]
for year in range(BASE_YEAR+1, END_YEAR+1):
    df = pd.merge(df, a[year], how="inner", on="Income_Bracket")

df.set_index('Income_Bracket', inplace=True)
df.to_csv('dist-table-all-years.csv', index=True)

df = pd.read_csv('dist-table-all-years.csv')
df.set_index('Income_Bracket', inplace=True)

# generating bar chart for Total Tax collection due to current law and reform 
# for all years
df_pit_totals_clp = df[df.columns[df.columns.str.startswith('pitax_total_clp')]]
df_pit_totals_ref = df[df.columns[df.columns.str.startswith('pitax_total_ref')]]
clp_pitax_list = df_pit_totals_clp.loc['ALL'].tolist()
#clp_pitax_list = [float(i.replace(',','')) for i in clp_pitax_list]
clp_pitax_list = [round(elem, 0) for elem in clp_pitax_list ]
ref_pitax_list = df_pit_totals_ref.loc['ALL'].tolist()
#ref_pitax_list = [float(i.replace(',','')) for i in ref_pitax_list]
ref_pitax_list = [round(elem, 0) for elem in ref_pitax_list ]
years = [x[-4:] for x in list(df_pit_totals_clp.columns)]

plt.style.use('seaborn-whitegrid')
fig = plt.figure()
"""
ax = plt.axes()
ax.plot(x, np.sin(x))
ax.set(xlim=(0, 10), ylim=(-2, 2),
       xlabel='x', ylabel='sin(x)',
       title='A Simple Plot')
"""
#plt.axis([2017, 2021, 150000, 400000])
plt.title("Estimated Tax Collection")
plt.xlabel("Year")
plt.ylabel("Tax Collection in lakh Cr.");
"""
print(year)
print(clp_pitax_list)
print(ref_pitax_list)
"""
plt.plot(years, clp_pitax_list, linestyle='-', marker='o', color='b', label='Current Law', linewidth=2.0)
plt.plot(years, ref_pitax_list, linestyle='--', marker='o', color='r', label='Reform', linewidth=2.0)
plt.legend(loc='best')
plt.savefig('Total_collection_PIT.png')
plt.show()

# generating bar chart for difference in average tax burden due to reform 
# for 2020 - the first year of reform
year = 2020
df_pitax_diff = df['pitax_diff_avg_ref_'+str(year)]
df_pitax_diff = df_pitax_diff[:-1]
df_pitax_diff = df_pitax_diff[2:]
df_pitax_diff = df_pitax_diff.reset_index()
pitax_inc_brac_list = df_pitax_diff['Income_Bracket'].tolist()
pitax_diff_list = df_pitax_diff['pitax_diff_avg_ref_'+str(year)].tolist()

#pitax_diff_list = [float(i.replace(',','')) for i in pitax_diff_list]

plt.rcdefaults()
#plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(8, 5))
# Example data
x_pos = np.arange(len(pitax_inc_brac_list))
ax.bar(x_pos, pitax_diff_list, 
        color='green')
ax.set_xticks(x_pos)
ax.set_xticklabels(pitax_inc_brac_list)
#ax.invert_yaxis()  # labels read top-to-bottom
ax.set_ylabel('Rupees')
ax.set_xlabel('Income Bracket')
ax.invert_yaxis()
ax.set_title('Change in Average Tax Burden Due to Reform in 2020')
plt.savefig('Average Tax Burden Change.png')
plt.show()

# generating bar chart for Difference in Total tax collection due to reform 
# for 2020 - the first year of reform

#df_pit_totals_clp = df[df.columns[df.columns.str.startswith('pitax_diff_clp')]]
df_pitax_diff_totals_ref = df[df.columns[df.columns.str.startswith('pitax_diff_total_ref')]]
pitax_diff_totals_ref_list = df_pitax_diff_totals_ref.loc['ALL'].tolist()
# ref_pitax_diff_list = [float(i.replace(',','')) for i in ref_pitax_diff_list]
pitax_diff_totals_ref_list = [round(elem, 0) for elem in pitax_diff_totals_ref_list ]
years = [x[-4:] for x in list(df_pitax_diff_totals_ref.columns)]

#plt.style.use('seaborn-whitegrid')
#fig = plt.figure()
plt.rcdefaults()
#plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(8, 5))
width = 0.35
x_pos = np.arange(len(years))
ax.bar(x_pos, pitax_diff_totals_ref_list, width,
        color='orange')
ax.set_xticks(x_pos)
ax.set_xticklabels(years)
#ax.invert_yaxis()  # labels read top-to-bottom
ax.set_ylabel('Rupees in Crores')
ax.set_xlabel('Years')
ax.invert_yaxis()
ax.set_title('Change in Total Tax Burden Due to Reform in 2020', fontweight="bold")
plt.savefig('Change in Total Tax Burden Due to Reform.png')
plt.show()


# generating pie chart for contribution of tax by different income groups 
# for 2020 - the first year of reform

year = 2020
df_pitax_tot_clp = df['pitax_total_clp_'+str(year)]
df_pitax_tot_clp = df_pitax_tot_clp[:-1]
df_pitax_tot_clp = df_pitax_tot_clp[2:]
df_pitax_tot_clp = df_pitax_tot_clp.reset_index()
pitax_inc_brac_list_clp = df_pitax_tot_clp['Income_Bracket'].tolist()
pitax_tot_list_clp = df_pitax_tot_clp['pitax_total_clp_'+str(year)].tolist()
#pitax_tot_list_clp = [float(i.replace(',','')) for i in pitax_tot_list_clp]
pitax_tot_list_clp = [round(elem) for elem in pitax_tot_list_clp ]

fig, ax = plt.subplots(figsize=(10, 5))
# only "explode" the 5th slice (contributing to max revenue)
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0.1)  

ax.pie(pitax_tot_list_clp, explode=explode, labels=pitax_inc_brac_list_clp, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.suptitle('Contribution by Income Bracket to total PIT in 2020 - Current Law', fontsize=16, fontweight="bold")
plt.savefig('Contribution to total PIT.png')
plt.show()


# generating pie chart for comparing contribution of tax by 
# different income groups for clp and reform for 2020 - the first year of reform



year = 2020
df_pitax_tot = df['pitax_total_ref_'+str(year)]
df_pitax_tot = df_pitax_tot[:-1]
df_pitax_tot = df_pitax_tot[2:]
df_pitax_tot = df_pitax_tot.reset_index()
pitax_inc_brac_list = df_pitax_tot['Income_Bracket'].tolist()
pitax_tot_list = df_pitax_tot['pitax_total_ref_'+str(year)].tolist()
#pitax_tot_list = [float(i.replace(',','')) for i in pitax_tot_list]
pitax_tot_list = [round(elem) for elem in pitax_tot_list ]


fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10, 5))
#fig, ax = plt.subplots(figsize=(10, 5))
#the_grid = GridSpec(2, 2)

# only "explode" the 5th slice (contributing to max revenue)
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0.1)  

#plt.subplot(the_grid[1, 0], aspect=1)
plt.suptitle('Contribution by Income Bracket to total PIT in 2020', fontsize=16, fontweight="bold")
ax1.pie(pitax_tot_list_clp, explode=explode, labels=pitax_inc_brac_list_clp, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#plt.subplot(the_grid[0, 1], aspect=1)
ax2.pie(pitax_tot_list, explode=explode, labels=pitax_inc_brac_list, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Current Law', fontweight="bold")
ax2.set_title('Reform', fontweight="bold")
plt.savefig('Contribution to total PIT - Before and After Reform.png')
plt.show()





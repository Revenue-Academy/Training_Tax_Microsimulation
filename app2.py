"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app2.py
"""
import pandas as pd
import json

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

with open('global_vars.json', 'w') as f:
    json.dump(vars, f)

from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Records object containing pit.csv and pit_weights.csv input data
#grecs = GSTRecords()

# create CorpRecords object containing cit.csv and cit_weights.csv input data
#crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
#calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
#                   corprecords=crecs, verbose=False)

calc1 = Calculator(policy=pol, records=recs, verbose=False)
#calc1.adjust_behavior('SALARY', elasticity_dict)
# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app1_reform1.json', None)
#print(reform)
pol2 = Policy()
pol2.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol2, records=recs, verbose=False)
#calc2.adjust_behavior('SALARY', elasticity_dict)
      
# loop through years 2017, 2018, and 2019 and print out pitax
for year in range(2019, 2021):
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    calc2.calc_all()
    weighted_tax1 = calc1.weighted_total_pit('pitax')
    weighted_tax2 = calc2.weighted_total_pit('pitax')    
    calc2_behv = copy.deepcopy(calc2)
    #print("without reform: ",calc1.array('SALARY'))
    #print("before adj: ",calc2.array('SALARY'))
    first_year=2019
    print("starting behavior adjustment")
    calc2_behv.adjust_behavior(first_year=2019, elasticity_filename=elasticity_filename)
    # Recalculate post-reform taxes incorporating behavioral responses
    calc2_behv.calc_all()
    weighted_tax3 = calc2_behv.weighted_total_pit('pitax')
    total_weights = calc1.total_weight_pit()
    print(f'Tax 1 for {year}: {weighted_tax1 * 1e-9:,.2f}')
    print(f'Tax 2 for {year}: {weighted_tax2 * 1e-9:,.2f}')
    print(f'Tax 2 for {year} Adjusted: {weighted_tax3 * 1e-9:,.2f}')    
    print(f'Total weight for {year}: {total_weights * 1e-6:,.2f}')
    #print(calc1.array('pitax'))
    #print(calc2.array('pitax'))
    #print(calc2_behv.array('pitax'))
    """
    dump_vars = ['FILING_SEQ_NO', 'AGEGRP', 'SALARY', 'INCOME_HP',
             'TOTAL_PROFTS_GAINS_BP', 'TOTAL_INCOME_OS', 'GTI', 'TTI', 'Aggregate_Income', 'pitax']
    dump_vars_year_clp = [i+'_clp_'+str(year) for i in dump_vars]
    dump_vars_year_ref = [i+'_ref_'+str(year) for i in dump_vars]    
    dump_vars_behv = [i+'_behv' for i in dump_vars_year_ref]
    dumpdf1 = calc1.dataframe(dump_vars)
    dumpdf1.to_csv('app2-dump-clp-'+str(year)+'.csv',
              index=False, float_format='%.0f')
    dumpdf1.columns = dump_vars_year_clp
    dumpdf2 = calc2.dataframe(dump_vars)
    dumpdf2.to_csv('app2-dump-ref-'+str(year)+'.csv',
              index=False, float_format='%.0f')
    dumpdf2.columns = dump_vars_year_ref    
    dumpdf3 = calc2_behv.dataframe(dump_vars)
    dumpdf3.to_csv('app2-dump-ref-behv-'+str(year)+'.csv',
              index=False, float_format='%.0f')
    dumpdf3.columns = dump_vars_behv 
    """
"""
# dump out records for 2019
dump_vars = ['FILING_SEQ_NO', 'AGEGRP', 'SALARIES', 'INCOME_HP',
             'TOTAL_PROFTS_GAINS_BP', 'TOTAL_INCOME_OS', 'GTI', 'TTI']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['pitax1'] = calc1.array('pitax')
dumpdf['pitax2'] = calc2.array('pitax')
dumpdf['pitax_diff'] = dumpdf['pitax2'] - dumpdf['pitax1']
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app2-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
"""

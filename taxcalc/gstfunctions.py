"""
pitaxcalc-demo functions that calculate GST paid.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import json
import numpy as np
from taxcalc.decorators import iterate_jit
from taxcalc.gstrecords import GSTRecords

def gst_liability_item(calc):
    #json_data = open('taxcalc/gstrecords_variables_cmie.json').read()
    #vardict = json.loads(json_data)
    #print(vardict)
    vardict = GSTRecords.read_var_info()
    #print(vardict)
    FIELD_VARS = list(k for k, v in vardict['read'].items()
                      if (v['type'] == 'int' or v['type'] == 'float'))
    #print(FIELD_VARS)
    total_consumption_food = np.zeros(len(calc.garray('ID_NO')))
    total_consumption_non_food = np.zeros(len(calc.garray('ID_NO')))
    total_consumption_education = np.zeros(len(calc.garray('ID_NO')))
    total_consumption_health = np.zeros(len(calc.garray('ID_NO')))    
    total_consumption = np.zeros(len(calc.garray('ID_NO')))  
    gst_food = np.zeros(len(calc.garray('ID_NO')))
    gst_non_food = np.zeros(len(calc.garray('ID_NO')))
    gst_education = np.zeros(len(calc.garray('ID_NO')))
    gst_health = np.zeros(len(calc.garray('ID_NO')))
    gst = np.zeros(len(calc.garray('ID_NO')))    
    for v in FIELD_VARS:
        category = vardict['read'][v]['category']
        if v.startswith('CONS_'):
            w = v.replace('CONS_', 'gst_rate_').lower()
            x = v.replace('CONS_', 'gst_').lower()
            cons_item = calc.garray(v)
            gst_rate_item = calc.policy_param(w)
            gst_item = cons_item * (gst_rate_item/(1+gst_rate_item))
            calc.garray(x, gst_item)
            gst += gst_item
            total_consumption += cons_item
            if (category=='FOOD'):
                total_consumption_food += cons_item
                gst_food += gst_item
            elif (category=='NON_FOOD'):
                total_consumption_non_food += cons_item
                gst_non_food += gst_item
            elif (category=='EDUCATION'):
                total_consumption_education += cons_item
                gst_education += gst_item
            elif (category=='HEALTH'):
                total_consumption_health += cons_item
                gst_health += gst_item                
    calc.garray('total_consumption_food', total_consumption_food)
    calc.garray('total_consumption_non_food', total_consumption_non_food)
    calc.garray('total_consumption_education', total_consumption_education)
    calc.garray('total_consumption_health', total_consumption_health)    
    calc.garray('total_consumption', total_consumption)   
    calc.garray('gst_food', gst_food)
    calc.garray('gst_non_food', gst_non_food)
    calc.garray('gst_education', gst_education)
    calc.garray('gst_health', gst_health)
    calc.garray('gst', gst)    

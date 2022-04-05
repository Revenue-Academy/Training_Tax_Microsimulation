"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


"Calculation for wages" 
@iterate_jit(nopython=True)
def cal_ssc_w(ssc_rate_w, kind_1, ssc_w_calc):
    """
    Compute ssc as gross salary minus deductions u/s 16.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    intrducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    
    ssc_w_calc = ssc_rate_w*kind_1
    return ssc_w_calc


@iterate_jit(nopython=True)
def cal_tti_w(personal_allowance_labour, kind_1, ssc_w_calc, tti_w):
    """
    Compute ssc as gross salary minus deductions u/s 16.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    introducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """
    
    tti_w = kind_1 - ssc_w_calc - personal_allowance_labour
    tti_w = max(tti_w,0)
    
    return tti_w


@iterate_jit(nopython=True)
def cal_tti_I(kind_2,kind_3,kind_4,kind_5,kind_6,kind_7,kind_14,kind_19,kind_20,kind_23, tti_I):
    """
    Compute ssc as gross salary minus deductions u/s 16.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    intrducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    tti_I = kind_2+kind_3+kind_4+kind_5+kind_6+kind_7+kind_14+kind_19+kind_20+kind_23
    tti_I = max(tti_I,0)
    return tti_I


@iterate_jit(nopython=True)
def cal_tti_w_I(tti_w, tti_I, tti_w_I):
    """
    Compute the taxable total income from labor and business.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed

    tti_w_I = tti_w + tti_I
    
    return tti_w_I

@iterate_jit(nopython=True)
def cal_tti_w_I_behavior(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3,
                         rate1_curr_law, rate2_curr_law, rate3_curr_law, 
                         rate4_curr_law, tbrk1_curr_law, tbrk2_curr_law,
                         tbrk3_curr_law,
                         elasticity_pit_taxable_income_threshold,
                         elasticity_pit_taxable_income_value, tti_w_I,
                         tti_w_I_behavior):
    """
    Compute taxable total income after adjusting for behavior.
    """  
    elasticity_taxable_income_threshold0 = elasticity_pit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_pit_taxable_income_threshold[1]
    elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_pit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_pit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_pit_taxable_income_value[2]
    if tti_w_I<=0:
        elasticity=0
    elif tti_w_I<elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif tti_w_I<elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    else:
        elasticity=elasticity_taxable_income_value2

    if tti_w_I<0:
        marg_rate=0
    elif tti_w_I<=tbrk1:
        marg_rate=rate1
    elif tti_w_I<=tbrk2:
        marg_rate=rate2
    elif tti_w_I<=tbrk3:
        marg_rate=rate3
    else:        
        marg_rate=rate4

    if tti_w_I<0:
        marg_rate_curr_law=0
    elif tti_w_I<=tbrk1_curr_law:
        marg_rate_curr_law=rate1_curr_law
    elif tti_w_I<=tbrk2_curr_law:
        marg_rate_curr_law=rate2_curr_law
    elif tti_w_I<=tbrk3_curr_law:
        marg_rate_curr_law=rate3_curr_law
    else:        
        marg_rate_curr_law=rate4_curr_law
    
    frac_change_net_of_pit_rate = ((1-marg_rate)-(1-marg_rate_curr_law))/(1-marg_rate_curr_law)
    frac_change_tti_w_I = elasticity*(frac_change_net_of_pit_rate)  
    tti_w_I_behavior = tti_w_I*(1+frac_change_tti_w_I)
    return tti_w_I_behavior

@iterate_jit(nopython=True)
def cal_pit_w(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, tti_w, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tti_w  
    
    pit_w = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))
        
    return (pit_w)


@iterate_jit(nopython=True)
def cal_net_i_w(kind_1, ssc_labour, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    net_i_w = kind_1-ssc_labour-pit_w 
    return net_i_w


@iterate_jit(nopython=True)
def cal_pit_I(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, tti_I, pit_I):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tti_I
    
    pit_I = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))
    return (pit_I)


@iterate_jit(nopython=True)
def cal_net_i_I(kind_2,kind_3,kind_4,kind_5,kind_6,kind_7,kind_14,kind_19,kind_20,kind_23, ssc_I, pit_I, net_i_I):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    net_i_I = (kind_2+kind_3+kind_4+kind_5+kind_6+kind_7+kind_14+kind_19+kind_20+kind_23) - pit_I
    
    
    return net_i_I


@iterate_jit(nopython=True)
def cal_pit_w_I(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, 
                tti_w_I_behavior, pit_w_I):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tti_w_I_behavior 
    pit_w_I = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))
    return (pit_w_I)

    
"Calculation for Income from Capital"
@iterate_jit(nopython=True)
def cal_tti_c(kind_8,kind_9,kind_10,kind_11,kind_12,kind_13,kind_25,kind_26,deductions_capital, tti_c):
    """
    Compute ssc as gross salary minus deductions u/s 16.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    intrducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    tti_c = (kind_8+kind_9+kind_10+kind_11+kind_12+kind_13+kind_25+kind_26)-deductions_capital
    
    return tti_c

@iterate_jit(nopython=True)
def cal_tti_c_behavior(capital_income_rate, capital_income_rate_curr_law,
              elasticity_pit_capital_income_threshold,
              elasticity_pit_capital_income_value,
              tti_c, tti_c_behavior):
    """
    Compute ssc as gross salary minus deductions u/s 16.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    intrducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    elasticity_pit_capital_income_threshold0 = elasticity_pit_capital_income_threshold[0]
    elasticity_pit_capital_income_threshold1 = elasticity_pit_capital_income_threshold[1]
    elasticity_pit_capital_income_threshold2 = elasticity_pit_capital_income_threshold[2]
    elasticity_pit_capital_income_value0=elasticity_pit_capital_income_value[0]
    elasticity_pit_capital_income_value1=elasticity_pit_capital_income_value[1]
    elasticity_pit_capital_income_value2=elasticity_pit_capital_income_value[2]
    
    if tti_c<=0:
        elasticity=0
    elif tti_c<=elasticity_pit_capital_income_threshold0:
        elasticity=elasticity_pit_capital_income_value0
    elif tti_c<=elasticity_pit_capital_income_threshold1:
        elasticity=elasticity_pit_capital_income_value1
    else:
        elasticity=elasticity_pit_capital_income_value2
    
    frac_change_net_of_pit_capital_income_rate = ((1-capital_income_rate)-(1-capital_income_rate_curr_law))/(1-capital_income_rate_curr_law)
    frac_change_tti_c = elasticity*(frac_change_net_of_pit_capital_income_rate)  
    tti_c_behavior = tti_c*(1+frac_change_tti_c)    
    return tti_c_behavior
    
@iterate_jit(nopython=True)
def cal_pit_c(capital_income_rate, tti_c_behavior, pit_c):
    """pit_c
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    pit_c = tti_c_behavior*capital_income_rate
    return pit_c

@iterate_jit(nopython=True)
def cal_net_i_c(kind_8,kind_9,kind_10,kind_11,kind_12,kind_13,kind_25,kind_26,pit_c, net_i_c):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    net_i_c = (kind_8+kind_9+kind_10+kind_11+kind_12+kind_13+kind_25+kind_26)-pit_c
    
    return net_i_c

"total"
@iterate_jit(nopython=True)
def cal_total_gross_income(kind_1, kind_2,kind_3,kind_4,kind_5,kind_6,kind_7,kind_14,kind_19,kind_20,kind_23, kind_8,kind_9,kind_10,kind_11,kind_12,kind_13,kind_25,kind_26,total_gross_income):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_gross_income = kind_1+kind_2+kind_3+kind_4+kind_5+kind_6+kind_7+kind_14+kind_19+kind_20+kind_23+kind_8+kind_9+kind_10+kind_11+kind_12+kind_13+kind_25+kind_26
   
    return total_gross_income

@iterate_jit(nopython=True)
def cal_total_taxable_income(tti_w_I, tti_c, total_taxable_income):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_taxable_income = tti_w_I + tti_c
    return total_taxable_income


@iterate_jit(nopython=True)
def cal_total_pit(pit_w_I, pit_c, pitax):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    pitax = pit_w_I + pit_c
    return pitax

@iterate_jit(nopython=True)
def cal_total_net_income(net_i_w, net_i_I, net_i_c, total_net_income):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_net_income = net_i_w + net_i_I + net_i_c
    return total_net_income

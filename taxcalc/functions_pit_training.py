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

"Calculation for minimum base wage"
@iterate_jit(nopython=True)
def cal_min_base_wage(ave_gross_wage, min_base_wage):
    min_base_wage = ave_gross_wage * 0.5 * 12
    return min_base_wage

"Calculation for maximum base wage"
@iterate_jit(nopython=True)
def cal_max_base_wage(ave_gross_wage,number_of_wages_ssc, max_base_wage):
    max_base_wage = ave_gross_wage * number_of_wages_ssc * 12
    return max_base_wage

"Calculation for minimum Social Security Contribution (SSC)"
@iterate_jit(nopython=True)
def cal_min_ssc(min_base_wage, ssc_rate):
    min_ssc = min_base_wage * ssc_rate
    return min_ssc

"Calculation for maximum Social Security Contribution (SSC)"
@iterate_jit(nopython=True)
def cal_max_ssc(max_base_wage, ssc_rate):
    max_ssc = max_base_wage * ssc_rate
    return max_ssc

"Calculation for Social Security Contribution (SSC)"  
@iterate_jit(nopython=True)
def cal_ssc_w(ssc_w, income_wage_l, ssc_rate, min_base_wage, max_base_wage, min_ssc, max_ssc, ssc_w_calc):
    """
    Compute ssc for wages.
    """
    """ Note : First condition: Case when SSC is zero (e.g Exemption from SSC for TIDZ or no income from wages);
    Second condition:Case when gross income from wages is below minimum wages;
    Third condition: Case when gross income from wages is range between minium and maximum wages an
    Fourth condition:Case when gross income from wages is above maximum wages.
    note: income_wage_l = gross income for wages
    """
    if (ssc_w ==0 and income_wage_l > 0):     #ssc in cases where wage income is non-zero but ssc as per data is zero is deemed zero
        ssc_w_calc = 0 
    elif (income_wage_l < min_base_wage):
        ssc_w_calc = min_ssc
    elif (income_wage_l >= min_base_wage) and (income_wage_l <= max_base_wage):
        ssc_w_calc = ssc_rate * income_wage_l
    elif (income_wage_l > max_base_wage):
        ssc_w_calc = max_ssc
    return ssc_w_calc

"Calculation for Social Security Contribution (SSC) without cap"  
@iterate_jit(nopython=True)
def cal_ssc_w_rem_cap(ssc_w, income_wage_l, ssc_rate, min_base_wage, max_base_wage, min_ssc, max_ssc, ssc_w_rem_cap):
    """
    Compute ssc for wages.
    """
    """ Note : First condition: Case when SSC is zero (e.g Exemption from SSC for TIDZ or no income from wages);
    Second condition:Case when gross income from wages is below minimum wages;
    Third condition: Case when gross income from wages is range between minium and maximum wages an
    Fourth condition:Case when gross income from wages is above maximum wages.
    note: income_wage_l = gross income for wages
    """
    if (ssc_w ==0 and income_wage_l > 0):     #ssc in cases where wage income is non-zero but ssc as per data is zero is deemed zero
        ssc_w_rem_cap = 0 
    elif (income_wage_l < min_base_wage):
        ssc_w_rem_cap = min_ssc
    elif (income_wage_l >= min_base_wage) and (income_wage_l <= max_base_wage):
        ssc_w_rem_cap = ssc_rate * income_wage_l
    elif (income_wage_l > max_base_wage):
        ssc_w_rem_cap = ssc_rate * income_wage_l
    return ssc_w_rem_cap




"Calculation for Social Security Contribution (SSC)"  
@iterate_jit(nopython=True)
def cal_ssc_inc_temp_fun(ssc_w, income_contract_l, ssc_rate, min_base_wage, max_base_wage, min_ssc, max_ssc, cal_ssc_inc_temp_calc):
    """
    Compute ssc for wages.
    """
    """ Note : First condition: Case when SSC is zero (e.g Exemption from SSC for TIDZ or no income from wages);
    Second condition:Case when gross income from wages is below minimum wages;
    Third condition: Case when gross income from wages is range between minium and maximum wages an
    Fourth condition:Case when gross income from wages is above maximum wages.
    note: income_wage_l = gross income for wages
    """
    if (ssc_w > 0 and income_contract_l > 0):     #ssc in cases where wage income is non-zero but ssc as per data is zero is deemed zero
        cal_ssc_inc_temp_calc = 0
    elif (income_contract_l < min_base_wage):
        cal_ssc_inc_temp_calc = min_ssc
    elif (income_contract_l >= min_base_wage) and (income_contract_l <= max_base_wage):
        cal_ssc_inc_temp_calc = ssc_rate * income_contract_l
    elif (income_contract_l > max_base_wage):
        cal_ssc_inc_temp_calc = max_ssc
    return cal_ssc_inc_temp_calc
	

"Calculation SSC with or without CAP"
@iterate_jit(nopython=True)
def cal_ssc_total(exclude_cap, ssc_w_rem_cap,ssc_w_calc,total_ssc_w):
     if exclude_cap == 1:
        total_ssc_w = ssc_w_rem_cap 
     else :
        total_ssc_w = ssc_w_calc
     return total_ssc_w


"Calculation for personal allowance - default rate of personal allowance is 100%, which can be changed in reform"
@iterate_jit(nopython=True)
def cal_personal_allowance_new(rate_personal_allowance_w, personal_allowance_w, personal_allowance_new):
    personal_allowance_new = personal_allowance_w * rate_personal_allowance_w
    return personal_allowance_new

# "Calculation for tax base for wages"
# #we can introduce the same condition that income_salary_l> and add all the other exemptions
# @iterate_jit(nopython=True)
# def cal_tax_base_w(income_wage_l, ssc_w_calc, personal_allowance_new):
#     tax_base_w = income_wage_l - ssc_w_calc - personal_allowance_new
#     tax_base_w = max(tax_base_w, 0.)
#     return tax_base_w

"Calculation for tax base for wages"
#we can introduce the same condition that income_salary_l> and add all the other exemptions
@iterate_jit(nopython=True)
def cal_tax_base_w(income_wage_l, total_ssc_w, personal_allowance_new):
    tax_base_w = income_wage_l - total_ssc_w - personal_allowance_new
    tax_base_w = max(tax_base_w, 0.)
    return tax_base_w

  
"Calculation for PIT from wages only"
@iterate_jit(nopython=True)
def cal_pit_w(tax_base_w, rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tax_base_w  
    
    pit_w = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))
        
    return (pit_w)
    

"Calculating the Tax Expenditure"
@iterate_jit(nopython=True)
def cal_expenditure_w(pit_w, te_disable_unemp, te_special_comp, te_TIDZ, te):
    if te_disable_unemp==0.0 and te_special_comp==0.0 and te_TIDZ==0.0:
        te = 0.
    te = pit_w
    return(te)

"Calculation of deductions from income from agriculture/medicine"

@iterate_jit(nopython=True)
def cal_deductions_income_agr_med_l(rate_ded_income_agr_med_l, income_agr_med_l, deductions_income_agr_med_l):
    deductions_income_agr_med_l = rate_ded_income_agr_med_l * income_agr_med_l
    return deductions_income_agr_med_l

"Calculation for tax base for income from agriculture/medicine - after deductions "
@iterate_jit(nopython=True)
def cal_tax_base_agr(income_agr_med_l, deductions_income_agr_med_l):
    tax_base_agr = income_agr_med_l - deductions_income_agr_med_l
    return tax_base_agr
   
"Calculation for tax base for temp income"
#we can introduce the same condition that income_salary_l> and add all the other exemptions
@iterate_jit(nopython=True)
def cal_tax_inc_temp(income_contract_l, cal_ssc_inc_temp_calc,ssc_temp_rate):
    tax_base_inc_temp = income_contract_l - (cal_ssc_inc_temp_calc *ssc_temp_rate)
    tax_base_inc_temp = max(tax_base_inc_temp, 0.)
    return tax_base_inc_temp


                       
# "Calculation for tax base for other labor income" 
# @iterate_jit(nopython=True)
# def cal_tax_base_other(tax_base_agr, income_add_l, income_supvr_l, income_officials_l, 
#                         income_jury_l, income_manu_l, income_contract_l, tax_base_other):
#     tax_base_other = (tax_base_agr + income_add_l + income_supvr_l + income_officials_l + 
#                       income_jury_l + income_manu_l + income_contract_l)
#     tax_base_other = max(tax_base_other, 0.)
#     return tax_base_other

    "Calculation for tax base for other labor income" 
@iterate_jit(nopython=True)
def cal_tax_base_other(tax_base_agr,tax_base_inc_temp, income_add_l, income_supvr_l, income_officials_l, 
                        income_jury_l, income_manu_l, tax_base_other):
    tax_base_other = (tax_base_agr + income_add_l + income_supvr_l + income_officials_l + 
                      income_jury_l + income_manu_l + tax_base_inc_temp)
    tax_base_other = max(tax_base_other, 0.)
    return tax_base_other

 
"Calculation for total tax base from labor - sum of tax base wages and other labour income "
@iterate_jit(nopython=True)
def cal_tti_w_I(tax_base_w, tax_base_other,tti_w_I):
    tti_w_I = tax_base_w + tax_base_other
    return tti_w_I

"Calculation for incorporating behavior - uses tax elasticity of total tax from labour income "
"Elasticity = % Change in income / % Change in tax rate "

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
    #elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
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
    
"Calculation for PIT from labor income incorporating behaviour"
@iterate_jit(nopython=True)
def cal_pit_w_I(tti_w_I_behavior, rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, pit_w_I):
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


"Calculation for tax base from capital - income from interest and dividends against which no deduction is allowed"
@iterate_jit(nopython=True)
def cal_tti_wd(income_dividends_c, income_interest_c, tti_wd):
    tti_wd = (income_dividends_c + income_interest_c)
    return (tti_wd)

"Calculation of deduction against income from property/rental income"
"Deduction from rental income is at different rates depending on whether property is rented out for business or non-business purpose"
"If proof of actual cost incurred is available actual cost is deductible"
@iterate_jit(nopython=True)
def cal_deduction_rental_income_c(rate_rent_house_business_c,rate_rent_non_house_business_c,rent_house_business,
                                  rent_non_house_business,rent_actual_costing,
                                  rent_actual_cost,income_prop_c,deductions_rental_income_c):
    if rent_house_business:
        deductions_rental_income_c = rate_rent_house_business_c * income_prop_c
    elif rent_non_house_business:
        deductions_rental_income_c = rate_rent_non_house_business_c * income_prop_c 
    elif rent_actual_costing:
        deductions_rental_income_c = rent_actual_cost
        
    return deductions_rental_income_c
        
"Calculation for tax base for capital income from copyrights income"
"Deduction rate is different for different source of capital income"
@iterate_jit(nopython=True)
def cal_deduction_copyrights_income_c(rate_income_sculpture_c,rate_income_artistic_photography_c,
                                      rate_income_paintings_c,rate_income_music_ballet_c,
                                      rate_income_translations_lectures_c, rate_income_stage_music_c,
                                      rate_income_copyrights_other_c, income_sculpture,
                                      income_artistic_photography, income_paintings,
                                      income_music_ballet, income_translations_lectures,
                                      income_stage_music, income_copyrights_other,
                                      income_copyrights_actual_costing, income_copyrights_actual_cost,
                                      income_copyrights_c, deductions_copyrights_income_c):
    if income_sculpture:
        deductions_copyrights_income_c = rate_income_sculpture_c * income_copyrights_c
    elif income_artistic_photography:
        deductions_copyrights_income_c = rate_income_artistic_photography_c * income_copyrights_c
    elif income_paintings:
        deductions_copyrights_income_c = rate_income_paintings_c * income_copyrights_c
    elif income_music_ballet:
        deductions_copyrights_income_c = rate_income_music_ballet_c * income_copyrights_c
    elif income_translations_lectures:
        deductions_copyrights_income_c = rate_income_translations_lectures_c * income_copyrights_c
    elif income_stage_music:
        deductions_copyrights_income_c = rate_income_stage_music_c * income_copyrights_c
    elif income_copyrights_other:
        deductions_copyrights_income_c = rate_income_copyrights_other_c * income_copyrights_c
    elif income_copyrights_actual_costing:
        deductions_copyrights_income_c = income_copyrights_actual_cost
    return deductions_copyrights_income_c


"Calculation of deduction from income other than capital income"
@iterate_jit(nopython=True)
def cal_deduction_income_other_c(rate_income_claimed_other_c,
                                 income_claimed_other_c, income_other_c,
                                 deductions_income_other_claimed_c, deductions_income_other_c):
    if income_claimed_other_c == 1: 
        deductions_income_other_c = rate_income_claimed_other_c * income_other_c
    else:
        deductions_income_other_c = deductions_income_other_claimed_c
    return deductions_income_other_c
  
"Calculation for total tax base from capital income OTHER THAN games of chance"
@iterate_jit(nopython=True)
def cal_tti_c_a(income_prop_c, deductions_rental_income_c, tti_wd, income_copyrights_c, deductions_copyrights_income_c, 
                income_other_c, deductions_income_other_c, tti_c_a):
    income_prop = income_prop_c -deductions_rental_income_c
    income_copyrights = income_copyrights_c - deductions_copyrights_income_c
    income_other = income_other_c - deductions_income_other_c
    # If inter-head loss allowed to be adjusted then add all above income(loss) and calculate net income from capital
    tti_c_a = tti_wd + income_prop + income_copyrights + income_other
    tti_c_a = max(tti_c_a, 0.)
    return(tti_c_a)

"Calculation for total tax base from capital income from games of chance"
@iterate_jit(nopython=True)
def cal_tti_c_g(income_gamesch_c,exemption_income_gamesch_c, tti_c_g):
    tti_c_g = income_gamesch_c - exemption_income_gamesch_c
    tti_c_g = max(tti_c_g, 0.)
    return(tti_c_g)

"Calculation for total tax base from capital income"
@iterate_jit(nopython=True)
def cal_tti_c(tti_c_a , tti_c_g, tti_c ):
    tti_c = tti_c_a + tti_c_g
    return(tti_c)


"Calculation behavior"
@iterate_jit(nopython=True)
def cal_tti_c_behavior(capital_income_rate_a, capital_income_rate_a_curr_law,
                      capital_income_rate_g, capital_income_rate_g_curr_law,
                      elasticity_pit_capital_income_threshold,
                      elasticity_pit_capital_income_value,
                      tti_c_a, tti_c_g, tti_c, tti_c_a_behavior, tti_c_g_behavior):
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
    
    frac_change_net_of_pit_capital_income_rate_a = ((1-capital_income_rate_a)-(1-capital_income_rate_a_curr_law))/(1-capital_income_rate_a_curr_law)
    frac_change_tti_c_a = elasticity*(frac_change_net_of_pit_capital_income_rate_a) 
    frac_change_net_of_pit_capital_income_rate_g = ((1-capital_income_rate_g)-(1-capital_income_rate_g_curr_law))/(1-capital_income_rate_g_curr_law)
    frac_change_tti_c_g = elasticity*(frac_change_net_of_pit_capital_income_rate_g)   
    tti_c_a_behavior = tti_c_a*(1+frac_change_tti_c_a)    
    tti_c_g_behavior = tti_c_g*(1+frac_change_tti_c_g)
    return tti_c_a_behavior, tti_c_g_behavior

"Calculation for PIT from capital"
@iterate_jit(nopython=True)
def cal_pit_c(capital_income_rate_a, capital_income_rate_g, tti_c_a_behavior, tti_c_g_behavior, pit_c):
    pit_c = (tti_c_a_behavior*capital_income_rate_a) + (tti_c_g_behavior*capital_income_rate_g)
    return pit_c


"Calculation for net income from labor"
@iterate_jit(nopython=True)
def cal_net_w_I(tti_w_I, pit_w_I, net_w_I):
    """
    net income from wages/salary and other labor income
    """
    net_w_I = tti_w_I-pit_w_I
    return net_w_I

"Calculation for net income from capital"
@iterate_jit(nopython=True)
def cal_net_c(tti_c, pit_c, net_c):
    """
    net income from capital
    """
    net_c = tti_c-pit_c
    return net_c

"total"
@iterate_jit(nopython=True)
def cal_total_gross_income(income_wage_l, income_add_l, income_supvr_l, income_officials_l, income_jury_l,
                           income_manu_l, income_contract_l, income_agr_med_l, income_prop_c,
                           income_copyrights_c, income_dividends_c, income_interest_c, income_gamesch_c,     
                           income_other_c, total_gross_income):
    """
    Compute total gross income.
    """
    total_gross_income = (income_wage_l + income_add_l + income_supvr_l + income_officials_l +
    income_jury_l + income_manu_l + income_contract_l + income_agr_med_l + income_prop_c + 
    income_copyrights_c + income_dividends_c + income_interest_c + income_gamesch_c + income_other_c)
    return total_gross_income

@iterate_jit(nopython=True)
def cal_total_taxable_income(tti_w_I, tti_c, total_taxable_income):
    """
    Compute total taxable income.
    """
    total_taxable_income = tti_w_I + tti_c
    return total_taxable_income


@iterate_jit(nopython=True)
def cal_total_pit(pit_w_I, pit_c, pitax):
    """
    Compute PIT.
    """
    pitax = pit_w_I + pit_c
    return pitax

@iterate_jit(nopython=True)
def cal_total_net_income(net_w_I, net_c, total_net_income):
    """
    Compute net income.
    """
    total_net_income = net_w_I + net_c
    return total_net_income

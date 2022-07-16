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


"Calculation for minumum annual threshold for social payment"
@iterate_jit(nopython=True)
def cal_min_social_base(monthly_income_threshold,min_threshold_social_p):
   min_threshold_social_p = monthly_income_threshold*12
   return (min_threshold_social_p)

"Calculation for maximum annual threshold for social payment"
@iterate_jit(nopython=True)
def cal_max_social_base(min_monthly_salary,max_threshold_social_p):
   max_threshold_social_p = (min_monthly_salary*15)*12  
   return (max_threshold_social_p)

"Deduction annual amount for social payment"
@iterate_jit(nopython=True)
def cal_deduction_social(deduction_monthly_social_p,deduction_amount_social_p):
   deduction_amount_social_p = deduction_monthly_social_p*12
   return (deduction_amount_social_p)

"Calculation for tax base for wages"
@iterate_jit(nopython=True)
def cal_tax_base_s(salary, civil_contract,base_social):
    base_social=salary + civil_contract
    return (base_social)

"Calculation of annual cap for social payment"
@iterate_jit(nopython=True)
def cal_cap_social_p(max_cap_monthly_social_p,max_cap_social_p):
    max_cap_social_p=max_cap_monthly_social_p*12
    return (max_cap_social_p)


"Calculation of Social payments"
@iterate_jit(nopython=True)
def cal_ssc_fun(social_fee,min_threshold_social_p,max_threshold_social_p,max_cap_social_p,rate_sp_1,rate_sp_2,deduction_amount_social_p,base_social,cal_ssc):    
    """ Note:  
            Hint: Please note, that the social security scheme is mandatory for all the taxpayers born after 1974, and it is voluntary for others born before 1974.
            
             1.Base for social payment :
              
              The base for calculation of the social payment is the basic income, which is salary and other payments equal thereto which are subject to taxation by income tax.
              The Employer, as a tax agent, is obliged to withhold the amount of social payment as well as submit monthly personalized reports to the tax authorities on calculated income, amounts of tax and social payments withheld from individuals within the terms established by the RA Tax Code.
              The social payment rates are as follows:
                  
                     Basic monthly Income*             Social payment
             2021   Up to AMD 500,000                   3.5 %
                    More than AMD 500,000              10 % - AMD 32,500
                     
             2022  Up to AMD 500,000                     4.5 %
                   More than AMD 500,000                10 % - AMD 27,500     
                     
             2023  Up to AMD 500,000                     5 %
                   More than AMD 500,000                10 % - AMD 25,000            
                     
              Starting 01.07.2020 the maximum monthly threshold of the calculation basis for social payment is AMD 1,020,000. This means that the maximum amount of the Social Payment in 2021 will be capped at AMD.69,500. (Source https://home.kpmg/xx/en/home/insights/2021/07/armenia-thinking-beyond-borders.html)
                
              
              2.Rule for calculation Social security contributions for 2021 :
               
              Individuals born after 1 January 1974 must make social security payments at a rate of 3.5 % on their salary and equivalent income and income from the provision of services, in a case where the income is less than or equal to AMD 500,000. 
              If the salary and equivalent income or income from the provision of services is between AMD 500,000 and AMD 1,020,000 (the latter amount is calculated as 15 times the minimum monthly salary (AMD 68,000)), 
              the social security contribution is calculated as 10% on the gross income minus AMD 32,500. Where the relevant income is equal to or exceeds AMD 1,020,000, the social security contribution is calculated 
              as 10% on AMD 1,020,000 minus AMD 32,500. Individuals have the right to waive the maximum threshold for social security payments.(Source:https://www2.deloitte.com/content/dam/Deloitte/global/Documents/Tax/dttl-tax-armeniahighlights-2021.pdf)
    
    """
    
    if social_fee ==0 and base_social> 1:
       calc_ssc = 0
    elif base_social < min_threshold_social_p: 
       calc_ssc = base_social*rate_sp_1  
    elif (base_social >=min_threshold_social_p) and ( base_social <=max_threshold_social_p): 
       calc_ssc =  (base_social * rate_sp_2)-deduction_amount_social_p 
    elif base_social > max_threshold_social_p:
       calc_ssc = max_cap_social_p  
    return  (cal_ssc)



"Calculation for tax base for wages"
@iterate_jit(nopython=True)
def cal_tax_base_b(salary, civil_contract,other_income,deduction,calculation_base):
    calculation_base=(salary + civil_contract + other_income)-deduction
    return (calculation_base)


"Calculation for PIT from salaires,civil contracts, other income"
@iterate_jit(nopython=True)
def cal_pit_fun(calculation_base,rate1,rate2,rate3,rate4,tbrk1,tbrk2,tbrk3,pit_calc):
    """
        Note: 
             From 1 January 2020, a FLAT RATE of income tax on salaries was established, which will gradually decrease to 20 percent by 2023: 
      
             Period                                                         Income tax rate
          From 1 January 2020                                                    23 %
          From 1 January 2021                                                    22 %
          From 1 January 2022                                                    21%
          From 1 January 2023                                                    20 %
        
        (Source https://home.kpmg/xx/en/home/insights/2021/07/armenia-thinking-beyond-borders.html)
        
        Individual - Deductions
        
        Employment expenses
        Deductions from gross income for employees may include the following:
        Paid benefits, except benefits defined by the Law of Armenia on Temporary Disability Benefits etc. 
        More information on https://taxsummaries.pwc.com/armenia/individual/deductions
    
    """   
    
    pit_calc = (rate1 * min(calculation_base, tbrk1) +
                            rate2 * min(tbrk2 - tbrk1, max(0., calculation_base - tbrk1)) +
                            rate3 * min(tbrk3 - tbrk2, max(0., calculation_base - tbrk2)) +
                            rate4 * max(0., calculation_base - tbrk3))
    
        
    return (pit_calc)
    

"Calculating the Tax Expenditure"
@iterate_jit(nopython=True)
def cal_tax_expenditure(income_tax,amount_rcvd,pit_calc, te):
    """
    Note: Tax Expendutures from Global Tax Expenditures Database  
    
    Detected tax expenditures :
       Income tax expenses: Agriculture
       Income  tax expenses: Dividends
       Income tax: the salary of agricultural workers
       Income tax: micro business
       Income tax: IT Business
       Income tax: refund for mortgage interest servicing
 
    At the moment this information are not avilable in sample 2021.

    (Source: https://gted.net/country-profile/?country=ARM)
    """  
    if income_tax==0.0 and amount_rcvd==0.0 :
        te = 0.
    te = pit_calc
    return(te)

                       

"Calculation for total tax base from labor - sum of tax base wages and other labour income "
@iterate_jit(nopython=True)
def cal_tti_w_I(calculation_base,tti_w_I):
    tti_w_I = calculation_base #+ tax_base_other
    return (tti_w_I)

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
    return (tti_w_I_behavior)
    
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



@iterate_jit(nopython=True)
def cal_total_pit(pit_calc,pit_w_I,cal_ssc,pitax):
    """
    Explanation about total PIT calculation
    
    Gross amount of income tax:
    ------------------------------------------------------------------
    Employment contracts, civil contracts, and other incomes = 396.64
    Other sources of income (royalties, interest incomes etc.) = 44.56
    Temporary disability benefits=15.10
    Income declared by individuals (residents and nonresidents)= 2.70
    -----------------------------------------------------------------
    Total gross amount of income tax  = 459 
    
    Cash back from income tax:	
    -----------------------------------------------------------------
    Mortgage 	-22.70
    Dividends	-9.40
    Tuition fee 	-0.20
    -----------------------------------------------------------------
    Total cash back of income tax = 32.3
    
    
    Annual PIT amount, reported on the State Revenue Committee’s official website
    -----------------------------------------------------------------
    Net PIT= 459-32.3= 426.70 (bln. AMD)
    
    """
    
    pitax = pit_w_I 
   
    return (pitax)


@iterate_jit(nopython=True)
def cal_total_net_income(total_income, cal_ssc, pitax, total_net_income):
    """
    Compute net income.
    """
    total_net_income = total_income-(cal_ssc + pitax)
    return total_net_income

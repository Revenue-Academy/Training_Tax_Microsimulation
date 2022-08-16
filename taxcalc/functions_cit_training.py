"""
Functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def Net_accounting_profit(Revenues, Other_revenues, Expenses, Net_accounting_profit):
    """
    Compute accounting profit from business
    """
    Net_accounting_profit = Revenues + Other_revenues - Expenses
    return Net_accounting_profit


@iterate_jit(nopython=True)
def Total_additions_to_GP(Donations_NGO, Donations_Others, Donations_Govt, Other_additions, Total_additions_to_GP):
    """
    Compute accounting profit from business
    """
    Total_additions_to_GP = Donations_NGO + Donations_Others + Donations_Govt + Other_additions
    return Total_additions_to_GP

@iterate_jit(nopython=True)
def Total_taxable_profit(Net_accounting_profit, Total_additions_to_GP, Total_taxable_profit):
    """
    Compute total taxable profits afer adding back non-allowable deductions.
    """
    Total_taxable_profit = Net_accounting_profit + Total_additions_to_GP
    return Total_taxable_profit

@iterate_jit(nopython=True)
def Op_WDV_depr(Op_WDV_Bld, Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp):
    """
    Return the opening WDV of each asset class.
    """
    Op_WDV_Bld, Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp = (Op_WDV_Bld, 
    Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp)
    return (Op_WDV_Bld, Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp)

@iterate_jit(nopython=True)
def Tax_depr_Bld(Op_WDV_Bld, Add_Bld, Excl_Bld, rate_depr_bld, Tax_depr_Bld):
    """
    Compute tax depreciation of building asset class.
    """
    Tax_depr_Bld = max(rate_depr_bld*(Op_WDV_Bld + Add_Bld - Excl_Bld),0)
    return Tax_depr_Bld

@iterate_jit(nopython=True)
def Tax_depr_Intang(Op_WDV_Intang, Add_Intang, Excl_Intang, rate_depr_intang, Tax_depr_Intang):
    """
    Compute tax depreciation of intangibles asset class
    """
    Tax_depr_Intang = max(rate_depr_intang*(Op_WDV_Intang + Add_Intang - Excl_Intang),0)
    return Tax_depr_Intang

@iterate_jit(nopython=True)
def Tax_depr_Mach(Op_WDV_Mach, Add_Mach, Excl_Mach, rate_depr_mach, Tax_depr_Mach):
    """
    Compute tax depreciation of Machinary asset class
    """
    Tax_depr_Mach = max(rate_depr_mach*(Op_WDV_Mach + Add_Mach - Excl_Mach),0)
    return Tax_depr_Mach

@iterate_jit(nopython=True)
def Tax_depr_Others(Op_WDV_Others, Add_Others, Excl_Others, rate_depr_others, Tax_depr_Others):
    """
    Compute tax depreciation of Other asset class
    """
    Tax_depr_Others = max(rate_depr_others*(Op_WDV_Others + Add_Others - Excl_Others),0)
    return Tax_depr_Others

@iterate_jit(nopython=True)
def Tax_depr_Comp(Op_WDV_Comp, Add_Comp, Excl_Comp, rate_depr_comp, Tax_depr_Comp):
    """
    Compute tax depreciation of Computer asset class
    """
    Tax_depr_Comp = max(rate_depr_comp*(Op_WDV_Comp + Add_Comp - Excl_Comp),0)
    return Tax_depr_Comp

@iterate_jit(nopython=True)
def Tax_depreciation(Tax_depr_Bld, Tax_depr_Intang, Tax_depr_Mach, Tax_depr_Others, Tax_depr_Comp, Tax_depr):
    """
    Compute total depreciation of all asset classes.
    """
    Tax_depr = Tax_depr_Bld + Tax_depr_Intang + Tax_depr_Mach + Tax_depr_Others + Tax_depr_Comp
    return Tax_depr

@iterate_jit(nopython=True)
def Cl_WDV_depr(Op_WDV_Bld, Add_Bld, Excl_Bld, Tax_depr_Bld, 
                Op_WDV_Intang, Add_Intang, Excl_Intang, Tax_depr_Intang,
                Op_WDV_Mach, Add_Mach, Excl_Mach, Tax_depr_Mach,
                Op_WDV_Others, Add_Others, Excl_Others, Tax_depr_Others,
                Op_WDV_Comp, Add_Comp, Excl_Comp, Tax_depr_Comp,
                Cl_WDV_Bld, Cl_WDV_Intang, Cl_WDV_Mach, Cl_WDV_Others, Cl_WDV_Comp):
    """
    Compute Closing WDV of each block of asset.
    """
    Cl_WDV_Bld = max((Op_WDV_Bld + Add_Bld - Excl_Bld),0) - Tax_depr_Bld
    Cl_WDV_Intang = max((Op_WDV_Intang + Add_Intang - Excl_Intang),0) - Tax_depr_Intang
    Cl_WDV_Mach = max((Op_WDV_Mach + Add_Mach - Excl_Mach),0) - Tax_depr_Mach
    Cl_WDV_Others = max((Op_WDV_Others + Add_Others - Excl_Others),0) - Tax_depr_Others
    Cl_WDV_Comp= max((Op_WDV_Comp + Add_Comp - Excl_Comp),0) - Tax_depr_Comp
    return (Cl_WDV_Bld, Cl_WDV_Intang, Cl_WDV_Mach, Cl_WDV_Others, Cl_WDV_Comp)

@iterate_jit(nopython=True)
def Total_deductions(Tax_depr, Other_deductions, Donations_Govt, Donations_Govt_rate, Total_deductions):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Total_deductions = Tax_depr + Other_deductions + (Donations_Govt_rate*Donations_Govt)
    return Total_deductions

@iterate_jit(nopython=True)
def Net_taxable_profit(Total_taxable_profit, Total_deductions, Net_taxable_profit):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Net_taxable_profit = Total_taxable_profit - Total_deductions
    return Net_taxable_profit

@iterate_jit(nopython=True)
def Donations_allowed(Donations_NGO, Donations_Others, Donations_NGO_rate, Net_taxable_profit, Donations_Others_rate, Donations_allowed):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Donations_allowed = min(Donations_NGO, max(0, Donations_NGO_rate*Net_taxable_profit)) + Donations_Others_rate*Donations_Others
    return Donations_allowed

@iterate_jit(nopython=True)
def Carried_forward_losses(Carried_forward_losses, CF_losses):
    """
    Compute net taxable profits afer allowing deductions.
    """
    CF_losses = Carried_forward_losses
    return CF_losses

@iterate_jit(nopython=True)
def Tax_base_CF_losses(Net_taxable_profit, Donations_allowed, Loss_CFLimit, CF_losses,
    Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, Loss_lag6, Loss_lag7, Loss_lag8,
    newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8, Used_loss_total, Tax_base):
    
    """
    Compute net tax base afer allowing donations and losses.
    """
    BF_loss = np.array([Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, Loss_lag6, Loss_lag7, Loss_lag8])
    
    Gross_Tax_base = min(Net_taxable_profit, max((Net_taxable_profit - Donations_allowed), 0))

    if BF_loss.sum() == 0:
        BF_loss[0] = CF_losses

    N = int(Loss_CFLimit)
    if N == 0:
        (newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8) = np.zeros(8)
        Used_loss_total = 0
        Tax_base = Gross_Tax_base
        
    else:
        BF_loss = BF_loss[:N]
                
        if Gross_Tax_base < 0:
            CYL = abs(Gross_Tax_base)
            Used_loss = np.zeros(N)
        elif Gross_Tax_base >0:
            CYL = 0
            Cum_used_loss = 0
            Used_loss = np.zeros(N)
            for i in range(N, 0, -1):
                GTI = Gross_Tax_base - Cum_used_loss
                Used_loss[i-1] = min(BF_loss[i-1], GTI)
                Cum_used_loss += Used_loss[i-1]
        elif Gross_Tax_base == 0:
            CYL=0
            Used_loss = np.zeros(N)
    
        New_loss = BF_loss - Used_loss
        Tax_base = Gross_Tax_base - Used_loss.sum()
        newloss1 = CYL
        Used_loss_total = Used_loss.sum()
        (newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8) = np.append(New_loss[:-1], np.zeros(8-N))

    return (Tax_base, newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8, Used_loss_total)


@iterate_jit(nopython=True)
def Net_tax_base(Tax_base, cit_rate_oil, Sector_Code, Exemptions, Investment_incentive, Net_tax_base):
    """
    Compute net tax base afer allowing donations and losses.
    """
    if Sector_Code == 2:
        Net_tax_base = Tax_base/(1 - cit_rate_oil)
    else:
        Net_tax_base = Tax_base - Exemptions - Investment_incentive
    return Net_tax_base

@iterate_jit(nopython=True)
def Net_tax_base_behavior(cit_rate_oil, cit_rate_hotels, cit_rate_banks,
                                cit_rate_oil_curr_law, cit_rate_hotels_curr_law,
                                cit_rate_banks_curr_law, cit_rate_genbus, 
                                cit_rate_genbus_curr_law, elasticity_cit_taxable_income_threshold,
                                elasticity_cit_taxable_income_value, Net_tax_base, 
                                Net_tax_base_behavior):
    """
    Compute net taxable profits afer allowing deductions.
    """
    NP = Net_tax_base   
    elasticity_taxable_income_threshold0 = elasticity_cit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_cit_taxable_income_threshold[1]
    elasticity_taxable_income_threshold2 = elasticity_cit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_cit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_cit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_cit_taxable_income_value[2]
    if NP<=0:
        elasticity=0
    elif NP<elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif NP<elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    else:
        elasticity=elasticity_taxable_income_value2

    frac_change_net_of_cit_rate_oil = ((1-cit_rate_oil)-(1-cit_rate_oil_curr_law))/(1-cit_rate_oil_curr_law)
    frac_change_Net_tax_base_oil = elasticity*(frac_change_net_of_cit_rate_oil)
    frac_change_net_of_cit_rate_hotels = ((1-cit_rate_hotels)-(1-cit_rate_hotels_curr_law))/(1-cit_rate_hotels_curr_law)
    frac_change_Net_tax_base_hotels = elasticity*(frac_change_net_of_cit_rate_hotels)
    frac_change_net_of_cit_rate_banks = ((1-cit_rate_banks)-(1-cit_rate_banks_curr_law))/(1-cit_rate_banks_curr_law)
    frac_change_Net_tax_base_banks = elasticity*(frac_change_net_of_cit_rate_banks)
    frac_change_net_of_cit_rate_genbus = ((1-cit_rate_genbus)-(1-cit_rate_genbus_curr_law))/(1-cit_rate_genbus_curr_law)
    frac_change_Net_tax_base_genbus = elasticity*(frac_change_net_of_cit_rate_genbus)    
    Net_tax_base_behavior = Net_tax_base*(1+frac_change_Net_tax_base_oil+frac_change_Net_tax_base_hotels+frac_change_Net_tax_base_banks+frac_change_Net_tax_base_genbus)
    return Net_tax_base_behavior

@iterate_jit(nopython=True)
def Net_tax_base_Egyp_Pounds(Net_tax_base_behavior, Exchange_rate, Net_tax_base_Egyp_Pounds):
    """
    Compute net tax base afer allowing donations and losses.
    """
    Net_tax_base_Egyp_Pounds = Net_tax_base_behavior * Exchange_rate
    return Net_tax_base_Egyp_Pounds

DEBUG = False
DEBUG_IDX = 0

@iterate_jit(nopython=True)
def mat_liability(mat_rate, Net_accounting_profit, MAT):
    """
    Compute tax liability given the corporate rate
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    MAT = mat_rate*Net_accounting_profit
        
    return MAT

@iterate_jit(nopython=True)
def cit_liability(cit_rate_oil, cit_rate_hotels, cit_rate_banks, cit_rate_genbus, Sector_Code, Net_tax_base_Egyp_Pounds, MAT, citax):
    """
    Compute tax liability given the corporate rate
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = max(Net_tax_base_Egyp_Pounds, 0)
    if Sector_Code == 0:
        citax = cit_rate_hotels * taxinc
    elif Sector_Code == 1:
        citax = cit_rate_banks * taxinc
    elif Sector_Code == 2:
        citax = cit_rate_oil * taxinc
    elif Sector_Code == 3:
        citax = cit_rate_genbus * taxinc
        
    if MAT>citax:
        citax=MAT
        
    return citax





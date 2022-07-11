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

@iterate_jit(nopython=True)
def calc_EmpInc(EmpIncRemuneration,TerminalBenefit,EmpInc):
    EmpInc = EmpIncRemuneration+TerminalBenefit 
    return EmpInc

@iterate_jit(nopython=True)
def calc_BussInc(BussIncDomestic,BussIncForeign,BussInc):
    BussInc = BussIncDomestic+BussIncForeign    
    return BussInc

@iterate_jit(nopython=True)
def calc_InvestIncome(InterestIncomeSenior,RentalIncome,
                      InvestIncomeOther, InvestIncome):
    InvestIncome = (InterestIncomeSenior+RentalIncome+
                    InvestIncomeOther)
    return InvestIncome

@iterate_jit(nopython=True)
def calc_OtherIncome(OtherIncomeNonBetting,OtherIncomeBetting,OtherIncome):
    OtherIncome = (OtherIncomeNonBetting+OtherIncomeBetting)
    return OtherIncome

@iterate_jit(nopython=True)
def calc_AssessibleIncome(EmpInc,BussInc,InvestIncome,
                          OtherIncome, AssessibleIncome):
    AssessibleIncome = EmpInc+BussInc+InvestIncome+OtherIncome    
    #print(AssessibleIncome)
    return AssessibleIncome

@iterate_jit(nopython=True)
def calc_ReliefEmpIncome(ReliefEmpIncome,EmpInc,ReliefEmpIncomeAllowed):
    ReliefEmpIncomeAllowed = min(EmpInc,ReliefEmpIncome)
    #print(ReliefEmpIncome)
    #print(ReliefEmpIncomeAllowed)   
    return ReliefEmpIncomeAllowed

@iterate_jit(nopython=True)
def calc_ReliefForeignIncome(ReliefForeignIncome, BussIncForeign,
                             ReliefForeignIncomeAllowed):
    ReliefForeignIncomeAllowed = min(ReliefForeignIncome,BussIncForeign)  
    return ReliefForeignIncomeAllowed

@iterate_jit(nopython=True)
def calc_ReliefRentalIncome(percent_ReliefRentalIncome, ceiling_ReliefRentalIncome,
                            RentalIncome, ReliefForeignIncomeAllowed):
    ReliefRentalIncome = percent_ReliefRentalIncome*RentalIncome
    ReliefRentalIncomeAllowed = min(ceiling_ReliefRentalIncome,ReliefRentalIncome)  
    return ReliefRentalIncomeAllowed

@iterate_jit(nopython=True)
def calc_ReliefInterestIncome(ReliefInterestIncome, InterestIncomeSenior,
                             ReliefInterestIncomeAllowed):
    ReliefInterestIncomeAllowed = min(ReliefInterestIncome,InterestIncomeSenior)   
    return ReliefInterestIncomeAllowed

@iterate_jit(nopython=True)
def calc_PersonalRelief(PersonalRelief, AssessibleIncome, ReliefEmpIncomeAllowed,
                        ReliefForeignIncomeAllowed, ReliefRentalIncomeAllowed, 
                        ReliefInterestIncomeAllowed, PersonalReliefAllowed):
    AssessibleIncome_remaining = (AssessibleIncome-(ReliefEmpIncomeAllowed+
                                  ReliefForeignIncomeAllowed+
                                  ReliefRentalIncomeAllowed+
                                  ReliefInterestIncomeAllowed))
    AssessibleIncome_remaining = max(0,AssessibleIncome_remaining) 
    PersonalReliefAllowed = min(PersonalRelief,AssessibleIncome_remaining)
    return PersonalReliefAllowed

@iterate_jit(nopython=True)
def calc_TotalRelief(ReliefEmpIncomeAllowed, ReliefForeignIncomeAllowed, 
                     ReliefRentalIncomeAllowed, ReliefInterestIncomeAllowed,
                     PersonalReliefAllowed, TotalRelief):
    TotalRelief = (ReliefEmpIncomeAllowed+
                                  ReliefForeignIncomeAllowed+
                                  ReliefRentalIncomeAllowed+
                                  ReliefInterestIncomeAllowed+
                                  PersonalReliefAllowed)
    #print(TotalRelief)
    return TotalRelief

@iterate_jit(nopython=True)
def calc_QualifyingPaymentAllowed(ceiling_Donations, percent_DonationsAllowed,
                                  Donations,AssessibleIncome, TotalRelief,
                                  QualifyingPaymentAllowed):
    AssessibleIncome_remaining = (AssessibleIncome-TotalRelief)
    AssessibleIncome_remaining = max(0,AssessibleIncome_remaining)
    DonationsAllowed = percent_DonationsAllowed*AssessibleIncome
    DonationsAllowed = min(DonationsAllowed,ceiling_Donations)
    DonationsAllowed = min(Donations, DonationsAllowed)
    QualifyingPaymentAllowed = min(DonationsAllowed,AssessibleIncome_remaining)
    return QualifyingPaymentAllowed

@iterate_jit(nopython=True)
def calc_TotalDudAsseIncome(AssessibleIncome,TotalRelief, QualifyingPaymentAllowed,
                            TotalDudAsseIncome):
    TotalDudAsseIncome = (TotalRelief+QualifyingPaymentAllowed)
    return TotalDudAsseIncome

@iterate_jit(nopython=True)
def calc_TaxableIncome(AssessibleIncome,TotalDudAsseIncome):
    TaxableIncome =	max(0, AssessibleIncome-TotalDudAsseIncome)
    #print(TaxableIncome)
    return TaxableIncome

@iterate_jit(nopython=True)
def calc_TaxTerminalBenefit(rate_TerminalBenefit, TerminalBenefit):
    TaxTerminalBenefit = rate_TerminalBenefit*TerminalBenefit
    return TaxTerminalBenefit

@iterate_jit(nopython=True)
def calc_TaxIncomeBetting(rate_IncomeBetting, OtherIncomeBetting):
    TaxIncomeBetting = rate_IncomeBetting*OtherIncomeBetting
    return TaxIncomeBetting

@iterate_jit(nopython=True)
def calc_CapitalGains(rate_Capital_Gains, CapitalGains, TaxRealizationIncAsset):
    TaxRealizationIncAsset = rate_Capital_Gains*CapitalGains
    return TaxRealizationIncAsset

@iterate_jit(nopython=True)
def calc_BalanceIncome(TaxableIncome, TerminalBenefit, CapitalGains,
                       BalanceIncome):
    BalanceIncome = TaxableIncome-TerminalBenefit-CapitalGains
    return BalanceIncome

@iterate_jit(nopython=True)
def calc_BalanceIncomeProgressive(BalanceIncome, OtherIncomeBetting,tti):
    BalanceIncomeProgressive = BalanceIncome - OtherIncomeBetting
    tti=BalanceIncomeProgressive
    return tti

"Calculation for incorporating behavior - uses tax elasticity of total tax from labour income "
"Elasticity = % Change in income / % Change in tax rate "
@iterate_jit(nopython=True)
def calc_tti_behavior(rate1, rate2, rate3, rate4, rate5, rate6, 
                     tbrk1, tbrk2, tbrk3, tbrk4, tbrk5,
                     rate1_curr_law, rate2_curr_law, rate3_curr_law, 
                     rate4_curr_law, rate5_curr_law, rate6_curr_law,
                     tbrk1_curr_law, tbrk2_curr_law, tbrk3_curr_law,
                     tbrk4_curr_law, tbrk5_curr_law, 
                     elasticity_pit_taxable_income_threshold,
                     elasticity_pit_taxable_income_value, tti,
                     BalanceIncomeProgressiveBehavior):
    """
    Compute taxable total income after adjusting for behavior.
    """  
    elasticity_taxable_income_threshold0 = elasticity_pit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_pit_taxable_income_threshold[1]
    #elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_pit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_pit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_pit_taxable_income_value[2]
    if tti<=0:
        elasticity=0
    elif tti<elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif tti<elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    else:
        elasticity=elasticity_taxable_income_value2

    if tti<0:
        marg_rate=0
    elif tti<=tbrk1:
        marg_rate=rate1
    elif tti<=tbrk2:
        marg_rate=rate2
    elif tti<=tbrk3:
        marg_rate=rate3
    else:        
        marg_rate=rate4

    if tti<0:
        marg_rate_curr_law=0
    elif tti<=tbrk1_curr_law:
        marg_rate_curr_law=rate1_curr_law
    elif tti<=tbrk2_curr_law:
        marg_rate_curr_law=rate2_curr_law
    elif tti<=tbrk3_curr_law:
        marg_rate_curr_law=rate3_curr_law
    else:        
        marg_rate_curr_law=rate4_curr_law
    
    frac_change_net_of_pit_rate = ((1-marg_rate)-(1-marg_rate_curr_law))/(1-marg_rate_curr_law)
    frac_change_tti = elasticity*(frac_change_net_of_pit_rate)  
    tti_behavior = tti*(1+frac_change_tti)
    BalanceIncomeProgressiveBehavior = tti_behavior
    return BalanceIncomeProgressiveBehavior
    
"Calculation for PIT from labor income incorporating behaviour"
@iterate_jit(nopython=True)
def calc_pit_progressive(BalanceIncomeProgressiveBehavior, rate1, rate2, rate3, rate4, rate5, rate6, 
            tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, TaxBalanceIncomeProgressive):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = BalanceIncomeProgressiveBehavior  
    
    TaxBalanceIncomeProgressive = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * min(tbrk4 - tbrk3, max(0., taxinc - tbrk3)) +
                    rate5 * min(tbrk5 - tbrk4, max(0., taxinc - tbrk4)) +
                    rate6 * max(0., taxinc - tbrk5))
        
    return (TaxBalanceIncomeProgressive)

@iterate_jit(nopython=True)
def calc_TaxBalanceIncome(TaxBalanceIncomeProgressive, TaxIncomeBetting,tti):
    TaxBalanceIncome = TaxBalanceIncomeProgressive + TaxIncomeBetting
    return TaxBalanceIncome

@iterate_jit(nopython=True)
def calc_TotalTaxPayable(TaxTerminalBenefit,TaxRealizationIncAsset,
                          TaxBalanceIncome,TaxFinalWHTCages180, pitax):
    TotalTaxPayable = (TaxTerminalBenefit+TaxRealizationIncAsset+
                       TaxBalanceIncome+TaxFinalWHTCages180)
    pitax = TotalTaxPayable
    return pitax


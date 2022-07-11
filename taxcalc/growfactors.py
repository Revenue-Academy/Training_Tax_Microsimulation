"""
Tax-Calculator GrowFactors class.
"""
# CODING-STYLE CHECKS:
# pycodestyle growfactors.py
# pylint --disable=locally-disabled growfactors.py

import os
import json
import numpy as np
import pandas as pd
from taxcalc.utils import read_egg_csv


class GrowFactors(object):
    """
    Constructor for the GrowFactors class.

    Parameters
    ----------
    growfactors_filename: string
        string is name of CSV file in which grow factors reside;
        default value is name of file containing baseline grow factors.

    Raises
    ------
    ValueError:
        if growfactors_filename is not a string.

    Returns
    -------
    class instance: GrowFactors

    Notes
    -----
    Typical usage is "gfactor = GrowFactors()", which produces an object
    containing the default grow factors in the GrowFactors.FILENAME file.
    """

    f = open('global_vars.json')
    global_variables = json.load(f)
 
    #print("global_variables in growfactors", global_variables)

    GROWFACTORS_FILENAME = global_variables['GROWFACTORS_FILENAME']
    
    CUR_PATH = os.path.abspath(os.path.dirname(__file__))
    #FILENAME = 'growfactors.csv'
    FILE_PATH = os.path.join(CUR_PATH, GROWFACTORS_FILENAME)

    # TODO: Growfactors for Corporate and non-corporate Income heads are
    # TODO: currently set as same. New field names should be read in case we
    # TODO: want separate growfactors for Corporate and Non-corporate data.
    if (global_variables['pit']):
        f = open(os.path.join(CUR_PATH, global_variables['pit_records_variables_filename']))
        records_variables = json.load(f)
        set1 = set(records_variables['read'].keys())
    else:
        set1 = set()
    if (global_variables['cit']):
        f = open(os.path.join(CUR_PATH, global_variables['cit_records_variables_filename']))
        corprecords_variables = json.load(f)
        set2 = set(corprecords_variables['read'].keys())        
    else:
        set2 = set()
    if (global_variables['vat']):    
        f = open(os.path.join(CUR_PATH, global_variables['vat_records_variables_filename']))
        gstrecords_variables = json.load(f)
        set3 = set(gstrecords_variables['read'].keys())         
    else:
        set3 = set()    

    set4 = set(['CPI', 'SALARY'])
    set5 = set(['CONSUMPTION', 'OTHER_CONS_ITEM'])
    VALID_NAMES = set.union(set1, set2, set3, set4, set5)
    """
    VALID_NAMES = set(['CPI', 'SALARY', 'RENT', 'BP_NONSPECULATIVE',
                       'BP_SPECULATIVE', 'BP_SPECIFIED', 'BP_PATENT115BBF',
                       'STCG_APPRATE', 'OINCOME', 'DEDUCTIONS',
                       'DEDU_SEC_10A_OR_10AA', 'ST_CG_AMT_1',
                       'ST_CG_AMT_2', 'LT_CG_AMT_1', 'LT_CG_AMT_2',
                       'LOSSES_CY', 'LOSSES_BF', 'AGRI_INCOME', 'CORP',
                       'INVESTMENT', 'CONSUMPTION', 'OTHER_CONS_ITEM'])
    """
    def __init__(self, growfactors_filename=GROWFACTORS_FILENAME):
        f = open('global_vars.json')
        global_variables = json.load(f)
        self.verbose = global_variables['verbose']
        growfactors_filename = global_variables['GROWFACTORS_FILENAME']
        # read grow factors from specified growfactors_filename
        gfdf = pd.DataFrame()
        CUR_PATH = os.path.abspath(os.path.dirname(__file__))
        #FILENAME = 'growfactors.csv'
        growfactors_filepath = os.path.join(CUR_PATH, growfactors_filename)
        #print('growfactors_filepath ', growfactors_filepath)
        if isinstance(growfactors_filepath, str):
            if os.path.isfile(growfactors_filepath):
                gfdf = pd.read_csv(growfactors_filepath,
                                   index_col='Year')
            else:
                # cannot call read_egg_ function in unit tests
                gfdf = read_egg_csv(GrowFactors.GROWFACTORS_FILENAME,
                                    index_col='Year')  # pragma: no cover
        else:
            raise ValueError('growfactors_filename is not a string')
        assert isinstance(gfdf, pd.DataFrame)
        # check validity of gfdf column names
        gfdf_names = set(list(gfdf))
        #print(GrowFactors.GROWFACTORS_FILENAME)
        #print("gfdf_names: ", gfdf_names)
        #print("GrowFactors.VALID_NAMES: ", GrowFactors.VALID_NAMES)
        if not gfdf_names.issubset(GrowFactors.VALID_NAMES):
        #if gfdf_names != GrowFactors.VALID_NAMES:
            msg = ('missing names are: {} and invalid names are: {}')
            missing = GrowFactors.VALID_NAMES - gfdf_names
            invalid = gfdf_names - GrowFactors.VALID_NAMES
            if self.verbose:
                print("Record Variables not in Grow Factors File are", missing)
                print("Non-Standard variables are declared", invalid)
            #raise ValueError(msg.format(missing, invalid))
        # determine first_year and last_year from gfdf
        #self._first_year = min(gfdf.index)
        #self._last_year = max(gfdf.index)
        self._first_year = int(global_variables['data_start_year'])
        self._last_year = int(global_variables['end_year'])  
        # set gfdf as attribute of class
        self.gfdf = pd.DataFrame()
        #setattr(self, 'gfdf', gfdf.astype(np.float64))  # pylint: disable=no-member
        setattr(self, 'gfdf', gfdf)  # pylint: disable=no-member
        #print(self.gfdf)
        del gfdf
        # specify factors as being unused (that is, not yet accessed)
        self.used = False

    @property
    def first_year(self):
        """
        GrowFactors class start_year property.
        """
        return self._first_year

    @property
    def last_year(self):
        """
        GrowFactors class last_year property.
        """
        return self._last_year

    def price_inflation_rates(self, firstyear, lastyear):
        """
        Return list of price inflation rates rounded to four decimal digits.
        """
        self.used = True
        if firstyear > lastyear:
            msg = 'first_year={} > last_year={}'
            raise ValueError(msg.format(firstyear, lastyear))
        if firstyear < self.first_year:
            msg = 'firstyear={} < GrowFactors.first_year={}'
            raise ValueError(msg.format(firstyear, self.first_year))
        if lastyear > self.last_year:
            msg = 'last_year={} > GrowFactors.last_year={}'
            raise ValueError(msg.format(lastyear, self.last_year))

        #print(self.gfdf)
        # pylint: disable=no-member
        rates = [round((self.gfdf['CPI'][cyr] - 1.0), 4)
                 for cyr in range(firstyear, lastyear + 1)]
        return rates

    def wage_growth_rates(self, firstyear, lastyear, SALARY_VARIABLE):
        """
        Return list of wage growth rates rounded to four decimal digits.
        """
        self.used = True
        if firstyear > lastyear:
            msg = 'firstyear={} > lastyear={}'
            raise ValueError(msg.format(firstyear, lastyear))
        if firstyear < self.first_year:
            msg = 'firstyear={} < GrowFactors.first_year={}'
            raise ValueError(msg.format(firstyear, self.first_year))
        if lastyear > self.last_year:
            msg = 'lastyear={} > GrowFactors.last_year={}'
            raise ValueError(msg.format(lastyear, self.last_year))
        # pylint: disable=no-member
        rates = [round((self.gfdf[SALARY_VARIABLE][cyr] - 1.0), 4)
                 for cyr in range(firstyear, lastyear + 1)]
        return rates

    def factor_value(self, name, year, attribute_name=None, attribute_value=None):
        """
        Return value of factor with specified name for specified year.
        """
        self.used = True
        if name not in GrowFactors.VALID_NAMES:
            msg = 'name={} not in GrowFactors.VALID_NAMES'
            raise ValueError(msg.format(year, name))
        if year < self.first_year:
            msg = 'year={} < GrowFactors.first_year={}'
            raise ValueError(msg.format(year, self.first_year))
        if year > self.last_year:
            msg = 'year={} > GrowFactors.last_year={}'
            raise ValueError(msg.format(year, self.last_year))
        if attribute_name is None:
            #print('self.gfdf ', self.gfdf)
            #print('self.gfdf[name][year] ', self.gfdf[name][year])
            return self.gfdf[name][year]
        else:
            #print('self.gfdf ', self.gfdf)
            #print(self.gfdf[attribute_name]==attribute_value)
            #print('col ', name)
            #print('year ', year)
            #print('attribute_name ', attribute_name)
            #print('attribute_value ', attribute_value)
            #print('self.gfdf[self.gfdf[attribute_name]==attribute_value][name][year] ', 
                  #self.gfdf[self.gfdf[attribute_name]==attribute_value][name][year])
            return self.gfdf[self.gfdf[attribute_name]==attribute_value][name][year]

    def factor_names(self):
        """
        Return value of factor with specified name for specified year.
        """
        self.used = True
        return set(self.gfdf.columns)
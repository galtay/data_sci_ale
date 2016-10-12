"""
CMS provides data on the geographic variation in the utilization and quality
of health care services,

https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Geographic-Variation/GV_PUF.html

This module handles the State/County level table (more to be added).  The class
handles CSV files that are generated from the excel file
(see `convert_geo_var_state_county_to_csv.py`)

State level data includes all 50 states +
 - District of Columbia (DC)
 - Puerto Rico (PR)
 - US Virgin Islands (VI)
 - ??? (XX) maybe this means outside the US ?
"""

import os
import time
import pandas
import us_states


VALID_LEVELS = ['national', 'state', 'county']
DEFAULT_CSV_FNAME = './data/County_All_Table_2014.csv'


class CmsGeoVarCountyTable:
    """Class to handle Geographic Variation Public Use Files (State/County)"""


    def __init__(self, csv_fname=DEFAULT_CSV_FNAME, verbose=False):
        """Initialize class with a CSV file name, it is read into a DataFrame.
        """
        self.verbose = verbose
        if self.verbose: print('csv fname: {}'.format(csv_fname))
        self.df = pandas.read_csv(csv_fname)


    def select_rows(self, level, exclude=None):
        """Return a selection of rows from the total DataFrame.

        Args:
          level (str): the selection of rows to return.  One of
            ['national', 'state', 'county']
          exclude (list of str): a list of either states or counties
            to exclude from the retuned DataFrame

        Returns:
          DataFrame: Selected rows from the full DataFrame
        """
        if level not in VALID_LEVELS:
            raise ValueError('level must be one of {}'.format(VALID_LEVELS))
        if exclude is None:
            exclude = []
        if level == 'national':
            return self._select_national_row()
        elif level == 'state':
            return self._select_state_rows(exclude=exclude)
        elif level == 'county':
            return self._select_county_rows(exclude=exclude)


    def _select_national_row(self):
        """Select row that represents the national total."""
        bmask = self.df['State']=='National'
        return self.df[bmask].iloc[0]


    def _select_state_rows(self, exclude=None):
        """Select rows that represent individual states.

        By default state abbreviations 'XX', 'DC', 'PR', and 'VI' will be
        included.  The `exclude` keyword can be set to a list of strings
        to remove a set of state abbreviations from the return value.
        """
        if exclude is None:
            exclude = []
        bmask = self.df['County'] == 'STATE TOTAL'
        bmask = bmask & ~(self.df['State'].isin(exclude))
        return self.df[bmask]


    def _select_county_rows(self, exclude=None):
        """Select rows that represent individual counties.

        By default state abbreviations 'XX', 'DC', 'PR', and 'VI' will be
        included.  The `exclude` keyword can be set to a list of strings
        to remove a set of counties from the return value.

        Note that some states don't have county level data ('XX', 'PR', VI').
        In that case the return value will contain the single state total row.
        """
        if exclude is None:
            exclude = []

        # get states that only have state level data
        grpd_df = self.df.groupby('State').size()
        single_row_states = grpd_df[grpd_df==1].index.tolist()
        single_row_states.remove('National')

        # is a single row state
        bmask1 = self.df['State'].isin(single_row_states)
        # is not a single row state and is not a state total
        bmask2 = ~bmask1 & (self.df['County'] != 'STATE TOTAL')
        # is not a national total
        bmask3 = self.df['State'] != 'National'
        # is not in county exclude list
        bmask4 = ~(self.df['County'].isin(exclude))

        bmask = (bmask1 | bmask2) & bmask3 & bmask4
        return self.df[bmask]


    def return_feature_cols(self):
        """Return a list of column names that could be plausible features
        for a learning model.  For example we choose 'standardized' and
        'per capita' type columns.
        """

        #===========================================
        # Demographics features
        #===========================================
        demographics = [
            'MA Participation Rate',
            'Average Age',
            'Percent Female',
            'Percent Male',
            'Percent Eligible for Medicaid',
            'Average HCC Score',
        ]

        #===========================================
        # Total Cost features
        #===========================================
        total_costs = [
            'Actual Per Capita Costs',
            'Standardized Per Capita Costs',
            'Standardized Risk-Adjusted Per Capita Costs',
        ]

        #===========================================
        # Service-Level Costs and Utilization
        #===========================================
        slcu_dict = {}

        # All categories have these columns
        #===========================================
        slcu_categories = [
            'IP', 'PAC: LTCH', 'PAC: IRF', 'PAC: SNF', 'PAC: HH',
            'Hospice', 'OP', 'FQHC/RHC', 'Outpatient Dialysis Facility',
            'ASC', 'E&M', 'Procedures', 'Imaging', 'DME', 'Tests',
            'Part B Drugs', 'Ambulance']
        slcu_lines = [
            '{} Standardized Costs as % of Total Standardized Costs',
            '{} Per Capita Standardized Costs',
            '{} Per User Standardized Costs',
            '% of Beneficiaries Using {}',
        ]

        for cat in slcu_categories:
            cols = [line.format(cat) for line in slcu_lines]
            slcu_dict[cat] = cols

        # Covered Stays
        #===========================================
        slcu_categories = ['IP', 'PAC: LTCH', 'PAC: IRF', 'PAC: SNF', 'Hospice']
        slcu_line = '{} Covered Stays Per 1000 Beneficiaries'
        for cat in slcu_categories:
            slcu_dict[cat].append(slcu_line.format(cat))

        # Covered Days
        #===========================================
        slcu_categories = ['IP', 'PAC: LTCH', 'PAC: IRF', 'PAC: SNF', 'Hospice']
        slcu_line = '{} Covered Days Per 1000 Beneficiaries'
        for cat in slcu_categories:
            slcu_dict[cat].append(slcu_line.format(cat))

        # Visits
        #===========================================
        slcu_categories = ['PAC: HH', 'OP', 'FQHC/RHC']
        slcu_line = '{} Visits Per 1000 Beneficiaries'
        for cat in slcu_categories:
            slcu_dict[cat].append(slcu_line.format(cat))

        # Events
        #===========================================
        slcu_categories = [
            'Outpatient Dialysis Facility', 'ASC', 'E&M',
            'Procedures', 'Imaging', 'DME', 'Tests', 'Ambulance']
        slcu_line = '{} Events Per 1000 Beneficiaries'
        for cat in slcu_categories:
            slcu_dict[cat].append(slcu_line.format(cat))

        # fix plurality
        slcu_dict['Procedures'][-1] = (
            slcu_dict['Procedures'][-1].replace('Procedures', 'Procedure'))
        slcu_dict['Tests'][-1] = (
            slcu_dict['Tests'][-1].replace('Tests', 'Test'))

        #===========================================
        # Readmissions and ED Visits
        #===========================================
        readmission_ed = [
            'Hospital Readmission Rate',
            'Emergency Department Visits per 1000 Beneficiaries',
        ]

        #===========================================
        # Combine all into a list of  feature columns
        #===========================================
        feature_cols = []
        feature_cols += demographics
        feature_cols += total_costs
        # Service-Level Costs and Utilization
        feature_cols += slcu_dict['IP']
        feature_cols += slcu_dict['PAC: LTCH']
        feature_cols += slcu_dict['PAC: IRF']
        feature_cols += slcu_dict['PAC: SNF']
        feature_cols += slcu_dict['PAC: HH']
        feature_cols += slcu_dict['Hospice']
        feature_cols += slcu_dict['OP']
        feature_cols += slcu_dict['FQHC/RHC']
        feature_cols += slcu_dict['Outpatient Dialysis Facility']
        feature_cols += slcu_dict['ASC']
        feature_cols += slcu_dict['E&M']
        feature_cols += slcu_dict['Procedures']
        feature_cols += slcu_dict['Imaging']
        feature_cols += slcu_dict['DME']
        feature_cols += slcu_dict['Tests']
        feature_cols += slcu_dict['Part B Drugs']
        feature_cols += slcu_dict['Ambulance']
        # Readmissions and ED visits
        feature_cols += readmission_ed


        return feature_cols


def check_state_totals_sum_to_national(df_state_totals, ser_national):
    """Check that summing the state level rows recovers the national total"""
    state_sum = df_state_totals['Total Actual Costs'].sum()
    national_total = ser_national['Total Actual Costs']
    print('state sum vs national total')
    print('state sum: {}'.format(state_sum))
    print('national: {}'.format(national_total))
    print(state_sum/national_total)
    print()


def check_county_totals_sum_to_national(df_county_totals, ser_national):
    """Check that summing the county level rows recovers the national total"""
    county_sum = df_county_totals['Total Actual Costs'].sum()
    national_total = ser_national['Total Actual Costs']
    print('county sum vs national total')
    print('county sum: {}'.format(county_sum))
    print('national: {}'.format(national_total))
    print(county_sum/national_total)
    print()



if __name__ == '__main__':

    fname = './data/County_All_Table_2014.csv'
    gvct = CmsGeoVarCountyTable(fname, verbose=True)
    st = gvct.select_rows('state')
    ct = gvct.select_rows('county')
    nt = gvct.select_rows('national')

    check_state_totals_sum_to_national(st, nt)
    check_county_totals_sum_to_national(ct, nt)

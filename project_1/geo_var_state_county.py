"""
CMS provides data on the geographic variation in the utilization and quality
of health care services,

https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Geographic-Variation/GV_PUF.html

This module handles the State/County level table (more to be added).


State level data includes all 50 states +
 - District of Columbia (DC)
 - Puerto Rico (PR)
 - US Virgin Islands (VI)
 - ??? (XX) maybe this means outside the US ?
"""


import time
import pandas
import us_states


class CmsGeoVarCountyTable:
    """Class to handle Geographic Variation Public Use Files (State/County)"""

    def __init__(self, fname, year=2014, verbose=False):
        """Read Excel file into DataFrame."""
        sheetname = 'State_county {}'.format(year)

        if verbose:
            print('reading file: {}, sheet: {}'.format(fname, sheetname))
            t1 = time.time()
        self._df = pandas.read_excel(
            fname, sheetname=sheetname, header=1, engine='xlrd',
            na_values=['.', '*'])
        if verbose:
            t2 = time.time()
            print('I/O took {} seconds'.format(t2-t1))

    def return_national(self):
        """Return a Series with national data"""
        bmask = self._df['State']=='National'
        return self._df[bmask].iloc[0]

    def return_state_totals(self, exclude=None):
        """Return a DataFrame with only state level rows.

        By default state abbreviations 'XX', 'DC', 'PR', and 'VI' will be
        included.  The `exclude` keyword can be set to a list of strings
        to remove a set of state abbreviations from the return value."""
        if exclude is None:
            exclude = []
        bmask = self._df['County'] == 'STATE TOTAL'
        bmask = bmask & ~(self._df['State'].isin(exclude))
        return self._df[bmask]

    def return_county_totals(self, st_exclude=None):
        """Return a DataFrame with only county level rows.

        By default state abbreviations 'XX', 'DC', 'PR', and 'VI' will be
        included.  The `st_exclude` keyword can be set to a list of strings
        to remove a set of state abbreviations from the return value.

        Note that some states don't have county level data ('XX', 'PR', VI').
        In that case the return value will contain the single state total row.
        """
        if st_exclude is None:
            st_exclude = []

        # get states that only have state level data
        grpd_df = self._df.groupby('State').size()
        single_row_states = grpd_df[grpd_df==1].index.tolist()
        single_row_states.remove('National')

        # is a single row state
        bmask1 = self._df['State'].isin(single_row_states)
        # is not a single row state and is not a state total
        bmask2 = ~bmask1 & (self._df['County'] != 'STATE TOTAL')
        # is not a national total
        bmask3 = self._df['State'] != 'National'
        # is not in state exclude list
        bmask4 = ~(self._df['State'].isin(st_exclude))

        bmask = (bmask1 | bmask2) & bmask3 & bmask4
        return self._df[bmask]



def check_state_totals_sum_to_national(df_state_totals, ser_national):
    state_sum = df_state_totals['Total Actual Costs'].sum()
    national_total = ser_national['Total Actual Costs']
    print('state sum vs national total')
    print('state sum: {}'.format(state_sum))
    print('national: {}'.format(national_total))
    print(state_sum/national_total)
    print()


def check_county_totals_sum_to_national(df_county_totals, ser_national):
    county_sum = df_county_totals['Total Actual Costs'].sum()
    national_total = ser_national['Total Actual Costs']
    print('county sum vs national total')
    print('county sum: {}'.format(county_sum))
    print('national: {}'.format(national_total))
    print(county_sum/national_total)
    print()



if __name__ == '__main__':

    fname = '/home/galtay/Downloads/cms_data/County_All_Table.xlsx'
    gvct = CmsGeoVarCountyTable(fname, verbose=True)
    st = gvct.return_state_totals()
    ct = gvct.return_county_totals()
    nt = gvct.return_national()

    check_state_totals_sum_to_national(st, nt)
    check_county_totals_sum_to_national(ct, nt)

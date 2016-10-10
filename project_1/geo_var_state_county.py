"""
CMS provides data on the geographic variation in the utilization and quality
of health care services,

https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Geographic-Variation/GV_PUF.html

This module handles the State/County level table (more to be added).  The class
includes functions to convert the excel files into CSV files for faster reading.

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


class CmsGeoVarCountyTable:
    """Class to handle Geographic Variation Public Use Files (State/County)"""

    def __init__(self, excel_fname, verbose=False):
        """Initialize class."""
        self.verbose = verbose
        if self.verbose: print('excel fname: {}'.format(excel_fname))
        self.excel_fname = excel_fname
        self.dirname = os.path.dirname(excel_fname)
        self.basename = os.path.basename(excel_fname)
        self.fbase, ext = self.basename.split('.')
        if ext != 'xlsx':
            raise IOError(
                'fname must end in "xlsx", got {}'.format(excel_fname))

    def gen_csv_fname(self, year):
        """Retrun a CSV file name given a year"""
        return '{}_{}.csv'.format(
            os.path.join(self.dirname, self.fbase), str(year))

    def write_all_csvs(self):
        """Find all sheet names and write them to CSV"""
        excel_file = pandas.ExcelFile(self.excel_fname)
        self.sheetnames = excel_file.sheet_names
        self.years = []
        for sheetname in self.sheetnames:
            if sheetname != 'Documentation':
                year = sheetname.split(' ')[-1]
                self.years.append(year)
                self.write_csv(year)

    def write_csv(self, year):
        """Read an Excel sheet and write it to CSV for quick reading later"""
        csv_fname = self.gen_csv_fname(year)
        sheetname = 'State_county {}'.format(year)
        if os.path.isfile(csv_fname):
            if self.verbose:
                print('csv file {} already exists, returning'.format(csv_fname))
            return
        if self.verbose:
            print('reading file: {}, sheet: {}'.format(fname, sheetname))
            t1 = time.time()
        df = pandas.read_excel(
            fname, sheetname=sheetname, header=1, engine='xlrd',
            na_values=['.', '*'])
        if self.verbose:
            t2 = time.time()
            print('I/O took {} seconds'.format(t2-t1))
            print('writing to {}'.format(csv_fname))
        df.to_csv(csv_fname)
        return df

    def read_csv(self, year):
        """Read a converted CSV file"""
        csv_fname = self.gen_csv_fname(year)
        df = pandas.read_csv(csv_fname)
        return df

    def return_national(self, df):
        """Return a Series with national data"""
        bmask = df['State']=='National'
        return df[bmask].iloc[0]

    def return_state_totals(self, df, exclude=None):
        """Return a DataFrame with only state level rows.

        By default state abbreviations 'XX', 'DC', 'PR', and 'VI' will be
        included.  The `exclude` keyword can be set to a list of strings
        to remove a set of state abbreviations from the return value."""
        if exclude is None:
            exclude = []
        bmask = df['County'] == 'STATE TOTAL'
        bmask = bmask & ~(df['State'].isin(exclude))
        return df[bmask]

    def return_county_totals(self, df, st_exclude=None):
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
        grpd_df = df.groupby('State').size()
        single_row_states = grpd_df[grpd_df==1].index.tolist()
        single_row_states.remove('National')

        # is a single row state
        bmask1 = df['State'].isin(single_row_states)
        # is not a single row state and is not a state total
        bmask2 = ~bmask1 & (df['County'] != 'STATE TOTAL')
        # is not a national total
        bmask3 = df['State'] != 'National'
        # is not in state exclude list
        bmask4 = ~(df['State'].isin(st_exclude))

        bmask = (bmask1 | bmask2) & bmask3 & bmask4
        return df[bmask]



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
    df = gvct.read_csv(2014)
    st = gvct.return_state_totals(df)
    ct = gvct.return_county_totals(df)
    nt = gvct.return_national(df)

    check_state_totals_sum_to_national(st, nt)
    check_county_totals_sum_to_national(ct, nt)

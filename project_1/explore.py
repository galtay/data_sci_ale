import pandas
import us_states

read_data = True

if read_data:
    fname = '/home/galtay/Downloads/cms_data/County_All_Table.xlsx'
    df_raw = pandas.read_excel(
        fname, sheetname='State_county 2014', header=1, engine='xlrd',
        na_values=['.', '*'])


    # get only state total rows (this sums up to national value)
    # and includes State=='XX'
    bmask = df_raw['County']=='STATE TOTAL'
    df_state_totals = df_raw[bmask]

    # mask out summary rows (i.e. national and state totals)
    # need to keep XX for this to match national total
    bmask1 = df_raw['State']=='XX'
    bmask2 = (df_raw['State']!='XX') & (df_raw['County']!='STATE TOTAL')
    bmask = bmask1 | bmask2


    # remove state entries we dont want
    bmask = ~df['State'].isin(['National', 'XX'])
    df = df[bmask]

    # remove STATE TOTAL entris
    bmask = ~(df['County']=='STATE TOTAL')
    df = df[bmask]



top_col_levels = [
    'Beneficiary Demographic Characteristics',
    'Total Costs',
    'Service-Level Costs and Utilization',
    'Readmissions and ED Visits',
    'Prevention Quality Indicators',
]



features = ['Standardized Risk-Adjusted Per Capita Costs']

frac_nan = df.isnull().sum() / df.shape[0]
dense_columns = frac_nan < 0.10


for st in df_raw['State'].unique():
    if st in us_states.STATES:
        bmask = (df_raw['State']==st) & (df_raw['County']=='STATE TOTAL')
        state_total = df_raw.loc[bmask, 'Total Actual Costs']

        bmask = (df_raw['State']==st) & (df_raw['County']!='STATE TOTAL')
        state_sum = df_raw.loc[bmask, 'Total Actual Costs'].sum()
        print('{} {} {}'.format(st, state_total, state_sum))
        print(state_total/state_sum)
        print()

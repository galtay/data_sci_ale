import time
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

import us_states
from geo_var_state_county import CmsGeoVarCountyTable

doio=False
if doio:
    fname = '/home/galtay/Downloads/cms_data/County_All_Table.xlsx'
    gvct = CmsGeoVarCountyTable(fname, verbose=True)


ct = gvct.return_county_totals()


# find columns for which less than 10% of the data is missing
frac_nan = ct.isnull().sum() / ct.shape[0]
dense_columns = frac_nan < 0.10


pair_cols = [
    'Average HCC Score',
    'Standardized Per Capita Costs',
    'Emergency Department Visits per 1000 Beneficiaries'
    ]

plt_df = ct[pair_cols].dropna()
plt_df.columns = ['Avg HCC', 'Cost/Person [$1k]', 'EDD/1000']
plt_df['Cost/Person [$1k]'] = plt_df['Cost/Person [$1k]'] * 1.0e-3
g = sns.pairplot(plt_df, size=4.0)
g.savefig('pairplot.png')

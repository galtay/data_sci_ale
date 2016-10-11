import pandas
import matplotlib.pyplot as plt
import seaborn as sns

import us_states
from geo_var_state_county import CmsGeoVarCountyTable



fname = './data/County_All_Table_2014.csv'
gvct = CmsGeoVarCountyTable(fname, verbose=True)
ct = gvct.return_county_totals()

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

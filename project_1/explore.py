import sys
import argparse

import pandas
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

import us_states
from geo_var_state_county import CmsGeoVarCountyTable


def make_pair_plot(fname, level):

    gvct = CmsGeoVarCountyTable(fname, verbose=True)
    df = gvct.select_rows(level)
    pair_cols = [
        'Average HCC Score',
        'Standardized Per Capita Costs',
        'Emergency Department Visits per 1000 Beneficiaries'
    ]

    plt_df = df[pair_cols].dropna()
    plt_df.columns = ['Avg HCC', 'Cost/Person [$1k]', 'EDD/10']
    plt_df['Cost/Person [$1k]'] = plt_df['Cost/Person [$1k]'] * 1.0e-3
    plt_df['EDD/10'] = plt_df['EDD/10'] * 1.0e-2

    n_levels = 5
    palette = list(reversed(sns.color_palette("Reds_d", n_levels)))
    my_cmap = ListedColormap(palette)

    g = sns.PairGrid(plt_df, size=2.5)
    g.map_diag(plt.hist)
    g.map_offdiag(plt.scatter, s=10, alpha=0.5)
    g.map_offdiag(sns.kdeplot, cmap=my_cmap, n_levels=n_levels);
    g.savefig('gvct_pairplot_{}.png'.format(level))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--fname',
        type=str,
        default='./data/County_All_Table_2014.csv',
        help='name of geographical variation state/county file')
    parser.add_argument(
        '--level',
        default='state',
        choices=['state', 'county'],
        help='rows to select from data')
    args = parser.parse_args()

    make_pair_plot(fname=args.fname, level=args.level)

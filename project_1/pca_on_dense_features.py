import pandas
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler

import us_states
from geo_var_state_county import CmsGeoVarCountyTable

fname = '/home/galtay/Downloads/cms_data/County_All_Table.xlsx'
gvct = CmsGeoVarCountyTable(fname, verbose=True)

df = gvct.read_csv(2014)
ct = gvct.return_county_totals(df)
nt = gvct.return_national(df)


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


# All services have these columns
#===========================================
slcu_cats = [
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

for cat in slcu_cats:
    cols = [line.format(cat) for line in slcu_lines]
    slcu_dict[cat] = cols

# Covered Stays
#===========================================
slcu_cats = ['IP', 'PAC: LTCH', 'PAC: IRF', 'PAC: SNF', 'Hospice']
slcu_line = '{} Covered Stays Per 1000 Beneficiaries'
for cat in slcu_cats:
    slcu_dict[cat].append(slcu_line.format(cat))

# Covered Days
#===========================================
slcu_cats = ['IP', 'PAC: LTCH', 'PAC: IRF', 'PAC: SNF', 'Hospice']
slcu_line = '{} Covered Days Per 1000 Beneficiaries'
for cat in slcu_cats:
    slcu_dict[cat].append(slcu_line.format(cat))

# Visits
#===========================================
slcu_cats = ['PAC: HH', 'OP', 'FQHC/RHC']
slcu_line = '{} Visits Per 1000 Beneficiaries'
for cat in slcu_cats:
    slcu_dict[cat].append(slcu_line.format(cat))

# Events
#===========================================
slcu_cats = [
    'Outpatient Dialysis Facility', 'ASC', 'E&M',
    'Procedures', 'Imaging', 'DME', 'Tests', 'Ambulance']
slcu_line = '{} Events Per 1000 Beneficiaries'
for cat in slcu_cats:
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
# Make list of feature columns
#===========================================

feature_cols = demographics + total_costs
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



# limit to dense columns
#==================================================
frac_thresh = 0.10
frac_nan = ct[feature_cols].isnull().sum() / ct.shape[0]
is_column_dense = frac_nan < frac_thresh
sparse_cols = is_column_dense[is_column_dense==False].index.tolist()
feature_cols = is_column_dense[is_column_dense==True].index.tolist()

# do some analysis
#==================================================
features = ct[feature_cols]

# replace missing values with column means
imp = Imputer()
X = imp.fit_transform(features)

# standardize columns
scaler = StandardScaler()
X = scaler.fit_transform(X)

# do PCA
pca = PCA()
pca.fit(X)
n = pca.n_components_

plt.figure()
plt.plot(
    pandas.np.arange(n)+1,
    pandas.np.cumsum(pca.explained_variance_ratio_),
    lw=3.0)
plt.xlim(0, n+1)
plt.ylim(-0.05, 1.05)
plt.xlabel('Principal Component')
plt.ylabel('Total Variance')
plt.savefig('pca_components_vs_total_variance.png')



Xpc = pca.transform(X)
plt.figure()
plt.scatter(Xpc[:,0], Xpc[:,1])
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.savefig('pca_components_2d.png')

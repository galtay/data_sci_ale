import pandas
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler

import us_states
from geo_var_state_county import CmsGeoVarCountyTable


fname = '/home/galtay/Downloads/cms_data/County_All_Table_2014.csv'
gvct = CmsGeoVarCountyTable(fname, verbose=True)
ct = gvct.return_county_totals()
nt = gvct.return_national()
feature_cols = gvct.return_feature_cols()


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

plt.figure(figsize=(6,6))
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
plt.figure(figsize=(6,6))
plt.scatter(Xpc[:,0], Xpc[:,1])
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.savefig('pca_components_2d.png')

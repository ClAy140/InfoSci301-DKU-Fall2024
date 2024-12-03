# import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import math
import argparse
from EDA import feature
import seaborn as sns
# data_path = 'Dataset/absentee_random_20000.csv'
data_path = 'Dataset/2016_random_20000_rows.csv'
data_random = pd.read_csv(data_path)
data_random_processed = feature(data_random)
print(data_random_processed.info())
print(data_random_processed['race'].value_counts())
print(data_random_processed['ethnicity'].value_counts())
# print(data_random_processed["voter_party_code"].value_counts())

'''
1. REP - Republican Party
2. DEM - Democratic Party
3. UNA - Unaffiliated or Independent
'''
sns.kdeplot(data=data_random_processed, x='age', hue='voter_party_code', fill=True, alpha=0.5)
plt.title('Age Distribution by Party')
plt.xlabel('Age')
plt.ylabel('Density')
plt.show()

# -*- coding: utf-8 -*-
"""DataMiningProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KMgoX9MEJEj2sadEhi_Jr8g2XkkOQ3Lx

Retrieve Data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import preprocessing
df = pd.read_csv("http://storm.cis.fordham.edu/~yli/data/tayko.csv")

#pd.set_option('precision',2)
#np.set_printoptions(precision=2)

#just to delete the spending anomaly, where purchase was 0 but spending was reported as 1. Note: only one customer had spending = 1 as well.
mask = df['Spending']==1
mask.sum()
for i in df[mask].index:
  df.loc[i,'Spending'] = 0

"""#Study of Characteristics"""

df.info()

df.head()

"""###Describing columns"""

#Characteristics 1 - 23
#ways to check all columns at once:
for column in df:
  print(df[column].describe())

"""###Checking for if any null"""

df.isnull().any()
#we actually don't even have to do this since df.info() tells us non-null count and they are all 2000
#none of the columns have null values

"""#####Removing columns that aren't useful"""

df = df.drop('last_update_days_ago', axis = 1)
df = df.drop('1st_update_days_ago', axis = 1)
df = df.drop('Purchase', axis = 1)
#df = df.drop('Partition', axis = 1)

#turn spending into categorical data
df['Spending'] = df['Spending'].astype('object')

"""###Graphs

######Box Plots
"""

#outliers in both Freq and Spending
df[['Freq','Spending']].plot.box(sharey=True, figsize=(15,10), title='box plots for freq and spending', whis = 1.5)

"""######Density Plots"""

fig, axs=plt.subplots(1,2,figsize=(22,5))
df['Freq'].plot.density(ax=axs[0], color='red',linestyle='--', title = 'Freq',xlim=(1,15))
df['Spending'].plot.density(ax=axs[1], color='black',linestyle='--', title = 'Spending',xlim=(0,1500))

fig, axs=plt.subplots(figsize=(30,5))
df['Spending'].plot.density(color='black',linestyle='--', title = 'Spending',xlim=(0,2000))

"""######Histogram Plots"""

fig, axs=plt.subplots(1,2,figsize=(15,4))
df['Freq'].plot.hist(ax=axs[0], color='red', title='Freq')
df['Spending'].plot.hist(ax=axs[1], color='black', title='Spending')

fig, axs=plt.subplots(figsize=(30,5))
df['Spending'].plot.hist(bins = 100, alpha=0.5, histtype='stepfilled', color='black', title = 'Spending',xlim=(0,1500))

df1 = df.copy(deep=True)

#df1 = df1[df1.Spending !=0]
df1.drop(df1.index[df1['Spending'] == 0], inplace=True)

df1['Spending'].where(df1['Spending']==0).sum()

fig, axs=plt.subplots(figsize=(30,5))
df1['Spending'].plot.hist(bins = 500, alpha=0.5, histtype='stepfilled', color='black', title = 'Spending',xlim=(0,1500))

sns.histplot(df1['Freq'], bins=50, color='green', kde=True)

sns.pairplot(df1[['Spending','Freq']])

sns.histplot(df1['Spending'], bins=50, color='green', kde=True)

df1

"""# Data Cleaning

###Binning

######Spending

Looking at the plots above, we want to bin spending into 4 groups:
1. group that spends 0
2. group that spends 1-300
3. group that spends 301-1000
4. group that spends >1000
"""

df1['ew_bin'] =pd.cut(df1['Spending'],4)
df1['ew_bin'].value_counts().sort_index()

df1['qbinned']=pd.qcut(df1['Spending'], 5)
df1['qbinned'].value_counts().sort_index()

df1.groupby('ew_bin')['Freq'].mean()

df1.groupby('qbinned')['Freq'].mean()

df1['binTest'] = pd.cut(x=df1['Spending'], bins=[0,100,400,1000,1600], labels=['1-100','101-400','401-1000','>1000'])

df1['binTest'].value_counts().sort_index()

df1.groupby('binTest').Freq.describe()

#binning
df['Spen_binned'] = pd.cut(x=df['Spending'], bins=[-1,0,300,1000,1600], labels=['0','1-300','301-1000','>1000'])

df.groupby('Spen_binned').Freq.describe()

df['Spen_binned'].describe()

"""######Freq"""

fig, axs=plt.subplots(figsize=(30,5))
df1['Freq'].plot.hist(bins = 30, alpha=0.5, histtype='stepfilled', color='black', title = 'Freq',xlim=(0,20))

df1['F_ew_bin'] =pd.cut(df1['Freq'],4)
df1['F_ew_bin'].value_counts().sort_index()

df1['F_ef_bin']=pd.qcut(df1['Freq'], 2)
df1['F_ef_bin'].value_counts().sort_index()

df1['F_binTest'] = pd.cut(x=df1['Freq'], bins=[0,2,7,16], labels=['1-2','3-7','>7'])

df1['F_binTest'].value_counts().sort_index()

df1

df['Freq_bin'] = pd.cut(x=df['Freq'], bins=[-1,0,2,7,16], labels=['0','1-2','3-7','>7'])

df

"""### Aggregate Columns

Combine source_ columns into one
"""

data = df.copy(deep = True)

conditions = [
              (data['source_a'] == 1),
              (data['source_c'] == 1),
              (data['source_b'] == 1),
              (data['source_d'] == 1),
              (data['source_e'] == 1),
              (data['source_m'] == 1),
              (data['source_o'] == 1),
              (data['source_h'] == 1),
              (data['source_r'] == 1),
              (data['source_s'] == 1),
              (data['source_t'] == 1),
              (data['source_u'] == 1),
              (data['source_p'] == 1),
              (data['source_x'] == 1),
              (data['source_w'] == 1)
]

values = ['A','C','B','D','E','M','O','H','R','S','T','U','P','X','W']
#values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

data['sourceALL'] = np.select(conditions, values)

data1 = data[['sourceALL','Freq','Web order','Gender=male','Address_is_res','Spending','Freq_bin','Spen_binned']]
data1

data1.loc[data1.sourceALL == '0', 'sourceALL'] = 'default'

data1['sourceALL'].describe()

data1.groupby('sourceALL').Freq.describe()
#some of the data doesnt belong to any source --> default source...
#H - highest Freq
#O - lowest Freq

#source H has the highest Freq but when we look at spending it's the lowest
#when Freq > 0 but spending == 0, means they bought stuff in the past

#A - highest average spending
#P - second highest avg spending
#H - lowest average spending
data1.groupby('sourceALL').Spending.describe()

data1.corr()

#sizeable correlation between Freq and Spending
data1.groupby('Freq').Spending.describe()

"""# Scaling Features

we are not going to normalize features since spending is categorical anyways
"""

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import cross_val_score #cross validation
from sklearn.model_selection import train_test_split #split the available dataset for training and testing

y_df = pd.DataFrame(['Freq', 'Web_'], columns=['class'])

"""#Feature Selection"""

#Correlation Matrix
X = df.iloc[:,0:20]  #independent columns
y = df.iloc[:,-1]    #target column i.e price range
corrmat = df.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(25,25))

#plot heat map
g=sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")

"""### Information Gain

"""

print('Data:', df.columns)

#for each unique item we will run through the list to get a count
def getProbs(feat):
  allProbs = []
  tol = len(df[feat])
  uniqueItems = df[feat].unique()

  for i in uniqueItems:
    count = 0
    for j in df[feat]:
      if j == i:
        count += 1
    #print(f'P({feat}={i})', ' = ', (count/tol))
    allProbs.append([i, (count/tol)])

  return(allProbs)

getProbs('Web order')
#getProbs('Purchase')
#getProbs('Spending')
test = getProbs('Freq')
print(test)

from pandas.core.arrays.numeric import T
import math
def infoD(feat):
  all = getProbs(feat)
  tol = 0
  for i in all:
    t = i[1]*(math.log2(i[1]))
    tol -= t
  return tol

print('Info(D) = ',infoD('Freq'))
print('Info(D) = ',infoD('Web order'))
print('Info(D) = ',infoD('Spending'))
print('Info(D) = ',infoD('Address_is_res'))



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import preprocessing
from sklearn.datasets import load_iris

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
#from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import BernoulliNB

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import OrdinalEncoder

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#df = pd.read_csv("http://storm.cis.fordham.edu/~yli/data/tayko.csv", index_col = 0)

pd.set_option('precision',2)
np.set_printoptions(precision=2)
#df = df.drop(['last_update_days_ago', '1st_update_days_ago'], axis = 1)

"""###Benchmark Model and Chi-Square and Mutual_Inforamtion Feature Selection Methods
Perform Gaussian Naive Bayes classification on original dataset.
"""

df_clean = df.drop(['Partition', 'Spen_binned', 'Freq_bin'], axis=1)
Telco_C={}
Telco_C['feature_names']= df_clean.columns.values
Telco_C['data']=df_clean.values
df_clean.head()

#spending binned
X = df.iloc[:,21:22]
Telco_C['target_names']=X['Spen_binned'].unique()
Telco_C['target']=X['Spen_binned'].values
Telco_C['target']
X.head()

#regular spending

#Y = df.iloc[:,22:23]
#Telco_C['target_names']=Y['Freq_bin'].unique()
#Telco_C['target']=Y['Freq_bin'].values
#Telco_C['target']

NB_G = GaussianNB()
NB_G_scores_old = cross_val_score(NB_G, Telco_C['data'], Telco_C['target'], cv=10,scoring='accuracy', error_score='raise')# default 5-fold

print(NB_G_scores_old)
print("Accuracy: %0.2f (+/- %0.2f)" % (NB_G_scores_old.mean(), NB_G_scores_old.std() * 2))

chi_selector = SelectKBest(chi2,k=5)
Telco_C['new_data_chi'] = chi_selector.fit_transform(Telco_C['data'], Telco_C['target'])
mask = chi_selector.get_support()
Telco_C['new_feature_names_chi']=Telco_C['feature_names'][mask]
Telco_C['new_data_chi'].shape

Telco_C['new_feature_names_chi'] #selected top 5 by performing chi2

mi_selector = SelectKBest(mutual_info_classif,k=5)
Telco_C['new_data_mi'] = chi_selector.fit_transform(Telco_C['data'], Telco_C['target'])
mask = chi_selector.get_support()
Telco_C['new_feature_names_mi']=Telco_C['feature_names'][mask]
Telco_C['new_data_mi'].shape

Telco_C['new_feature_names_mi']

set(Telco_C['new_feature_names_chi'])& set(Telco_C['new_feature_names_mi'])

scores_new_chi = cross_val_score(NB_G, Telco_C['new_data_chi'], Telco_C['target'],cv=10, scoring='accuracy')
print(scores_new_chi)
print('Accuracy: %0.2f (+/- %0.2f)' % (scores_new_chi.mean(),scores_new_chi.std()*2))

"""#Perform Naive Bayes classification on dataset with only selected 5 features.

#Naive Bayes

###Categorical Neive Bayes
###To-do bin Freq -- did it above in binning section
"""

from sklearn.datasets import load_iris

from sklearn.naive_bayes import GaussianNB
#from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import OrdinalEncoder

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
model = GaussianNB()

#bin Freq to use categorical nb
X = data1.iloc[:,1:8].drop(['Freq', 'Spending', 'Spen_binned'], axis = 1)
X.head()

Spending_Category = {}
Spending_Category['feature_names'] = X.columns.values

enc = OrdinalEncoder()
X = enc.fit_transform(X)
X

Spending_Category['data'] = X

Y = data1.iloc[:,7:8]
Y.head()
Spending_Category['target_names']=Y['Spen_binned'].unique()
Spending_Category['target']=Y['Spen_binned'].values

Spending_Category['target_names']

Spending_Category['target']

NB_C = CategoricalNB()

scores_NBC = cross_val_score(NB_C, Spending_Category['data'], Spending_Category['target'], cv=5, scoring='accuracy')
scores_NBC

print("Accuracy: %0.2f (+/- %0.2f)" % (scores_NBC.mean(), scores_NBC.std() * 2))

"""###Bernoulli Naive Bayes

BernoulliNB works on categorical values in binary format.

"""

X = df.iloc[:,15:22].drop(['Freq', 'Spending', 'Spen_binned', 'Partition'], axis = 1)
X = pd.get_dummies(X)
X.head()

"""BernoulliNB """

Computer = {} # a dictionary with key-value pairs 
Computer['feature_names'] = X.columns.values
Computer['data']=X.values
Computer['target_names']=Y['Spen_binned'].unique()
Computer['target']=Y['Spen_binned'].values


#Computer['target_names']=Y['Spen_binned'].unique()
#Computer['target']=Y['Spen_binned'].values

NB_B = BernoulliNB()#categorical binary format

scores_NBB = cross_val_score(NB_B, Computer['data'], Computer['target'], cv=5, scoring='accuracy')
scores_NBB

#mean and 95% confidence level
print("Accuracy: %0.2f (+/- %0.2f)" % (scores_NBB.mean(), scores_NBB.std() * 2))

y_predict= NB_B.fit(Computer['data'],Computer['target']).predict(Computer['data'])

df['predict']= y_predict
#df = df.drop('Partition', axis = 1)
#df = df.drop('Spending', axis = 1)
#df = df.drop('Freq', axis = 1)

y_predict= NB_C.fit(Spending_Category['data'],Spending_Category['target']).predict(Spending_Category['data'])
data1['predict']= y_predict

data1

"""Categorical Works better

#predicton tables
"""

data1.groupby('sourceALL')['predict'].describe()

data1.groupby('predict')['sourceALL'].describe()

data1.groupby('predict')['Freq'].describe()

data1.groupby('Freq')['predict'].describe()

data1.groupby('predict')['Freq_bin'].describe()

data1.groupby('Freq_bin')['predict'].describe()

data1.groupby('Gender=male')['predict'].describe()

data1.groupby('Web order')['predict'].describe()

data1.groupby('Address_is_res')['predict'].describe()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:18:28 2019

@author: cyfile
"""

import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import sklearn
from sklearn import metrics
from sklearn.metrics import calinski_harabasz_score
import matplotlib.pyplot as plt
import seaborn as sns

PCCR = pd.read_csv('cross_tablulate.csv', sep = ',') # import data

pccr = PCCR[['PCCR_OR_and_Anesth_Costs']].copy()
kmeans = KMeans(n_clusters=2).fit(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1))
labels = kmeans.labels_
pccr['clusters']=labels
chscore_2 = metrics.calinski_harabasz_score(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1),labels)#
print(chscore_2)

pccr = PCCR[['PCCR_OR_and_Anesth_Costs']].copy()
kmeans = KMeans(n_clusters=3).fit(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1))
labels = kmeans.labels_
pccr['clusters']=labels
chscore_3 = metrics.calinski_harabasz_score(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1),labels)
print(chscore_3)

pccr = PCCR[['PCCR_OR_and_Anesth_Costs']].copy()
kmeans = KMeans(n_clusters=4).fit(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1))
labels = kmeans.labels_
pccr['clusters']=labels
chscore_4 = metrics.calinski_harabasz_score(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1),labels)
print(chscore_4)

pccr = PCCR[['PCCR_OR_and_Anesth_Costs']].copy()
kmeans = KMeans(n_clusters=5).fit(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1))
labels = kmeans.labels_
pccr['clusters']=labels
chscore_5 = metrics.calinski_harabasz_score(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1),labels)
print(chscore_5)

pccr = PCCR[['PCCR_OR_and_Anesth_Costs']].copy()
kmeans = KMeans(n_clusters=3).fit(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1))
labels = kmeans.labels_
pccr['clusters']=labels
chscore_3 = metrics.calinski_harabasz_score(pccr['PCCR_OR_and_Anesth_Costs'].values.reshape(-1,1),labels)

pccr = pccr.sort_values(by = ['PCCR_OR_and_Anesth_Costs'], ascending = True) #排序
pccr['number'] = range(len(pccr)) #编号

pccr['clusters'] = pccr['clusters'].astype(str)
pccr.info()
pccr['clusters'] = pccr['clusters'].str.replace('0', 'Low Cost')
pccr['clusters'] = pccr['clusters'].str.replace('1', 'Medium Cost')
pccr['clusters'] = pccr['clusters'].str.replace('2', 'High Cost')

pccr.to_csv('cross_tabluate_cluster.csv',index=False)

sns.scatterplot(x='number', y='PCCR_OR_and_Anesth_Costs',
                hue = 'clusters', palette=['green','orange','red'], legend = "full",
                data=pccr)
plt.title('Cost Cluster')
plt.xlabel('number')
plt.ylabel('PCCR_OR_and_Anesth_Costs')



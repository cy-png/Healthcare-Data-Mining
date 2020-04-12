#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 17:04:35 2019

@author: yuan
"""

import pandas as pd
import scipy.stats as stats


npidata1000 = pd.read_excel('Desktop/hs_256/npidata_pfile_20050523-20191013_1000Rows.xlsx')
npidata1000.head()

npi1000 = pd.DataFrame(npidata1000)
print(npi1000)
npi1000.head()

##question 2
#filter the gender and sole proprietor columns
npi1000['Provider Gender Code'].unique()
npi1000['Is Sole Proprietor'].unique()
npisole= npi1000[['Provider Gender Code','Is Sole Proprietor']]
#delete all the nan and other types
npisole = npisole.dropna(axis=0,how='any') 
npisole['Provider Gender Code'].unique()
npisole = npisole[npisole['Is Sole Proprietor']!= 'X']
print(npisole)
npisole.groupby['Provider Gender Code']
a = npisole.groupby(by=['Provider Gender Code','Is Sole Proprietor'])['Is Sole Proprietor'].count()
obs = pd.DataFrame([[154,24], [419,87]])
new_col = ['N','Y']
obs.columns=new_col
obs.index=['F','M']

print(obs)
fisher_result = stats.fisher_exact(obs)
print(fisher_result)

##question 3
npirisk = npi1000[['Provider Gender Code','Healthcare Provider Taxonomy Cod']]
print(npirisk)
npirisk = npirisk.dropna(axis=0,how='any') 
#low:Obstetrics & Gynecology is 207V00000X,“Pediatrics”-208000000X
#high risk: Surgery - 208600000X   Orthopaedic Surgery - 207X00000X
npilowrisk=npirisk.loc[npirisk['Healthcare Provider Taxonomy Cod'].isin (['207V00000X', '208000000X'])]
print(npilowrisk)
b = npilowrisk.groupby(by=['Provider Gender Code'])['Healthcare Provider Taxonomy Cod'].size()
print(b)
npihighrisk=npirisk.loc[npirisk['Healthcare Provider Taxonomy Cod'].isin (['208600000X ', '207X00000X'])]
print(npihighrisk)
c = npihighrisk.groupby(by=['Provider Gender Code'])['Healthcare Provider Taxonomy Cod'].size()
print(c)
obs2 = pd.DataFrame([[27,1], [28,33]])
new_col = ['low','high']
obs2.columns=new_col
obs2.index=['F','M']
print(obs2)
fisher_result = stats.fisher_exact(obs2)
print(fisher_result)

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:00:50 2022


"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from datetime import datetime


#read data
dt = pd.read_excel('/Users/riva5/Downloads/CDM projects basic information.xlsx')

df = dt.copy()

#%%% data exploration
df.head()
df.info()

df.isnull().sum()

# check if the scales is unbalance
df['Project classification'].value_counts() 
## scales are not very unbalanced

#%%% data processing

# get the year of date
date_list = ['Registered or rejected','Start of first crediting period','End of first crediting period',
             'Start of Second crediting period','End of second crediting period',
             'Start of third crediting period', 'End of third crediting period']

for column in date_list:
    df[column] = df[column].dt.year

## check if the columns are only the year
df['Registered or rejected'].head()
df['Start of first crediting period'].head()


# missing data
df.isnull().sum()

## fill the mode value for some of the null values
mode_list = ['Registration project title', 'Project classification', 'Methodologies used at registration', 
       'Project type (UNEP DTU)', 'Website project status', 'Sectoral scope number(s)', 
       'List of host countries', 'Start of first crediting period','End of first crediting period']

for column in mode_list:
    df[column].fillna((df[column].mode()[0]), inplace=True)

df.isnull().sum()

## create new type(0) for the columns with lots of NA
zero_list = ['CDM project reference number','Registered or rejected',
             'Start of Second crediting period','End of second crediting period',
             'Start of third crediting period', 'End of third crediting period']

for column in zero_list:
    df[column].fillna(value = 0, inplace=True)

## create new type('unknown) for the columns with lots of NA
df['Type of crediting period'].fillna(value = 'unknown', inplace=True)

df.isnull().sum()


# year: convert float to integer
for column in date_list:
    df[column] = df[column].astype(np.int64)



# clearly Methodologies
df['Methodologies used at registration'] = df['Methodologies used at registration'].str[:3]
df['Methodologies used at registration'] = df['Methodologies used at registration'].replace(['AM0'],['AM'])
df['Methodologies used at registration'].value_counts() 
## 'ACM','AMS','AM', 'AR-'

# Rename columns
df = df.rename(columns={'Methodologies used at registration': 'Methodologies'})
df = df.rename(columns={'Project type (UNEP DTU)': 'Project_type'})
df = df.rename(columns={'Website project status': 'Status'})
df = df.rename(columns={'Type of crediting period': 'Crediting_type'})
df = df.rename(columns={'Total reductions': 'Reductions'})
df = df.rename(columns={'Start of first crediting period': 'First_crediting'})
df = df.rename(columns={'End of first crediting period': 'End_first'})
df = df.rename(columns={'List of host countries': 'Countries'})
df = df.rename(columns={'Sectoral scope number(s)': 'Scope'})


df.head()
df.info()

# Export to a new excel file
df.to_excel('update_CDM_projects_basic_information.xlsx', index = False)

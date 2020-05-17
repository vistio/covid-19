#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

file_prefix = 'Folkhalsomyndigheten_Covid19'
file_suffix = '.xlsx'
file_path = './data/FHM/'
    
list_of_files = os.listdir(file_path)


# In[2]:


list_of_files.sort()


# In[3]:


tab_name = 'Totalt antal per region'
column_no = 5
column_name = 'Totalt_antal_avlidna'


# In[4]:


rd = pd.DataFrame()


# In[5]:


for file_name in list_of_files:
    xl = pd.ExcelFile(file_path+file_name)
    regions_day = xl.parse(tab_name)
    regions_day.set_index('Region', inplace=True)
    rd = pd.concat([rd, regions_day[column_name]], axis=1)
    if len(rd.columns) > 0:
        column_names = list(rd.columns.values)
        column_names[-1] = file_name[-15:-5]
        rd.columns = column_names
    


# In[6]:


plt.rcParams['patch.edgecolor'] = 'none'
colors = ['blue/green']
pal = sns.xkcd_palette(colors)
sns.set_palette(pal)

f2, ax2 = plt.subplots(nrows=5, ncols=4, figsize=(12,12), dpi=200)

regions = [
    'Stockholm',
    'Västra Götaland',
    'Östergötland',
    'Sörmland',
    
    'Uppsala',
    'Örebro',
    'Dalarna',
    'Västmanland',
    
    'Jönköping',
    'Skåne',
    'Kronoberg',
    'Halland',
    
    'Gävleborg',
    'Västerbotten',
    'Norrbotten',
    'Jämtland Härjedalen',
    
    'Kalmar',
    'Västernorrland',
    'Blekinge',
    'Värmland'
]

g = [None] * len(regions)

i, j = (0,0)
for r in regions:
    g[i] = sns.barplot( x=rd.T.index, y=rd.diff(axis=1).T[r], ax=ax2[i][j], color=sns.xkcd_rgb['blue/green'])
    rolling = rd.diff(axis=1).T[r].rolling(10).mean().shift(-7)
    sns.lineplot(x=np.arange(len(rd.T.index)), y=rolling, ax=ax2[i][j], zorder=1, color=sns.xkcd_rgb['dark blue grey'])
    ax2[i][j].set_xlabel(r)
    if r == 'Stockholm' or r == 'Västra Götaland':
        ax2[i][j].set_ylim(0,100)
    else:
        ax2[i][j].set_ylim(0,30)
    i = i+1
    if i==5:
        j = j+1
        i = 0

f2.suptitle('COVID-19 Reported deaths per day from 2020-04-02 to ' + str(rd.T.index[-1]))
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
#tmp = plt.setp(ax2, xticks=[], ylabel=None, ylim=(0,300))
tmp = plt.setp(ax2, xticks=[], ylabel=None)

plt.savefig('reported_deaths_per_day_per_region.png', bbox_inches='tight')


# In[ ]:





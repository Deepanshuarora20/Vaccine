#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import os
import pandas as pd
import random as RB
import subprocess
from playsound import playsound


# In[2]:


import requests
import json


# In[3]:


def JSON(link):
    response = requests.get(link)
    json_response = response.json()
    df = pd.json_normalize(json_response, list(json_response.keys())[0])
    return df


# In[53]:


DIST = JSON('https://cdn-api.co-vin.in/api/v2/admin/location/districts/9')


# In[31]:


DIST = DIST[DIST['district_id'].isin([150,149,144,142])]


# In[91]:


runn = True
while runn:
    first = True
    for X in list(DIST['district_id']):
        for Y in range(5,7):
            data = JSON('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={X}&date=0{Y}-05-2021'.format(X=X,Y=Y))

            if first:
                DF = data
                first = False
            else:
                DF = pd.concat([DF,data])

    COLS = list(DF.columns)
    for COL in ['block_name','from','to','lat','long','fee_type','session_id','slots']:
        COLS.remove(COL)
    DF = DF[COLS]
    DF['fee'] = DF['fee'].astype('int')
    DF['pincode'] = DF['pincode'].astype('int')
#     DF18 = DF[DF['name'].str.contains('FORTIS')]
#     DF18 = DF[(DF['min_age_limit'] == 18)]
    DF18 = DF[(DF['min_age_limit'] == 18) & 
#     (DF['vaccine'] != 'COVISHIELD') & \
      (DF['available_capacity'] >= 1) &\
      (((DF['fee'] >= 0) & (~DF['pincode'].isin([110005,110088])))| \
      (DF['pincode'].isin([110024,110048,110049,110065])))]
#     print(len(DF18))
    if len(DF18)>=1:
        DF18 = DF18.sort_values('district_name')
        DF18.to_csv('VAC.csv',index=False)
#        playsound('mixkit-home-standard-ding-dong-109.wav')        
    time.sleep(0.5)

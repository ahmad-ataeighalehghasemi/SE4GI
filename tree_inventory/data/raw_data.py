# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:43:27 2020

@author: abdou
"""
import json
import pandas as pd
data=open("form-1__tree-inventory.json","r",encoding="utf-8")
data=json.load(data)
df = pd.DataFrame(data) #the full dataFrame
#creation of the dataFrame
q=df['data'][0] #used to creat the colums of the dataFrame
colum_name=[] #initialisation of the list of column
for col_name in q.keys():
    colum_name.append(col_name)	
df=dict(df) #dataFrame in dict
df=df['data'] #accessing to the dataFrame
df=list(df)
ind=list(range(181)) #here we creat the list of index
df=pd.DataFrame(df, index=ind, columns=colum_name)
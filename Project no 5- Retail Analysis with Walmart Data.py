#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv('Walmart_Store_sales.csv')


# In[4]:


df.info()


# In[5]:


df.head()


# In[6]:


#finding which store has maximum sales
df.loc[df['Weekly_Sales'] ==  df['Weekly_Sales'].max()]


# In[7]:


#finding which store has maximum standard deviation 'msd'
msd=pd.DataFrame(df.groupby('Store').agg({'Weekly_Sales':['std','mean']}))


# In[8]:


msd = msd.reset_index()


# In[9]:


msd['CoV'] =(msd[('Weekly_Sales','std')]/msd[('Weekly_Sales','mean')])


# In[10]:


#finding the store with maximum standard deviation.
msd.loc[msd[('Weekly_Sales','std')]==msd[('Weekly_Sales','std')].max()]


# In[11]:


#to find which store has good quarterly growth rate in Q3’2012
from datetime import date
df['Date'] = pd.to_datetime(df['Date'])


# In[12]:


#define the start and end date  Q3 and Q2
Q3_date_from = pd.Timestamp(date(2012,7,1))
Q3_date_to = pd.Timestamp(date(2012,9,30))
Q2_date_from = pd.Timestamp(date(2012,4,1))
Q2_date_to = pd.Timestamp(date(2012,6,30))


# In[14]:


#Collecting the data of Q3 and Q2 
Q2data=df[(df['Date'] > Q2_date_from) & (df['Date'] < Q2_date_to)]
Q3data=df[(df['Date'] > Q3_date_from) & (df['Date'] < Q3_date_to)]


# In[15]:


#finding the sum weekly sales of each store in Q2
Q2 = pd.DataFrame(Q2data.groupby('Store')['Weekly_Sales'].sum())
Q2.reset_index(inplace=True)
Q2.rename(columns={'Weekly_Sales': 'Q2_Weekly_Sales'},inplace=True)


# In[16]:


#finding the sum weekly sales of each store in Q2
Q3 = pd.DataFrame(Q3data.groupby('Store')['Weekly_Sales'].sum())
Q3.reset_index(inplace=True)
Q3.rename(columns={'Weekly_Sales': 'Q3_Weekly_Sales'},inplace=True)


# In[17]:


#mergeing Q2 and Q3 and Store in Q_Growth
Q_Growth= Q2.merge(Q3,how='inner',on='Store')


# In[20]:


#Calculating Growth rate   
Q_Growth['Growth_Rate'] =(Q_Growth['Q3_Weekly_Sales'] - Q_Growth['Q2_Weekly_Sales'])/Q_Growth['Q2_Weekly_Sales']
Q_Growth['Growth_Rate']=round(Q_Growth['Growth_Rate'],2)


# In[21]:


Q_Growth.sort_values('Growth_Rate',ascending=False).head()


# In[22]:


Q_Growth.sort_values('Growth_Rate',ascending=False).tail()


# In[23]:


#Find out holidays which have higher sales than the mean sales
#finding the mean sales of non holiday and holiday 
df.groupby('Holiday_Flag')['Weekly_Sales'].mean()


# In[26]:


#marking the holiday dates 
Christmas1 = pd.Timestamp(date(2010,12,31) )
Christmas2 = pd.Timestamp(date(2011,12,30) )
Christmas3 = pd.Timestamp(date(2012,12,28) )
Christmas4 = pd.Timestamp(date(2013,12,27) )


# In[27]:


DontKnow1=pd.Timestamp(date(2010,11,26) )
DontKnow2=pd.Timestamp(date(2011,11,25) )
DontKnow3=pd.Timestamp(date(2012,11,23) )
DontKnow4=pd.Timestamp(date(2013,11,29) )


# In[28]:


LabourDay1=pd.Timestamp(date(2010,2,10) )
LabourDay2=pd.Timestamp(date(2011,2,9) )
LabourDay3=pd.Timestamp(date(2012,2,7) )
LabourDay4=pd.Timestamp(date(2013,2,6) )


# In[29]:


Votingday1=pd.Timestamp(date(2010,9,12) )
Votingday2=pd.Timestamp(date(2011,9,11) )
Votingday3=pd.Timestamp(date(2012,9,10) )
Votingday4=pd.Timestamp(date(2013,9,8) )


# In[30]:


#Calculating the mean sales during the holidays
Christmas_mean_sales=df[(df['Date'] == Christmas1) | 
                        (df['Date'] == Christmas2) | 
                        (df['Date'] == Christmas3) | 
                        (df['Date'] == Christmas4)]


# In[31]:


DontKnow_mean_sales=df[(df['Date'] == DontKnow1) | 
                       (df['Date'] == DontKnow2) | 
                       (df['Date'] == DontKnow3) | 
                       (df['Date'] == DontKnow4)]


# In[32]:


LabourDay_mean_sales=df[(df['Date'] == LabourDay1) | 
                        (df['Date'] == LabourDay2) | 
                        (df['Date'] == LabourDay3) | 
                        (df['Date'] == LabourDay4)]


# In[33]:


Votingday_mean_sales=df[(df['Date'] == Votingday1) | 
                        (df['Date'] == Votingday2) | 
                        (df['Date'] == Votingday3) | 
                        (df['Date'] == Votingday4)]


# In[35]:


list_of_mean_sales = {'Christmas_mean_sales' : round(Christmas_mean_sales['Weekly_Sales'].mean(),2),
'DontKnow_mean_sales': round(DontKnow_mean_sales['Weekly_Sales'].mean(),2),
'LabourDay_mean_sales' : round(LabourDay_mean_sales['Weekly_Sales'].mean(),2),
'Votingday_mean_sales':round(Votingday_mean_sales['Weekly_Sales'].mean(),2),
'Non holiday weekly sales' : df[df['Holiday_Flag'] == 0 ]['Weekly_Sales'].mean()}
list_of_mean_sales


# In[36]:


#finding monthly and semester view of sales
#Monthly sales 
monthly = df.groupby(pd.Grouper(key='Date', freq='1M')).sum()# groupby each 1 month
monthly=monthly.reset_index()
fig, ax = plt.subplots(figsize=(10,8))
x = monthly['Date']
y = monthly['Weekly_Sales']
plt.plot(x,y)
plt.title('Month Wise Sales')
plt.xlabel('Monthly')
plt.ylabel('Weekly_Sales')


# In[37]:


#Semester Sales 
Semester = df.groupby(pd.Grouper(key='Date', freq='6M')).sum()
Semester = Semester.reset_index()
fig, ax = plt.subplots(figsize=(10,8))
x = Semester['Date']
y = Semester['Weekly_Sales']
plt.plot(x,y)
plt.title('Semester Wise Sales')
plt.xlabel('Semester')
plt.ylabel('Weekly_Sales')


# In[ ]:





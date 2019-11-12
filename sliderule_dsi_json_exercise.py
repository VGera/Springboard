#!/usr/bin/env python
# coding: utf-8

# In[1]:


# JSON examples and exercise
"""
#+ get familiar with packages for dealing with JSON
#+ study examples with JSON strings and files 
#+ work on exercise to be completed and submitted 
#****
#+ reference: http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-reader
#+ data source: http://jsonstudio.com/resources/
"""


# In[2]:


import json
from pandas.io.json import json_normalize



# In[3]:


import pandas as pd


# ## imports for Python, Pandas

# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas.pydata.org/pandas-docs/stable/io.html#normalization

# In[4]:


# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': {'governor': 'Rick Scott'},
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': {'governor': 'John Kasich'},
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[5]:


# use normalization to create tables from nested element
json_normalize(data, 'counties')


# In[6]:


# further populate tables created from nested element
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])


# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 
# + data source: http://jsonstudio.com/resources/

# In[7]:


# load json as string
json.load((open('data/world_bank_projects_less.json')))


# In[8]:


# load as Pandas dataframe
sample_json_df = pd.read_json('data/world_bank_projects_less.json')
sample_json_df


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[9]:


# Exercise 1: Find the 10 countries with most projects

# load json as string
data=json.load((open('data/world_bank_projects.json')))
# load as Pandas dataframe
json_df = pd.read_json('data/world_bank_projects.json')
relevant = json_df[['id', 'countrycode', 'countryname', 'project_name']]

# Index with country code and country name
country_group = relevant.groupby(['countrycode', 'countryname'])[['project_name']].count()

#rename the coumn name
country_group.columns = ['totalprojects']
sorted_group_project = country_group.sort_values('totalprojects',ascending =False)

sorted_group_project.head(10)


# In[10]:


#sample_json_df.info()
sample_json_df['mjtheme_namecode']
json_df.info()


# In[11]:


sample_json_df.head(10)


# In[53]:


# Exercise 2: Find the top 10 major project themes (using column 'mjtheme_namecode')

# load json as string
data=json.load((open('data/world_bank_projects.json')))

#normalize the mjtheme_namecode to make it a table 
theme_norm  =json_normalize(data,'mjtheme_namecode')

#count the frequency of occurence of each unique theme name
theme_namefreq = theme_norm['name'].value_counts()

#******* print top 10 major project themes with name ********

#identify the unique theme names for verification
uni =theme_norm['name'].unique()
#print the unique theme names and its size for verification
print("\n\b Unique Theme names: " ,uni)

#for verification of all the unique theme names
print("\n\b Unique Theme names size: ", uni.size)

#print top 10 major project themes
print("\b Top 10 major project themes with name: ")
print(theme_namefreq[:10]) # one of the theme name is also blank '' or unknown

#******* print top 10 major project themes with code ********

#due to missing names, will use the code for top 10 project themes
theme_codefreq = theme_norm['code'].value_counts()

print("\b Top 10 major project themes with code: ")
print(theme_codefreq[:10])

#print(mjtheme_raw['mjtheme_namecode'].describe())
#print(theme_norm['name'].size)


# In[112]:


# Exercise 3:  In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with
#the missing names filled in.

# load json as string
data=json.load((open('data/world_bank_projects.json')))

#normalize the mjtheme_namecode to make it a table 
theme_norm  =json_normalize(data,'mjtheme_namecode')

# Replace empty name value to None
theme_norm.loc[theme_norm['name']=='', 'name'] = None

#group wrt code and name to all the code with and without names will come together an duse ffill() 
grouped = theme_norm.sort_values(['code','name']).ffill().sort_index()

print(grouped.tail(20))


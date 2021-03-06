# -*- coding: utf-8 -*-
"""housing price(linear regression).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D16Edi6K3NMXrMgMjMfKVr4lUra9zTgH

**HOUSING PRICE**

**OBJECTIVE:**
In this problem we analyse the housing data set to identify variables effecting the price and then create a linear model and know the accuracy of the model.

upload the csv file in the colaboratory
"""

from google.colab import files
  
  
uploaded = files.upload()

"""Import libraries and dataset"""

import numpy as np 
import pandas as pd 
import io
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv(io.BytesIO(uploaded['Housing.csv']))
data.head(5)

"""Understanding the Data"""

data.columns

data.describe()

data.info()

data.isnull().sum()

"""Converting all string value into boolean"""

data['mainroad'] = data['mainroad'].map({'yes':1,'no':0})
data['guestroom'] = data['guestroom'].map({'yes':1,'no':0})
data['basement'] = data['basement'].map({'yes':1,'no':0})
data['hotwaterheating'] = data['hotwaterheating'].map({'yes':1,'no':0})
data['airconditioning'] = data['airconditioning'].map({'yes':1,'no':0})
data['prefarea'] = data['prefarea'].map({'yes':1,'no':0})

data.head(5)

data.furnishingstatus.value_counts()

sns.relplot(x='price', y='area', hue='furnishingstatus',data=data)

"""here we see that furnishing status is effecting the price of the house
and we have 3 levels in it so we will create dummies and convert the value into integers.
"""

furnishingstatus = pd.get_dummies(data['furnishingstatus'])
furnishingstatus.head()

furnishingstatus = pd.get_dummies(data['furnishingstatus'],drop_first=True)
data = pd.concat([data,furnishingstatus],axis=1)
data.head()

"""we concatinate the vlaues
and drop furnishing status as we have dummies for it
"""

data.drop(['furnishingstatus'],axis=1,inplace=True)
data.head()

"""plotting graphs to understand other factors effecting the price of the house"""

sns.relplot(x='price', y='bathrooms',data=data)

sns.relplot(x='price', y='bedrooms',data=data)

sns.relplot(x='price', y='stories',data=data)

sns.relplot(x='price', y='area', hue='basement',data=data)

"""Observation: there an increase in price with the increase in no. of bathroom, bedroom, stories and area of basement.

Rescaling the features using normalization(min-max scaling)
"""

def normalize (x): 
    return ( (x-np.min(x))/ (max(x) - min(x)))
data = data.apply(normalize)

"""predictive model"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

"""Split data into train and test sets"""

X = data[data.columns[1:]]
y = data[data.columns[:1]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=100)

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

reg = LinearRegression()
reg.fit(X_train, y_train)

predict = reg.predict(X_test)

fig = plt.figure() 
plt.scatter(y_test,predict) 
plt.xlabel('y_test', fontsize=16)
plt.ylabel('predict', fontsize=16)

predict

reg.score(X_test, y_test)
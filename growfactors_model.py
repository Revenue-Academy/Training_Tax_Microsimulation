# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 23:05:16 2022

@author: wb305167
"""
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt

df = pd.read_excel("taxcalc/growfactors_egypt.xlsx","all")
df = df[['CIT', 'oil_price','cit_rate']]
df = df.sort_values(by=['oil_price'])
df = df.dropna()
X = df[['oil_price','cit_rate']]
X = sm.add_constant(X)
Y = df[['CIT']]
model = sm.OLS(Y, X).fit()
# Predict values
CIT_hat = model.predict(X)
print_model = model.summary()
print(print_model)

# Plot regression against actual data
plt.figure(figsize=(12, 6))
plt.plot(df['oil_price'], df['CIT'], 'o')       # scatter plot showing actual data
plt.plot(df['oil_price'], CIT_hat, 'r', linewidth=2)   # regression line
plt.xlabel('Oil Price')
plt.ylabel('Predicted CIT Values')
plt.title('Oil Prices vs CIT')
plt.show()

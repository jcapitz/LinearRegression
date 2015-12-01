#!/usr/bin/python

# imports
# import libraries
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

import statsmodels.api as sm
from statsmodels.formula.api import ols

import seaborn as sns
import matplotlib.pyplot as plt

# hald data
filename = '~/Documents/LinearRegression/STAT510/quiz3/hald.txt'
df = pd.read_table(filename, delim_whitespace=True)
df['mean'] = np.mean(df['Y'])
print 'These are the first few rows of the Hald dataset:'
print ''
print df.head()

# powerset
def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

v = [df.columns[i] for i in range(1,5)]
r = [x for x in powerset(v)]  

# initialization
n = len(df)
modeldict = {'model15': ols(formula = 'Y ~ mean', data = df)}
modelp = {'model15' : 1}
paxis = [1]
models = []
rsqvals = [ols(formula = 'Y ~ mean', data = df).fit().rsquared]
adj_rsqvals = [ols(formula = 'Y ~ mean', data = df).fit().rsquared_adj]
aic = [n * np.log(ols(formula = 'Y ~ mean', data = df).fit().ssr) - n * np.log(n) + 2 * 1]
full_mse = ols(formula = 'Y ~ X1 + X2 + X3 + X4', data = df).fit().mse_resid
Cp = [(ols(formula = 'Y ~ mean', data = df).fit().ssr/full_mse) - n + 2 * 1]
counter = 0

for l in r[:-1]: # lists in r
    reg = 'Y ~ ' + l[0]
    pminus = len(l)
    p = pminus + 1
    
    for m in range(1,len(l)): # build each model l to input in ols
        reg += ' + ' + l[m]
    
    if counter < 10:
        modeldict['model' + '0' + str(counter)] = ols(formula = reg, data = df) # create dict with model objects
        modelp['model' + '0' + str(counter)] = p
    else:
        modeldict['model' + str(counter)] = ols(formula = reg, data = df)
        modelp['model' + str(counter)] = p
    
    paxis.append(p)
    rsqvals.append(ols(formula = reg, data = df).fit().rsquared)
    adj_rsqvals.append(ols(formula = reg, data = df).fit().rsquared_adj)
    aic.append(n * np.log(ols(formula = reg, data = df).fit().ssr) - n * np.log(n) + 2 * p)
    Cp.append((ols(formula = reg, data = df).fit().ssr/full_mse) - n + 2 * p)
    counter += 1
    models.append(reg)
    
models.append('Y ~ mean')
print ''
print 'The possible models are:'
print ''
for i in range(len(models)):
    print models[i]

dfr0 = DataFrame(modelp.items(), columns = ['model','P']).sort(['model'], 
                                                    ascending=[1]).reset_index(drop = True)


##### PLOT CONSTRUCTOR #####
print ''
print 'The following plots summarize our analysis:'
print ''
# set up figure
fig, axes = plt.subplots(2,2, figsize = (12,10))

# R-sq

##### This pairs the model name with the corresponding $R^2$ value

rsqdict = {}
for key, values in modeldict.iteritems():
    rsqdict[key] = values.fit().rsquared

pd.options.display.float_format = '{:20,.4f}'.format
    
dfr1 = DataFrame(rsqdict.items(), columns = ['model','R-sq']).sort(['model'], 
                                                                 ascending=[1]).reset_index(drop = True)

##### Now create a graph to illustrate the corner principle:

prsq = zip(paxis,rsqvals)

maxrsq = []
for j in range(1,6):
    maxrsq.append(max([prsq[i][1] for i in range(len(prsq)) if prsq[i][0] == j]))

axes[0,0].set_title('Corner Principle for $R^2$')
axes[0,0].scatter(paxis,rsqvals)
axes[0,0].plot(range(1,6),maxrsq)
axes[0,0].set_xlabel('p')
axes[0,0].set_ylabel('$R^2$')

# adj. R-sq

adj_rsqdict = {}
for key, values in modeldict.iteritems():
    adj_rsqdict[key] = values.fit().rsquared_adj

dfr2 = DataFrame(adj_rsqdict.items(), columns = ['model','Adj. R-sq']).sort(['model'], 
                                                                 ascending=[1]).reset_index(drop = True)

adj_prsq = zip(paxis,adj_rsqvals)

adj_maxrsq = []
for j in range(1,6):
    adj_maxrsq.append(max([adj_prsq[i][1] for i in range(len(adj_prsq)) if adj_prsq[i][0] == j]))

axes[0,1].set_title('Corner Principle for Adjusted $R^2$')
axes[0,1].scatter(paxis,adj_rsqvals)
axes[0,1].plot(range(1,6),adj_maxrsq)
axes[0,1].set_xlabel('p')
axes[0,1].set_ylabel('adj. $R^2$')

# AIC

aicdict = {}
for key, values in modeldict.iteritems():
    aicdict[key] = n * np.log(values.fit().ssr) - n * np.log(n) + 2 * values.fit().df_model

dfr3 = DataFrame(aicdict.items(), columns = ['model','AIC']).sort(['model'],
                                                           ascending=[1]).reset_index(drop = True)

paic = zip(paxis,aic)

minaic = []
for j in range(1,6):
    minaic.append(min([paic[i][1] for i in range(len(paic)) if paic[i][0] == j]))

axes[1,0].set_title('Corner Principle for AIC')
axes[1,0].scatter(paxis,aic)
axes[1,0].plot(range(1,6),minaic)
axes[1,0].set_xlabel('p')
axes[1,0].set_ylabel('AIC')

# Cp

Cpdict = {}
for key, values in modeldict.iteritems():
    Cpdict[key] = (values.fit().ssr/full_mse) - n + 2 * values.fit().df_model

dfr4 = DataFrame(Cpdict.items(), columns = ['model','Cp']).sort(['model'],
                                                           ascending=[1]).reset_index(drop = True)

pcp = zip(paxis,Cp)

mincp = []
for j in range(1,6):
    mincp.append(min([pcp[i][1] for i in range(len(pcp)) if pcp[i][0] == j]))

axes[1,1].set_title('Corner Principle for $C_p$')
axes[1,1].scatter(paxis,Cp)
axes[1,1].plot(range(1,6),mincp)
axes[1,1].set_xlabel('p')
axes[1,1].set_ylabel('$C_p$')

plt.show()

### RESULTS TABLE ###
results_tbl =  pd.concat([dfr0,dfr1['R-sq'],dfr2['Adj. R-sq'],dfr3['AIC'],dfr4['Cp']], axis = 1)
